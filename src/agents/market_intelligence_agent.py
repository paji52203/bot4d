import logging
import json
import re
from typing import Any, Dict, Optional

from .base_agent import BaseAgent
from .config_loader import config


class MarketIntelligenceAgent(BaseAgent):
    """Sentiment & Historical Context Specialist."""

    @property
    def system_prompt(self):
        return config.get_agent_prompt("market_intelligence_agent")

    _FALLBACK_PROMPT = """You are the Market Intelligence Specialist for a High-Frequency Crypto Trading System.
Analyze sentiment/news/funding and return STRICT JSON only."""

    def __init__(self, logger: logging.Logger, model_manager: Any):
        super().__init__(logger, "market_intelligence_agent", model_manager)

    def _extract_first_json_object(self, text: str) -> str:
        """Extract first balanced JSON object from noisy model output."""
        if not text:
            return ""

        cleaned = text.strip()
        cleaned = re.sub(r"^```(?:json)?\\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\\s*```$", "", cleaned)

        start = cleaned.find("{")
        if start == -1:
            return ""

        depth = 0
        for i in range(start, len(cleaned)):
            ch = cleaned[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return cleaned[start:i+1]
        return ""

    def _robust_parse(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse model response to dict with fallback normalization."""
        if not text:
            return None

        parsed = self.parse_json_response(text)
        if isinstance(parsed, dict):
            return parsed

        candidate = self._extract_first_json_object(text)
        if not candidate:
            return None

        # Normalize percentage literals that break JSON numeric parsing (e.g. 57.23%)
        candidate = re.sub(r"(-?\\d+(?:\\.\\d+)?)%", r"\\1", candidate)

        try:
            obj = json.loads(candidate)
            return obj if isinstance(obj, dict) else None
        except Exception as e:
            self.logger.error(f"{self.name} fallback parse failed: {e}")
            return None

    async def analyze(self, market_context: Dict[str, Any], trade_history: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze market intelligence factors."""
        prompt = f"""Analyze market intelligence:\n\nMarket Context: {market_context}\nTrade History: {trade_history or {}}\n\nReturn ONLY valid JSON."""

        result = await self.call_model(prompt, self.system_prompt)
        if result.get("success"):
            parsed = self._robust_parse(result.get("response", ""))
            if parsed:
                return {"success": True, "data": parsed}

        return {"success": False, "error": result.get("error", "Market intel failed")}
