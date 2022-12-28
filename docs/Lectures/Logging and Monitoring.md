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


# Better Uptime

A free tool to monitoring website availabiltiy that help to:

- monitor response time/usage
- receive Alerts
- Incident Management

# Prometehus & Grafana        

Prometheus: Collect metrics (Capture/Storaging) & Alerting

- PormQL  

Grafana show the metrics collected by Prometheus

## Summary and Histograms

In Prometheus, a histogram is a type of metric that is used to represent the distribution of a set of values. A histogram consists of a series of bins (or buckets), each representing a range of values, and the number of elements that fall into each bin is counted and recorded. For example, you might use a histogram to represent the distribution of the response time of requests from a Web server.

A summary, on the other hand, is also a type of metric in Prometheus, but it is used to represent summary statistics of a set of values, such as the mean, median, maximum, and minimum. A summary is similar to a histogram, but instead of counting the number of elements in each bin, it tracks statistics on all the values that were recorded. For example, you might use a summary to represent summary statistics of the response time of requests from a web server.

In summary, a histogram is used to represent the distribution of values of a metric, while a summary is used to represent summary statistics of a metric.


There are many use cases for histograms in Prometheus. Here are some examples of the use of histograms:

1. Monitoring the response time of web server requests: you can use a histogram to represent the distribution of your web server's request response times. For example, you can use a histogram to see how many requests had a response time of less than 100ms, how many had a response time between 100ms and 1s, and so on.

2. Monitor the size of HTTP requests: you can use a histogram to monitor the size of HTTP requests your web server is receiving. For example, you can use a histogram to see how many requests are less than 1KB in size, how many are between 1KB and 10KB in size, and so on.

3. Monitor the amount of memory used by applications: you can use a histogram to monitor the memory usage of your applications. For example, you can use a histogram to see how many applications use less than 100MB of memory, how many use between 100MB and 1GB, and so on.

4. Monitor the execution time of database queries: you can use a histogram to monitor the execution time of database queries. For example, you can use a histogram to see how many queries were executed in less than 100ms, how many were executed between 100ms and 1s, and so on.
    
There are many use cases for summaries in Prometheus. Here are some examples of use cases for summaries:

1. Monitor a web server's request response times: you can use a summary to represent summary statistics of your web server's request response times, such as average, median, maximum, and minimum.

2. Monitor the size of HTTP requests: you can use a summary to monitor summary statistics of the size of HTTP requests your web server is receiving, such as the average, median, maximum, and minimum.

3. Monitor the amount of memory used by applications: you can use a summary to monitor summary statistics of the memory usage of your applications, such as the average, median, maximum, and minimum.

4. Monitor the execution time of database queries: you can use a summary to monitor summary statistics of the execution time of database queries, such as the average, median, maximum, and minimum.