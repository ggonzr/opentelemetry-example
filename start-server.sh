#!/bin/bash

# Install packages if they does not exists
VENV="$(pwd)/opentelemetry"


# Execute FastAPI web application
execute() {
  # To customize OpenTelemetry instrumentation features
  # This should be overriden using environment variables
  # More information: https://opentelemetry.io/docs/reference/specification/sdk-environment-variables/

  # Environment variables
  SERVICE_NAME='fastapi-test-server'
  OTLP_ENDPOINT='http://localhost:24000'

  # Set enviroment variables to OpenTelemetry
  export OTEL_RESOURCE_ATTRIBUTES=service.name=$SERVICE_NAME
  export OTEL_EXPORTER_OTLP_ENDPOINT=$OTLP_ENDPOINT

  # Start server using OpenTelemetry
  opentelemetry-instrument python main.py
}

virtualenv() {
  mkdir -p $VENV
  python3 -m venv $VENV
}

activate() {
  source $VENV/bin/activate
}

install() {
  python3 -m pip install -r "$(pwd)/requirements.txt"
}

# Main execution
if [ ! -d "$VENV" ];
then
  echo "Virtual enviroment does not exists at: $VENV!"
  echo "Creating it"
  virtualenv
  echo "Virtual enviroment created, installing packages"
  activate
  install
  echo "Packages installed: "
  python3 -m pip freeze
else
  echo "Virtual enviroment exists at: $VENV"
  echo "Assuming all packages were installed before"
  echo "Activating enviroment"
  activate
  echo "Packages available: "
  python3 -m pip freeze
fi

# Execute server
echo "Executing web server"
execute

