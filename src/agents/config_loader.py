import os
import re
from typing import Dict, Any, Optional

# Path to configpromp folder
CONFIGPROMP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "configpromp")


class AgentsConfig:
    """Centralized configuration loader for 5 AI Agents from .env files."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._config = self._load_all_configs()
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse env value to appropriate type."""
        value = value.strip()
        # Try to convert to number
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        # Boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        return value
    
    def _load_env_file(self, filepath: str) -> Dict[str, Any]:
        """Load a single .env file."""
        config = {}
        if not os.path.exists(filepath):
            return config
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Unescape \n to actual newlines for SYSTEM_PROMPT
                if key == 'SYSTEM_PROMPT':
                    value = value.replace('\\n', '\n')
                else:
                    value = self._parse_env_value(value)
                config[key] = value
        return config
    
    def _load_all_configs(self) -> Dict[str, Any]:
        """Load all .env files from configpromp folder."""
        configs = {
            "global": {},
            "agents": {}
        }
        
        if not os.path.exists(CONFIGPROMP_DIR):
            print(f"Warning: configpromp folder not found at {CONFIGPROMP_DIR}")
            return configs
        
        # Load global settings
        global_env = os.path.join(CONFIGPROMP_DIR, "global.env")
        configs["global"] = self._load_env_file(global_env)
        
        # Load each agent config
        agent_files = [
            "analysis_agent.env",
            "core_agent.env",
            "manager_agent.env",
            "market_intelligence_agent.env",
            "risk_agent.env"
        ]
        
        for agent_file in agent_files:
            agent_name = agent_file.replace(".env", "")
            agent_env = os.path.join(CONFIGPROMP_DIR, agent_file)
            agent_config = self._load_env_file(agent_env)
            if agent_config:
                configs["agents"][agent_name] = agent_config
        
        return configs
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Get configuration for a specific agent."""
        return self._config.get("agents", {}).get(agent_name, {})
    
    def get_agent_prompt(self, agent_name: str) -> str:
        """Get system prompt for a specific agent."""
        agent_config = self.get_agent_config(agent_name)
        return agent_config.get("SYSTEM_PROMPT", "")
    
    def get_global_settings(self) -> Dict[str, Any]:
        """Get global AI settings."""
        return self._config.get("global", {})


# Singleton instance for easy import
config = AgentsConfig()
