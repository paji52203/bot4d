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
        super().__init__(logger, "manager_agent", model_manager)


    def _compact_agent_outputs(self, agent_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Reduce token load: keep only fields relevant for final decision."""
        def pick(d: Dict[str, Any], keys):
            if not isinstance(d, dict):
                return {}
            return {k: d.get(k) for k in keys if k in d}

        out = {}
        for name, payload in (agent_outputs or {}).items():
            if not isinstance(payload, dict):
                out[name] = {"success": False}
                continue

            data = payload.get("data", payload)
            compact = {"success": bool(payload.get("success", True))}

            if name == "analysis":
                compact.update(pick(data, [
                    "signal", "confidence", "trend", "market_structure", "regime", "strength", "volatility", "market_quality",
                    "momentum_profile", "volume_profile", "candle_anatomy", "key_levels",
                    "entry", "stop_loss", "take_profit", "reasoning"
                ]))
            elif name == "core":
                compact.update(pick(data, [
                    "signal", "confidence", "timeframe_alignment", "entry", "stop_loss", "take_profit",
                    "risk_reward", "entry_quality", "fakeout_risk", "action", "approved", "reasoning"
                ]))
            elif name == "risk":
                compact.update(pick(data, [
                    "signal", "confidence", "approved", "veto", "veto_reason", "risk_level", "risk_score",
                    "position_size", "position_size_usdt", "leverage", "entry", "stop_loss", "take_profit",
                    "adjusted_entry", "adjusted_stop_loss", "adjusted_take_profit", "adjusted_risk_reward", "account_snapshot", "reasoning"
                ]))
            elif name == "market_intelligence":
                compact.update(pick(data, [
                    "sentiment", "context_score", "market_condition", "news_impact", "fear_greed",
                    "news_sentiment", "funding", "market_data", "data_stale", "reasoning"
                ]))
            elif name == "bot_d_position":
                compact.update(pick(data, [
                    "signal", "confidence", "current_price", "nearest_support", "nearest_resistance",
                    "price_position", "entry_zone", "wick_signal", "stop_loss", "take_profit", "reasoning"
                ]))
            elif name == "_meta":
                compact.update(pick(data, [
                    "context_completeness", "instruction"
                ]))
            else:
                compact.update(pick(data, ["signal", "confidence", "reasoning"]))

            out[name] = compact

        return out

    async def synthesize(self, agent_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize all agent outputs into final decision."""
        compact = self._compact_agent_outputs(agent_outputs)

        prompt = f"""You are final trading judge.
Input is already summarized by 5 specialist bots.
Decide ONE action: BUY, SELL, or HOLD.

Return STRICT JSON only with this exact schema:
{{
  "signal": "BUY|SELL|HOLD",
  "confidence": 0-100,
  "entry": number,
  "stop_loss": number,
  "take_profit": number,
  "position_size": 0.0-1.0,
  "reasoning": "short reason"
}}

Summaries:
{compact}
"""

        result = await self.call_model(prompt, self.system_prompt)
        if result.get("success"):
            parsed = self.parse_json_response(result.get("response", ""))
            if parsed and isinstance(parsed, dict):
                return {"success": True, "data": parsed}

        return {"success": False, "error": result.get("error", "Synthesis failed")}

