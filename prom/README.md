# Prometheus server settings

In order to pull the metrics we need to:

<li> Tell to docker where to store the metrics <b>YourIP:YourPort</b>. "Prometheus expects metrics to be available on targets on a path of /metrics". This is done by going to <b>Docker Preferences -> Docker Engine</b> and adding the rows:

<br>
{
<br>
"experimental": true,
<br>
"metrics-addr": "YourIP:YourPort"
<br>
}

<br>

</li>
<li> Track some metrics with Python library od Prometheus
<li> Setup the <b>prometheus.yml</b> specifying as target the <b>YourIP:YourPort</b> from the first step
<li> Start the Containers with docker compose

The metrics tracked with Python will be made available at <b>YourIP:YourPort/metrics</b> and Prometheus will pull them periodically.

## Example

A brief example of the configuration of my machine

### Docker engine file:

    {
      "builder": {
        "gc": {
          "defaultKeepStorage": "20GB",
          "enabled": true
        }
      },
      "experimental": true,
      "features": {
        "buildkit": true
      },
      "metrics-addr": "0.0.0.0:9000"
    }

As you can see docker will store the metrics on port 9000 of localhost. When the backend container (server) on which the metrics are tracked will be started, then the metrics will be stored at <b>0.0.0.0:9000/metrics.</b>

### Prometheus yaml

The prometheus configuration file follows.

    global:
      scrape_interval: 5s
    scrape_configs:
      - job_name: prometheus_api
        static_configs:
          - targets: ['docker.for.mac.localhost:9000']
        relabel_configs:
          - source_labels: [__address__]
            target_label: __param_target
          - source_labels: [__param_target]
            target_label: instance
          - target_label: __address__
            replacement: docker.for.mac.localhost:9000

When the container of Prometheus will be started, it will pull the metrics from localhost:9000/metrics every 5 seconds.

By default Prometheus is accessible on port 9090 of the container, so be sure that in your docker compose there is the following mapping between the public/private port:

<br>
<b>YourPublicPort:9090</b>

<br>

#### Piece of docker-compose.yml 
    prometheus:
        container_name: prometheus_container
        ports:
          - '9300:9090'
        build:
          context: ./prom
          dockerfile: Dockerfile
        depends_on:
          - backend

The Prometheus UI will be available at localhost:9300