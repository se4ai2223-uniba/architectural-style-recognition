# Prometheus server settings

In order to pull the metrics we need to:

<li> Serve the metrics on an ip and a port <b>YourIP:YourPort</b>. "Prometheus expects metrics to be available on targets on a path of /metrics". 
<li> Track some metrics with Python library od Prometheus
<li> Setup the <b>prometheus.yml</b> specifying as target the <b>YourIP:YourPort</b> from the first step
<li> Start the Containers with docker compose

The metrics tracked with Python will be made available at <b>YourIP:YourPort/metrics</b> and Prometheus will pull them periodically.

## Example

A brief example of the configuration of my machine.
As eaxmple we can track metrics from Docker as follows:
<b>Docker Preferences -> Docker Engine</b> and adding the rows:

<br>
{
<br>
"experimental": true,
<br>
"metrics-addr": "YourIP:YourPort"
<br>
}

<br>

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
      "metrics-addr": "0.0.0.0:8967"
    }

As you can see docker will store the metrics on port 8967 of localhost.

### Prometheus yaml

The prometheus configuration file follows.
If you change the port on Docker engine you'll need to update the port in this file!

    global:
      scrape_interval: 5s

    scrape_configs:
      - job_name: 'prometheus'
        scrape_interval: 5s
        static_configs:
         - targets: ['docker.for.mac.localhost:8967']

When the container of Prometheus will be started, it will pull the metrics from localhost:8967/metrics every 5 seconds.

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



### Real case scenario

The Python script has to be adapted in order to serve the metrics on a port so that Prometheus can pull them as happens with the metrics pulled from Docker in this example.