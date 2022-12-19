"""
Child process to test Span propagation with OpenTelemetry
and Jaeger.
"""
from opentelemetry import trace, context
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.context import Context
import logging
import time
import json


# Enable OpenTelemetry
app_name: str = "Batch Job"
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(instrumenting_module_name=app_name)

# Logger
logger_format: str = (
    "[%(asctime)4s : %(levelname)4s][%(filename)4s : %(name)4s : %(lineno)4s : %(funcName)4s] "
    "%(message)4s"
)
logging.basicConfig(format=logger_format)
logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_span_context(filename: str) -> Context:
    with open(file=filename, mode="r", encoding="utf-8") as cf:
        carrier_dict = json.load(fp=cf)
    print(f"Carrier dictionary: {carrier_dict}")

    # Retrieve parent span context information
    ctx = TraceContextTextMapPropagator().extract(carrier=carrier_dict)
    print("Context from TraceContext: ", ctx)
    return ctx


@tracer.start_as_current_span(name="subprocess_1")
def subprocess_1():
    print("Executing Subprocess 1")
    time.sleep(2)
    return "Subprocess 1"


@tracer.start_as_current_span(name="subprocess_2")
def subprocess_2():
    print("Executing Subprocess 2")
    time.sleep(2)
    return "Subprocess 2"


@tracer.start_as_current_span(name="child_process")
def child():
    s = trace.get_current_span()
    print(f"Span type: {type(s)}")
    s.set_attribute("child", "Executing Child Processes")
    s.add_event(name="test", attributes={"msg": "Test event from child parent execution"})
    logger.info("Executing Child Wrapper")
    subprocess_1()
    subprocess_2()


if __name__ == '__main__':
    # Retrieve the context using the trace parent from file
    ctx: Context = get_span_context(filename="test.json")
    logger.info("Context data: ", ctx)
    # Set the context globally
    context.attach(context=ctx)
    child()
