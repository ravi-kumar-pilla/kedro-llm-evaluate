from kedro.framework.hooks import hook_impl
from kedro.framework.context import KedroContext

from kedro_llm_evaluate.utils.config_registry import ConfigRegistry

class EvaluationHooks:
    @hook_impl
    def after_context_created(self, context: KedroContext) -> None:
        config_loader = context.config_loader
        llm_config = config_loader.get("parameters")
        ConfigRegistry.set_config(llm_config)


evaluation_hook_instance = EvaluationHooks()