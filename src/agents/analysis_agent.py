import logging
from typing import Any, Dict
from .base_agent import BaseAgent
from .config_loader import config


class AnalysisAgent(BaseAgent):
    """Technical Analysis Specialist - Multi-timeframe analysis."""
    
    # System prompt loaded from centralized config at config/agents_config.json
    @property
    def system_prompt(self):
        return config.get_agent_prompt("analysis_agent")
    
    # Fallback prompt kept for reference
    _FALLBACK_PROMPT = """You are the Technical Analysis Specialist for a High-Frequency Crypto Trading System.

Your Mission: Perform rapid, thorough technical analysis across multiple timeframes.
FOCUS ONLY on price action, indicators, patterns, and market structure.
Return CONCISE, structured JSON results.

Analysis Timeframe Priority:
- PRIMARY: User-specified (e.g., 1h, 4h, 15m)
- SECONDARY: 1D (daily macro)
- TERTIARY: Weekly + 365D (long-term context)

Step-by-Step Analysis:
1. MULTI-TIMEFRAME TREND ASSESSMENT: State ALIGNED/MIXED/DIVERGENT
2. TECHNICAL INDICATORS: RSI, MACD, ADX, ATR, Volume
3. PATTERN RECOGNITION: HH/HL, classic patterns, candlesticks
4. SUPPORT & RESISTANCE: Key levels with 3+ touches

Output Format (STRICT JSON):
{
  "timeframe_analysis": {
    "alignment": "ALIGNED|MIXED|DIVERGENT",
    "dominant_timeframe": "4h|1d|weekly",
    "trends": {"primary": "BULLISH|BEARISH|NEUTRAL", "daily": "BULLISH|BEARISH|NEUTRAL"}
  },
  "indicator_summary": {
    "rsi": {"value": 0-100, "status": "oversold|neutral|overbought"},
    "macd": {"signal": "bullish|bearish|neutral"},
    "adx": {"value": 0-100, "trend_strength": "weak|developing|strong"},
    "atr": {"value": number, "volatility": "low|medium|high"}
  },
  "confluence_score": {
    "trend_alignment": 0-100, "momentum_strength": 0-100,
    "volume_support": 0-100, "pattern_quality": 0-100,
    "support_resistance_strength": 0-100
  },
  "key_levels": {"support": [level1, level2], "resistance": [level1, level2]}
}

Time Budget: 2.5 minutes MAX."""
    
    def __init__(self, logger: logging.Logger, model_manager: Any):
        super().__init__(logger, "analysis_agent", model_manager)
    
    async def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform technical analysis on market data."""
        prompt = f"""Analyze the following market data:
Symbol: {market_data.get("symbol", "BTC/USDT")}
Timeframe: {market_data.get("timeframe", "15m")}
Current Price: {market_data.get("current_price", 0)}
OHLCV Data: {market_data.get("ohlcv_summary", "")}
Indicators: {market_data.get("indicators", {})}

Provide your technical analysis in the required JSON format."""
        
        result = await self.call_model(prompt, self.system_prompt)
        if result["success"]:
            parsed = self.parse_json_response(result["response"])
            if parsed:
                return {"success": True, "data": parsed}
        return {"success": False, "error": result.get("error", "Analysis failed")}
