import logging
from typing import Any, Dict
from .base_agent import BaseAgent
from .config_loader import config


class BotDPosition(BaseAgent):
    """Price Position Analyst - Analyzes price position relative to key levels."""

    @property
    def system_prompt(self):
        return config.get_agent_prompt("bot_d_position", fallback=self._FALLBACK_PROMPT)

    _FALLBACK_PROMPT = """You are the Price Position Analyst.

INPUTS:
- Current price
- Support/resistance levels
- Trend direction

OUTPUT (JSON only):
{
  "current_price": 0.0,
  "nearest_support": 0.0,
  "nearest_resistance": 0.0,
  "price_position": "NEAR_SUPPORT|NEAR_RESISTANCE|MIDDLE",
  "signal": "BUY|SELL|HOLD",
  "entry_zone": {"min": 0.0, "max": 0.0},
  "stop_loss": 0.0,
  "take_profit": 0.0,
  "confidence": 0.0,
  "reasoning": "Max 2 sentences"
}

RULES:
- If price near support -> BUY
- If price near resistance -> SELL
- Else HOLD"""

    def __init__(self, logger: logging.Logger, model_manager: Any):
        super().__init__(logger, "bot_d_position", model_manager)

    async def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Analyze price position:\n\nCurrent Price: {market_data.get('current_price', 0)}\nTrend: {market_data.get('trend_direction', 'neutral')}\nLevels: {market_data.get('levels', {})}\n\nReturn JSON only."""
        result = await self.call_model(prompt, self.system_prompt)
        if result.get("success"):
            parsed = self.parse_json_response(result.get("response", ""))
            if parsed:
                return {"success": True, "data": parsed}
        return {"success": False, "error": result.get("error", "Unknown error"), "data": {}}
