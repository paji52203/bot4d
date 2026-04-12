"""Multi-Agent AI System for Trading Decisions.

This module implements a 5-agent architecture:
1. Analysis Agent - Technical Analysis Specialist
2. Core Agent - Identity Controller & Output Validator
3. Bot D Position - Price Position Analyst
4. Market Intelligence Agent - Sentiment & Context Specialist
5. Risk Agent - Risk Validator with Veto Power
6. Manager Agent - Final Decision Synthesizer
"""

from .base_agent import BaseAgent
from .analysis_agent import AnalysisAgent
from .core_agent import CoreAgent
from .bot_d_position import BotDPosition
from .manager_agent import ManagerAgent
from .market_intelligence_agent import MarketIntelligenceAgent
from .risk_agent import RiskAgent
from .orchestrator import AgentsOrchestrator
from .config_loader import AgentsConfig, config

__all__ = [
    "BaseAgent",
    "AnalysisAgent",
    "CoreAgent",
    "BotDPosition",
    "ManagerAgent",
    "MarketIntelligenceAgent",
    "RiskAgent",
    "AgentsOrchestrator",
    "AgentsConfig",
    "config",
]
