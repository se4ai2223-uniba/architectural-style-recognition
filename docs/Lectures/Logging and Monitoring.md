# Logging and Monitoring 🖥️

## 1.1 Logging ⏲️

Save state, events, errors logs during time.

## 1.2 Monitoring

- Alerting: know when something goeas wrong (fauilres or problems i.i application running slowly)

- Debugging: get system information to reason about

- Trending: what are trends in using the system

### 1.2.1 Classic Monitoring

#### Resource Level
Used in every system, checking if all system is running and if all is okay (Latency, CPU, RAM, alive)

- Better Uptime: alert if service stop working (reciving email or similar and getting statistics)

- Prometheus: database that stores metrics (Counter: number of requests/errors/tasks completed etc. Gouge: number of concurrent requests, running containers, RAM, CPU usage basically every alue that can go up or down) from application based on time series.

    - Pull: expose metrics from application via an API.
    - Push: push metrics from app to Prometheus.

- Grafana: visualization tool for Prometheus

#### Performance Level
Monitor the performance level, check if the model still behave well like in the design test (monitor incoming data and output)

Drift: reason on why the model is becoming stale due the new incoming data on which the model must be retrained.

- Data Drift: feature input change the distribution with the original distribution of original set.

- Target Drift (prediction drift): removal or addition of new classes with categorical tasks

- Concept Drift: relation between input and output changed because for "external event" (i.e. Covid Pandemic changed the predictions about travelling agency/ Recurring Events)


#### Drift Detection

is made using Drift Detector in two ways:

- Batch

- Online
