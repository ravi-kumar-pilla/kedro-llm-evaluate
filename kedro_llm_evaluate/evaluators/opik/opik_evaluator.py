from opik import Opik
from opik.evaluation import evaluate_prompt
from opik.evaluation.metrics import Hallucination, AnswerRelevance
from kedro_llm_evaluate.evaluators.base import BaseLLMEvaluator

class OpikEvaluator(BaseLLMEvaluator):
    def __init__(self, config: dict):
        # config keys: project_name, host, etc.
        self.client = Opik(**config)
        self._current_trace = None

    def start_trace(self, metadata: dict):
        """
        Start a new Opik trace.  
        metadata should include at least 'model' and 'prompt'.
        """
        # create trace with initial input
        self._current_trace = self.client.trace(
            name=metadata.get("trace_name", "blog_summarizer_test_trace"),
            input={"prompt": metadata["prompt"], "model": metadata["model"]},
        )
        return self._current_trace

    def end_trace(self, metadata: dict):
        """
        Finish the trace by logging the LLM span and closing it.
        metadata should include 'output' (the LLM response).
        """
        if not self._current_trace:
            return

        # log the LLM call itself as a span
        self._current_trace.span(
            name=metadata.get("span_name", "blog_summarizer_test_span"),
            type="llm",
            input={"prompt": metadata["prompt"], "model": metadata["model"]},
            output={"response": metadata["output"]},
        )
        
        # dataset = self.client.get_or_create_dataset("blog_summary_eval")

        # 3. Insert rows (prompt, reference, prediction)
        # dataset.insert([{
        #     "input": metadata["prompt"],
        #     "expected_output": "Artificial intelligence (AI) has transformed the healthcare industry in the last decade, with applications in predictive diagnostics",
        #     "generated_output": metadata["output"]
        # }])

        # evaluate_prompt(
        #     dataset=dataset,
        #     messages=[{"role": "user", "content": metadata["prompt"]}],
        #     model="groq/llama3-8b-8192",
        #     scoring_metrics=[AnswerRelevance(model="groq/llama3-8b-8192"), Hallucination(model="groq/llama3-8b-8192")]
        # )
        metric = AnswerRelevance(model="groq/llama3-8b-8192", project_name="blog_summarizer_test")
        metric.score(
            input=metadata["prompt"],
            output=metadata["output"],
            context=["AI changing the world."],
        )
        
        # end the trace
        self._current_trace.end()
        self._current_trace = None
