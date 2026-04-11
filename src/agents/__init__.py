"""Multi-Agent AI System for Trading Decisions.

This module implements a 5-agent architecture:
1. Analysis Agent - Technical Analysis Specialist
2. Core Agent - Identity Controller & Output Validator
3. Manager Agent - Final Decision Synthesizer
4. Market Intelligence Agent - Sentiment & Context Specialist
5. Risk Agent - Risk Validator with Veto Power
"""

from .base_agent import BaseAgent
from .analysis_agent import AnalysisAgent
from .core_agent import CoreAgent
from .manager_agent import ManagerAgent
from .market_intelligence_agent import MarketIntelligenceAgent
from .risk_agent import RiskAgent
from .orchestrator import AgentsOrchestrator
from .config_loader import AgentsConfig, config

__all__ = [
    "BaseAgent",
    "AnalysisAgent",
    "CoreAgent",
    "ManagerAgent",
    "MarketIntelligenceAgent",
    "RiskAgent",
    "AgentsOrchestrator",
    "AgentsConfig",
    "config",
]
