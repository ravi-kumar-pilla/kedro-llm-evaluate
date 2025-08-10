from kedro_llm_evaluate.evaluators.opik.opik_evaluator import OpikEvaluator

def get_evaluator(config: dict):
    framework = config.get("framework", "opik")  # default
    if framework == "opik":
        return OpikEvaluator(config[framework])
    else:
        raise ValueError(f"Unsupported framework: {framework}")
