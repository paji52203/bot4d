import logging
import json
import re
from typing import Any, Dict, Optional
from .base_agent import BaseAgent
from .config_loader import config


class RiskAgent(BaseAgent):
    """Risk Management & Validation Specialist."""

    @property
    def system_prompt(self):
        return config.get_agent_prompt("risk_agent")

    def __init__(self, logger: logging.Logger, model_manager: Any):
        super().__init__(logger, "risk_agent", model_manager)

    def _extract_first_json_object(self, text: str) -> str:
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
        if not text:
            return None

        parsed = self.parse_json_response(text)
        if isinstance(parsed, dict):
            return parsed

        candidate = self._extract_first_json_object(text)
        if not candidate:
            return None

        # normalize percentage literals if model emits numeric like 1.2%
        candidate = re.sub(r"(-?\\d+(?:\\.\\d+)?)%", r"\\1", candidate)

        try:
            obj = json.loads(candidate)
            return obj if isinstance(obj, dict) else None
        except Exception as e:
            self.logger.error(f"{self.name} fallback parse failed: {e}")
            return None

    async def validate(self, proposal: Dict[str, Any], market_data: Dict[str, Any], current_price: float = None) -> Dict[str, Any]:
        """Validate trading proposal and risk parameters."""
        prompt = f"""Validate risk for this proposal:\n\nProposal: {proposal}\nMarket Data: {market_data}\nCurrent Price: {current_price}\n\nReturn ONLY valid JSON."""

        result = await self.call_model(prompt, self.system_prompt)
        if result.get("success"):
            parsed = self._robust_parse(result.get("response", ""))
            if parsed:
                return {"success": True, "data": parsed}

        return {"success": False, "error": result.get("error", "Risk validation failed")}
