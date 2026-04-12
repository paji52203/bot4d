import logging
from .config_loader import config
from typing import Any, Dict, Optional
import json
import re


class BaseAgent:
    """Base class for all trading agents."""
    
    def __init__(self, logger: logging.Logger, name: str, model_manager: Any):
        self.logger = logger
        self.name = name
        self.model_manager = model_manager
    
    async def call_model(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        """Call the AI model with the given prompt using config settings."""
        try:
            # Get agent-specific settings from config
            agent_config = config.get_agent_config(self.name)
            
            # Case-insensitive model lookup - try MODEL first (from .env), then model
            model = None
            if agent_config:
                model = agent_config.get('MODEL') or agent_config.get('model')
            
            # Fallback to global default if no agent-specific model
            if not model:
                global_config = config.get_global_settings()
                model = global_config.get('DEFAULT_MODEL')
            
            # Ultimate fallback to Claude Haiku (not deepseek!)
            if not model:
                model = 'openrouter/anthropic/claude-3-haiku'
                self.logger.warning(f"No model configured for {self.name}, using Claude Haiku fallback")
            
            # Log model selection for debugging
            self.logger.info(f"{self.name} using model: {model}\nAgent config: {agent_config}")
            
            temperature = agent_config.get('TEMPERATURE', agent_config.get('temperature', 0.1)) if agent_config else 0.1
            max_tokens = agent_config.get('MAX_TOKENS', agent_config.get('max_tokens', 4096)) if agent_config else 4096
            
            response = await self.model_manager.query_async(
                prompt=prompt,
                system_prompt=system_prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return {"success": True, "response": response}
        except Exception as e:
            self.logger.error(f"{self.name} model call failed: {e}")
            return {"success": False, "error": str(e)}
    
    def parse_json_response(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse JSON from model response robustly (supports trailing notes)."""
        try:
            if not text:
                return None

            t = str(text).strip()

            # Strip markdown fences when present
            t = re.sub(r"^```(?:json)?\s*", "", t, flags=re.IGNORECASE)
            t = re.sub(r"\s*```$", "", t)

            # 1) Fast path
            try:
                obj = json.loads(t)
                return obj if isinstance(obj, dict) else None
            except Exception:
                pass

            # 2) Parse first JSON object and ignore trailing text
            decoder = json.JSONDecoder()
            start = t.find('{')
            if start != -1:
                obj, _ = decoder.raw_decode(t[start:])
                return obj if isinstance(obj, dict) else None

            return None
        except Exception as e:
            self.logger.error(f"{self.name} JSON parse error: {e}")
            return None
