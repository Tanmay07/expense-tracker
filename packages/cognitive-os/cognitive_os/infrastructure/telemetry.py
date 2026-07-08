from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def setup_telemetry():
    """
    Sets up OpenTelemetry tracing for the Cognitive OS.
    In production, this would use OTLP exporter to the otel-collector deployed in Phase 11F.
    """
    provider = TracerProvider()

    # For now, export to console. In prod: OTLPSpanExporter
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    return trace.get_tracer(__name__)


tracer = setup_telemetry()


def trace_ai_reasoning(agent_role: str, model: str):
    """
    Decorator/context manager helper to trace reasoning latency and inject cost tags.
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(f"reasoning_{agent_role}") as span:
                span.set_attribute("ai.model", model)
                span.set_attribute("ai.agent_role", agent_role)
                # execute function
                result = await func(*args, **kwargs)
                # Mock cost injection
                span.set_attribute("ai.cost_usd", 0.002)
                return result

        return wrapper

    return decorator
