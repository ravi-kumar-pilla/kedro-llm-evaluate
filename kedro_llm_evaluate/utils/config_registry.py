# kedro_llm_evaluate/config_registry.py
class ConfigRegistry:
    _llm_config = {}

    @classmethod
    def set_config(cls, config: dict):
        cls._llm_config = config

    @classmethod
    def get_config(cls) -> dict:
        return cls._llm_config
