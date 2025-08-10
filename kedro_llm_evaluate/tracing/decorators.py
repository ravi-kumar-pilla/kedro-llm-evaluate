from functools import wraps
from kedro_llm_evaluate.tracing.context_manager import trace_llm

def trace_llm_call(model: str, prompt_arg: str, extra_metadata: dict = None):
    """
    Decorator that wraps a function returning the LLM output.
    It will call trace_llm() around that function.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            prompt = kwargs.get(prompt_arg) or (args[0] if args else "<no prompt>")
            with trace_llm(model, prompt, extra_metadata) as span:
                result = fn(*args, **kwargs)
                # Attach output for end_trace
                if span is not None:
                    span.output_value = result
                return result
        return wrapper
    return decorator
