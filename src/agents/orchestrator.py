import logging
from typing import Any, Dict, Optional
from datetime import datetime

from .base_agent import BaseAgent
from .analysis_agent import AnalysisAgent
from .core_agent import CoreAgent
from .manager_agent import ManagerAgent
from .market_intelligence_agent import MarketIntelligenceAgent
from .risk_agent import RiskAgent


class AgentsOrchestrator:
    """Orchestrates the 5 AI agents for trading decisions."""
    
    def __init__(self, logger: logging.Logger, model_manager: Any):
        self.logger = logger
        self.model_manager = model_manager
        
        # Initialize all 5 agents
        self.analysis_agent = AnalysisAgent(logger, model_manager)
        self.core_agent = CoreAgent(logger, model_manager)
        self.manager_agent = ManagerAgent(logger, model_manager)
        self.market_agent = MarketIntelligenceAgent(logger, model_manager)
        self.risk_agent = RiskAgent(logger, model_manager)
        
        self.logger.info("5 AI Agents initialized: Analysis, Core, Manager, MarketIntel, Risk")
    
    async def process_decision(self, market_analysis: Optional[Dict[str, Any]] = None, current_price: Optional[float] = None, symbol: Optional[str] = None, timeframe: Optional[str] = None) -> Dict[str, Any]:
        """Run all 5 agents and return final trading decision.
        
        Flow:
        1. Analysis Agent - Technical analysis
        2. Market Intelligence Agent - Sentiment & context
        3. Risk Agent - Risk validation
        4. Core Agent - Format validation
        5. Manager Agent - Final synthesis
        """
        start_time = datetime.utcnow()
        agent_outputs = {}
        
        try:
            # Agent 1: Technical Analysis
            self.logger.info("Agent 1/5: Analysis Agent processing...")
            market_data = {"current_price": current_price, "symbol": symbol, "timeframe": timeframe, "analysis": market_analysis}
            analysis_result = await self.analysis_agent.analyze(market_data)
            agent_outputs["analysis"] = analysis_result
            
            # Agent 2: Market Intelligence
            self.logger.info("Agent 2/5: Market Intelligence Agent processing...")
            market_result = await self.market_agent.analyze(market_data)
            agent_outputs["market_intelligence"] = market_result
            
            # Agent 3: Risk Validation
            self.logger.info("Agent 3/5: Risk Agent processing...")
            proposed_signal = {
                "signal": "HOLD",
                "confidence": 50,
                "entry_price": current_price or market_analysis.get("current_price", 0) if market_analysis else 0,
                "stop_loss": current_price or market_analysis.get("current_price", 0) if market_analysis else 0 * 0.99,
                "take_profit": current_price or market_analysis.get("current_price", 0) if market_analysis else 0 * 1.02,
                "position_size": 0.5
            }
            risk_result = await self.risk_agent.validate(proposed_signal, market_data)
            agent_outputs["risk"] = risk_result
            
            # Agent 4: Core Validation
            self.logger.info("Agent 4/5: Core Agent processing...")
            core_result = await self.core_agent.validate(proposed_signal, analysis_result.get("data", {}))
            agent_outputs["core"] = core_result
            
            # Agent 5: Manager Synthesis (Final Decision)
            self.logger.info("Agent 5/5: Manager Agent synthesizing...")
            final_result = await self.manager_agent.synthesize(agent_outputs)
            
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            self.logger.info(f"All 5 agents completed in {elapsed:.2f}s")
            
            return {
                "success": True,
                "decision": final_result.get("data", {}),
                "agent_outputs": agent_outputs,
                "processing_time_seconds": elapsed
            }
            
        except Exception as e:
            self.logger.error(f"Agents orchestrator error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent_outputs": agent_outputs
            }
