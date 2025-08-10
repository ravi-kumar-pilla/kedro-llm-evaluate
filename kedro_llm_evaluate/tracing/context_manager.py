from contextlib import contextmanager
from kedro_llm_evaluate.utils.factory import get_evaluator
from kedro_llm_evaluate.utils.config_registry import ConfigRegistry

@contextmanager
def trace_llm(model: str, prompt: str, extra_metadata: dict = None):
    config = ConfigRegistry.get_config()
    if not config.get("enabled", False):
        yield None
        return
    
    metadata = {"model": model, "prompt": prompt, **(extra_metadata or {})}
    evaluator = get_evaluator(config)
    
    span = evaluator.start_trace(metadata)

    try:
        yield span
    finally:
        # User code must attach 'output' to metadata before close
        output = getattr(span, "span_output", None)
        if output is not None:
            evaluator.end_trace({"prompt": prompt, 
                                 "model": model, 
                                 "output": output})
        else:
            evaluator.end_trace(metadata)