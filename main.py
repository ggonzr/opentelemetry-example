"""
Hello world server to test observability features with OpenTelemetry
and Jaeger.

Some quick start guides:
https://uptrace.dev/opentelemetry/distributed-tracing.html
https://opentelemetry.io/docs/concepts/observability-primer/
"""
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import uvicorn
import time
import json
import subprocess
import os

# Instantiate server
app: FastAPI = FastAPI()

# Append OpenTelemetry instrumentation wrapper
# Instrumentation libraries help to include OpenTelemetry automatically avoiding
# manual changes.
# Some examples: https://github.com/open-telemetry/opentelemetry-python/tree/main/docs/examples
#
# Instrumentation package for FastAPI:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
FastAPIInstrumentor.instrument_app(app=app)

# Get current tracer
tracer = trace.get_tracer("FastAPI")

# Current path
current_path = os.getcwd()


@tracer.start_as_current_span(name="custom_action")
def custom_action():
    time.sleep(2)
    return "Custom Action Finished"


@tracer.start_as_current_span(name="custom_action_2")
def custom_action_2():
    time.sleep(5)
    return "Custom Action v2 Finished"


@tracer.start_as_current_span(name="store_current_context")
def store_span_context(carrier: dict, filename: str):
    with open(file=filename, encoding="utf-8", mode="w") as cf:
        json.dump(obj=carrier, fp=cf, indent=4)


# Some test endpoints
@tracer.start_as_current_span(name="parent_endpoint")
@app.get(path="/")
def hello():
    # Retrieve current span and add some extra info
    # Events - They can be seen as logs for the current span
    # Attributes - Custom metadata for the span
    # https://opentelemetry.io/docs/concepts/signals/traces/#attributes

    span = trace.get_current_span()
    span.set_attribute("action", "Custom Action Override")
    span.add_event("custom-event", {"msg": "Custom Event Message"})

    # There are several ways to achieve distribute tracing
    # Its purpose is to retrieve runtime execution context information from several microservices
    # and allow developers and operators to check through time the workflow execution
    # At this time, we are going to persist context information manually using the W3C trace protocol
    # However, the vision of OpenTelemetry is to provide several implementation libraries to include
    # automatically observability features. Currently, there are several connectors
    # to enable distributed tracing without configure it manually.
    #
    # https://opentelemetry.io/docs/concepts/signals/traces/#context-propagation
    # https://opentelemetry.io/docs/instrumentation/python/automatic/
    # These automatically connectors generally share parent span context information
    # via request metadata, for example, HTTP headers.

    # We are going to store the parent span tracing information inside a JSON file,
    # the second process inside the current trace is going to be a batch process developed using Python.
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier=carrier)
    store_span_context(carrier=carrier, filename="test.json")

    # The following dummy functions mimic some auxiliary functions
    # required by some process
    c_a_v1 = custom_action()
    c_a_v2 = custom_action_2()

    # Fire and forget batch process
    batch_command: str = f"/bin/bash ./start-child.sh"
    command: list[str] = batch_command.strip().split(" ")
    subprocess.call(
        args=command,
        cwd=current_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # HTTP Response
    return {
        "action_1": c_a_v1,
        "action_2": c_a_v2,
    }


if __name__ == '__main__':
    print(f"Current working path: {current_path}")
    uvicorn.run(
        app=app,
        host="localhost",
        port=9000,
    )
