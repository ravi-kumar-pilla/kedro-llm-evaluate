class BaseLLMEvaluator:
    def start_trace(self, metadata: dict) -> None:
        """Start trace. Store metadata like model, prompt, etc."""
        raise NotImplementedError

    def end_trace(self, result: str) -> None:
        """End trace with final result."""
        raise NotImplementedError

    def evaluate(self, reference: str, prediction: str) -> dict:
        """Optional: Evaluate outputs against a reference."""
        raise NotImplementedError
