# Kedro LLM Evaluate

A Kedro plugin for evaluating and tracing Large Language Model (LLM) outputs in your data science pipelines.

## 🎯 What is kedro_llm_evaluate?

`kedro_llm_evaluate` is a Kedro plugin that seamlessly integrates LLM evaluation and tracing capabilities into your Kedro pipelines. It provides automated tracking, evaluation metrics, and observability for LLM-powered data processing workflows, addressing the critical need for monitoring and improving LLM performance in production data pipelines.

## 🏗️ Architecture

The plugin follows a modular architecture with the following components:

```
kedro_llm_evaluate/
├── evaluators/          # Pluggable evaluation backends
│   ├── base.py          # Base evaluator interface
│   └── opik/            # Opik evaluator implementation
│       ├── opik_evaluator.py # Opik implementation
│       └── Dockerfile   # Docker setup for Opik
├── tracing/             # LLM call tracing utilities
│   ├── decorators.py    # @trace_llm_call decorator
│   ├── context_manager.py # Context manager for tracing
│   └── logger.py        # Logging utilities
├── utils/               # Core utilities
│   ├── config_registry.py # Configuration management
│   └── factory.py       # Evaluator factory pattern
├── hooks.py             # Kedro lifecycle hooks
└── launchers/           # CLI extensions
    └── cli.py          # CLI command implementations
```

### Key Components:

- **BaseLLMEvaluator**: Abstract interface for evaluation backends
- **OpikEvaluator**: Implementation using Opik for tracing and evaluation
- **Tracing System**: Decorators and context managers for automatic LLM call tracking
- **Configuration Registry**: Centralized configuration management
- **Kedro Hooks**: Automatic integration with Kedro pipeline lifecycle

## 📋 Prerequisites

- Python 3.9+
- Kedro project
- Optional: Opik account for advanced evaluation features

## 🚀 Installation

```bash
pip install kedro-llm-evaluate
```

For Opik integration:
```bash
pip install kedro-llm-evaluate[opik]
```

## 📖 Usage

### 1. Configuration

Add LLM evaluation configuration to your `parameters.yml`:

```yaml
# conf/base/parameters.yml
llm_evaluation:
  enabled: true
  evaluator: "opik"
  config:
    project_name: "my-llm-project"
    # Additional Opik configuration
```

### 2. Using the Decorator

Wrap your LLM functions with the tracing decorator:

```python
from kedro_llm_evaluate.tracing.decorators import trace_llm_call

@trace_llm_call(model="gpt-4", prompt_arg="prompt")
def summarize_text(prompt: str) -> str:
    # Your LLM call logic here
    response = llm_client.generate(prompt)
    return response
```

### 3. Using the Context Manager

For more control over tracing:

```python
from kedro_llm_evaluate.tracing.context_manager import trace_llm

def process_document(text: str) -> str:
    with trace_llm("gpt-4", "Summarize this text", {"document_id": "doc_123"}) as span:
        result = llm_client.generate(f"Summarize: {text}")
        if span:
            span.output_value = result
        return result
```

## 🎉 Benefits & Value

### Immediate Benefits:
- **Automated LLM Tracking**: Zero-code instrumentation of LLM calls in your pipelines
- **Performance Monitoring**: Track response times, token usage, and success rates

### Business Value:
- **Reliability**: Ensure consistent LLM performance in production
- **Compliance**: Maintain audit trails for LLM decisions
- **Optimization**: Data-driven insights for prompt and model improvements
- **Scalability**: Monitor LLM performance across large-scale data pipelines

## 🔮 Next Steps After MVP

### Phase 1: Enhanced Evaluation
- [ ] Support for additional evaluation backends (DeepEval)
- [ ] Custom evaluation metrics framework
- [ ] Cost analysis and optimization recommendations
- [ ] Model drift detection

The plugin is particularly valuable for:
- **Data Science Teams** running LLM-powered pipelines in production
- **MLOps Engineers** needing observability for LLM components
- **Organizations** requiring audit trails and quality assurance for AI decisions
- **Research Teams** conducting systematic LLM evaluations at scale

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the the [Apache 2.0](https://github.com/ravi-kumar-pilla/kedro-llm-evaluate/blob/main/LICENSE) License.

## 🔗 Related Links

- [Kedro Documentation](https://docs.kedro.org)
- [Opik Documentation](https://www.comet.com/docs/opik/)
- [Issue Tracker](https://github.com/kedro-org/kedro/issues)