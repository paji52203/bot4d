import logging
from typing import Any, Dict
from .base_agent import BaseAgent
from .config_loader import config


class CoreAgent(BaseAgent):
    """Identity Controller & Output Format Validator."""
    
    # System prompt loaded from centralized config at config/agents_config.json
    @property
    def system_prompt(self):
        return config.get_agent_prompt("core_agent")
    
    # Fallback prompt kept for reference
    _FALLBACK_PROMPT = """You are the Core Identity Controller for an Institutional-Grade Crypto Trading System.

Your Mission: Validate and enforce the trading identity, output format, and decision structure.
You DO NOT perform analysis - you ensure the final output follows strict institutional standards.

Trading Mode: AGGRESSIVE SCALPING
- Target Profit: 1% - 3% per trade
- Stop Loss: 0.5% - 1.5% from entry

Decision Thresholds:
- BUY: confidence >= 70, R/R >= 2.0, 5+ confluences
- SELL: confidence >= 70, R/R >= 2.0, 5+ confluences
- HOLD: Any signal < 70 confidence or insufficient confluence
- CLOSE: Exit existing position immediately
- UPDATE: Adjust SL/TP of existing position

Validate that the output follows this JSON structure:
{
  "signal": "BUY|SELL|HOLD|CLOSE|UPDATE",
  "confidence": 0-100,
  "entry_price": number,
  "stop_loss": number,
  "take_profit": number,
  "position_size": 0.0-1.0,
  "reasoning": "string",
  "risk_reward_ratio": number
}

Return ONLY a validated JSON object. No markdown, no explanation."""
    
    def __init__(self, logger: logging.Logger, model_manager: Any):
        super().__init__(logger, "CoreAgent", model_manager)
    
    async def validate(self, proposed_decision: Dict[str, Any], analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a proposed trading decision."""
        prompt = f"""Validate this proposed trading decision:

Proposed Decision: {proposed_decision}
Analysis Data: {analysis_data}

Check if it meets the thresholds and format requirements.
Return validated JSON with validation_status and any adjustments."""
        
        result = await self.call_model(prompt, self.system_prompt)
        if result["success"]:
            parsed = self.parse_json_response(result["response"])
            if parsed:
                return {"success": True, "data": parsed}
        return {"success": False, "error": result.get("error", "Validation failed")}
