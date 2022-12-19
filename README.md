# OpenTelemetry Quick Start

This repository provides a quick start example about how to use OpenTelemetry to enable observability features
in web and batch applications using automatic and manual instrumentation.

# Requirements

1. Python >= 3.10
2. Docker >= 20.10

# Installation

Clone this repository, change your personal working directory to it (```cd <repo_path>```), then:

1. Deploy OpenTelemetry Collector and Jaeger using Docker Compose: ```docker compose -f services.yaml up -d```
2. Start the web server: ```bash start-server.sh```

# Usage

There is a single endpoint available at ```/``` that is going to execute some dummy functions that will leave their own trace.
After their execution, the web server will trigger one batch job. Their traces will be reported as an extension of the parent span.

You can trigger the endpoint via web browser opening ```http://localhost:9000/``` or via CLI using cURL ```curl -X GET http://localhost:9000/```

After you trigger the endpoint, access Jaeger UI via ```http://localhost:16686/search``` then click ```Find Traces``` button and finally click the top trace on the list [1].
You will see the traces of the services involved in the execution [2].

## Reference figures

### Jaeger UI Search Panel [1]
![Jaeger UI](https://user-images.githubusercontent.com/37672135/208459696-8c716e5b-e210-40a8-867a-e88d4eda4fe0.png)

### Jaeger UI Trace Panel [2]
![Jaeger Trace](https://user-images.githubusercontent.com/37672135/208459786-925b64ed-516c-4b79-a7fa-1820cd7a11f5.png)

# Uninstalling

Close the web server clicking ```Ctrl + C``` in the same console you used to started it. Finish the services execution using ```docker compose -f services.yaml down```
