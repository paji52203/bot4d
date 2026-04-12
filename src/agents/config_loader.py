import os
from typing import Dict, Any

CONFIGPROMP_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "configpromp",
)


class AgentsConfig:
    """Centralized configuration loader for AI Agents from .env files."""

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
        value = value.strip()
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        if value.lower() in ("true", "false"):
            return value.lower() == "true"

        # strip one-line wrapped quotes
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        return value

    def _load_env_file(self, filepath: str) -> Dict[str, Any]:
        config = {}
        if not os.path.exists(filepath):
            return config

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        i = 0
        n = len(lines)
        while i < n:
            raw = lines[i].rstrip("\n")
            line = raw.strip()

            if not line or line.startswith("#") or "=" not in line:
                i += 1
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key == "SYSTEM_PROMPT":
                # support multiline triple-quoted values
                if value.startswith("'''") or value.startswith('"""'):
                    quote = value[:3]
                    remainder = value[3:]

                    # one-line triple quote
                    if remainder.endswith(quote):
                        prompt = remainder[:-3]
                    else:
                        chunks = []
                        if remainder:
                            chunks.append(remainder)
                        i += 1
                        while i < n:
                            part = lines[i].rstrip("\n")
                            end_idx = part.find(quote)
                            if end_idx != -1:
                                chunks.append(part[:end_idx])
                                break
                            chunks.append(part)
                            i += 1
                        prompt = "\n".join(chunks)

                    config[key] = prompt
                else:
                    config[key] = self._parse_env_value(value).replace("\\n", "\n")
            else:
                config[key] = self._parse_env_value(value)

            i += 1

        return config

    def _load_all_configs(self) -> Dict[str, Any]:
        configs = {"global": {}, "agents": {}}

        if not os.path.exists(CONFIGPROMP_DIR):
            print(f"Warning: configpromp folder not found at {CONFIGPROMP_DIR}")
            return configs

        global_env = os.path.join(CONFIGPROMP_DIR, "global.env")
        configs["global"] = self._load_env_file(global_env)

        agent_files = [
            "analysis_agent.env",
            "core_agent.env",
            "manager_agent.env",
            "market_intelligence_agent.env",
            "risk_agent.env",
            "bot_d_position.env",
        ]

        for agent_file in agent_files:
            agent_name = agent_file.replace(".env", "")
            agent_env = os.path.join(CONFIGPROMP_DIR, agent_file)
            agent_config = self._load_env_file(agent_env)
            if agent_config:
                configs["agents"][agent_name] = agent_config

        return configs

    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        return self._config.get("agents", {}).get(agent_name, {})

    def get_agent_prompt(self, agent_name: str, fallback: str = "") -> str:
        agent_config = self.get_agent_config(agent_name)
        return agent_config.get("SYSTEM_PROMPT", fallback)

    def get_global_settings(self) -> Dict[str, Any]:
        return self._config.get("global", {})


config = AgentsConfig()
