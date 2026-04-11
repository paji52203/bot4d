import logging
from typing import Any, Dict
from .base_agent import BaseAgent
from .config_loader import config


class RiskAgent(BaseAgent):
    """Risk Validator & Trade Safety Guard with VETO POWER."""
    
    # System prompt loaded from centralized config at config/agents_config.json
    @property
    def system_prompt(self):
        return config.get_agent_prompt("risk_agent")
    
    # Fallback prompt kept for reference
    _FALLBACK_PROMPT = """You are the Risk Validator & Safety Guard for a High-Frequency Crypto Trading System.

Your Mission: Validate ALL trading decisions against risk parameters.
You have VETO POWER over unsafe trades.

VETO CONDITIONS (HARD NO-GO):
| Condition | Action | Severity |
|-----------|--------|----------|
| R/R < 1.5 | VETO to HOLD | CRITICAL |
| Stop Loss > 2% from entry | VETO with adjusted SL | CRITICAL |
| Position size > 5% account | VETO with reduced size | CRITICAL |
| Daily loss > 3% of account | VETO all new positions | CRITICAL |
| Open position count >= max | VETO new entry | INFO |

POSITION SIZING FORMULA:
base_size = confidence / 100
Adjustments:
- MIXED timeframe: -0.20
- DIVERGENT timeframe: -0.35
- ADX < 20: multiply by 0.7
- Losing streak: multiply by 0.5
final_size = clamp(base_size, 0.10, account_max)

OUTPUT FORMAT:
{
  "risk_validation": {
    "veto_applied": boolean,
    "veto_reason": "string or null",
    "approved_signal": "BUY|SELL|HOLD|CLOSE|UPDATE",
    "risk_score": 0-100,
    "risk_level": "low|moderate|elevated|critical"
  },
  "adjustments_made": {
    "stop_loss_adjusted": boolean,
    "adjusted_sl": number or null,
    "position_size_adjusted": boolean,
    "adjusted_position_size": 0.0-1.0 or null
  },
  "warnings": [{"type": "string", "severity": "info|warning|critical"}],
  "safe_to_proceed": boolean
}

Maximum 1 minute response time."""
    
    def __init__(self, logger: logging.Logger, model_manager: Any):
        super().__init__(logger, "RiskAgent", model_manager)
    
    async def validate(self, proposed_signal: Dict[str, Any], account_context: Dict[str, Any], market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate trading decision against risk rules."""
        prompt = f"""Validate this trading decision:

Proposed Signal: {proposed_signal}
Account Context: {account_context}
Market Context: {market_context}

Apply risk rules and return validation in JSON format."""
        
        result = await self.call_model(prompt, self.system_prompt)
        if result["success"]:
            parsed = self.parse_json_response(result["response"])
            if parsed:
                return {"success": True, "data": parsed}
        return {"success": False, "error": result.get("error", "Risk validation failed")}
