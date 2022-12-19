#!/bin/bash

# Environment variables
SERVICE_NAME='batch-worker'
OTLP_ENDPOINT='http://localhost:24000'

# Set enviroment variables to OpenTelemetry
export OTEL_RESOURCE_ATTRIBUTES=service.name=$SERVICE_NAME
export OTEL_EXPORTER_OTLP_ENDPOINT=$OTLP_ENDPOINT

# Start server using OpenTelemetry
opentelemetry-instrument python child.py
