import logging
from typing import Any, Dict
from .base_agent import BaseAgent
from .config_loader import config


class MarketIntelligenceAgent(BaseAgent):
    """Sentiment & Historical Context Specialist."""
    
    # System prompt loaded from centralized config at config/agents_config.json
    @property
    def system_prompt(self):
        return config.get_agent_prompt("market_intelligence_agent")
    
    # Fallback prompt kept for reference
    _FALLBACK_PROMPT = """You are the Market Intelligence Specialist for a High-Frequency Crypto Trading System.

Your Mission: Analyze market sentiment, news impact, and historical trading performance.

Task 1: FEAR & GREED SENTIMENT
- Index Value: 0-100
- Classification: EXTREME_FEAR/FEAR/NEUTRAL/GREED/EXTREME_GREED
- Interpretation: Extreme fear = potential buy, Extreme greed = potential sell

Task 2: BRAIN CONTEXT - TRADE HISTORY
- Analyze historical win rates by confidence level
- Extract key learnings from similar setups
- Calibrate confidence based on historical performance

Task 3: MARKET MICROSTRUCTURE
- Order book bias: buy_pressure/sell_pressure/balanced
- Recent trades analysis

Task 4: NEWS & EVENT IMPACT
- Market-moving news detection
- Sentiment override assessment

COMBINED OUTPUT FORMAT:
{
  "market_intelligence": {
    "sentiment": {"current_fear_greed": 0-100, "classification": "..."},
    "brain_context": {"confidence_calibration_suggestion": 0-100},
    "microstructure": {"order_book_bias": "buy_pressure|sell_pressure|balanced"},
    "news_impact": {"has_market_moving_event": boolean}
  },
  "final_sentiment_score": 0-100,
  "sentiment_alignment": "bullish|bearish|neutral"
}

Time Budget: 2.5 minutes MAX."""
    
    def __init__(self, logger: logging.Logger, model_manager: Any):
        super().__init__(logger, "MarketIntelligenceAgent", model_manager)
    
    async def analyze(self, market_context: Dict[str, Any], trade_history: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze market intelligence factors."""
        prompt = f"""Analyze market intelligence:

Market Context: {market_context}
Trade History: {trade_history or {}}

Provide market intelligence analysis in JSON format."""
        
        result = await self.call_model(prompt, self.system_prompt)
        if result["success"]:
            parsed = self.parse_json_response(result["response"])
            if parsed:
                return {"success": True, "data": parsed}
        return {"success": False, "error": result.get("error", "Market intel failed")}
