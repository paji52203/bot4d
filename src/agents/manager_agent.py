import logging
from typing import Any, Dict
from .base_agent import BaseAgent
from .config_loader import config


class ManagerAgent(BaseAgent):
    """Final Decision Synthesizer - Orchestrates all agent outputs."""
    
    # System prompt loaded from centralized config at config/agents_config.json
    @property
    def system_prompt(self):
        return config.get_agent_prompt("manager_agent")
    
    # Fallback prompt kept for reference
    _FALLBACK_PROMPT = """You are the Trading Decision Orchestrator - the FINAL AUTHORITY for all trading signals.

Your Mission: Synthesize outputs from 4 specialized agents into ONE definitive trading decision.

DECISION MATRIX (Weighted Scoring):
| Factor | Weight | Source |
|--------|--------|--------|
| Technical Confluence | 35% | Analysis Agent |
| Risk Assessment | 30% | Risk Rules Agent |
| Sentiment Alignment | 15% | Market Intel Agent |
| Brain Context | 15% | Market Intel Agent |
| Format Validation | 5% | Core Agent |

SIGNAL DETERMINATION LOGIC:
1. Check Risk Veto - if veto_applied, signal = HOLD/CLOSE
2. Calculate Composite Score based on timeframe alignment
3. Apply sentiment and brain modifiers
4. Final confidence = base + modifiers (clamped 0-100)
5. Signal = BUY/SELL if confidence >= 70 AND R/R >= 2.0, else HOLD

FINAL OUTPUT FORMAT (STRICT JSON):
{
  "final_decision": {"signal": "BUY|SELL|HOLD|CLOSE|UPDATE", "confidence": 0-100},
  "order_details": {"entry_price": number, "stop_loss": number, "take_profit": number, "position_size": 0.0-1.0},
  "synthesis": {"trend_assessment": "string", "risk_assessment": "string"},
  "reasoning": "1-2 sentence explanation"
}

Return ONLY the JSON object. NO markdown, NO explanation."""
    
    def __init__(self, logger: logging.Logger, model_manager: Any):
        super().__init__(logger, "ManagerAgent", model_manager)
    
    async def synthesize(self, agent_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize all agent outputs into final decision."""
        prompt = f"""Synthesize these agent outputs into a final trading decision:

Agent Outputs: {agent_outputs}

Apply the decision matrix and return the final decision in JSON format."""
        
        result = await self.call_model(prompt, self.system_prompt)
        if result["success"]:
            parsed = self.parse_json_response(result["response"])
            if parsed:
                return {"success": True, "data": parsed}
        return {"success": False, "error": result.get("error", "Synthesis failed")}
