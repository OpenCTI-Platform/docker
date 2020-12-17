# OpenCTI Docker deployment

OpenCTI can be deployed using the *docker-compose* command.

For production deployment, we advise you to deploy ElasticSearch manually in a dedicated environment and then to start the other components using Docker.

## Pre-requisites

To install OpenCTI using Docker, you will need the docker-compose command, you can install it using:

```bash
$ sudo apt-get install docker-compose
```

## Clone the repository

```bash
$ mkdir /path/to/your/app && cd /path/to/your/app
$ git clone <https://github.com/OpenCTI-Platform/docker.git>
$ cd docker
```

## Configure the environment

Before running the `docker-compose` command, the `docker-compose.yml` file must be configured.  Two ways to do that:

- Use environment variables as it is proposed and you have an exemple in the `.env.sample` file (ie. `APP__ADMIN__EMAIL=${OPENCTI_ADMIN_EMAIL}`).
- Directly set the parameters in the `docker-compose.yml`.

 Whether you are using one method or the other, here are the mandatory parameters to fill:

```bash
[OPENCTI_ADMIN_EMAIL=admin@opencti.io](mailto:OPENCTI_ADMIN_EMAIL=admin@opencti.io) # Valid email address
OPENCTI_ADMIN_PASSWORD=ChangeMe # String
OPENCTI_ADMIN_TOKEN=ChangeMe # Valid UUIDv4
MINIO_ACCESS_KEY=ChangeMeAccess # String
MINIO_SECRET_KEY=ChangeMeKey # String
RABBITMQ_DEFAULT_USER=guest # String
RABBITMQ_DEFAULT_PASS=guest # String
CONNECTOR_HISTORY_ID=ChangeMe # Valid UUIDv4
CONNECTOR_EXPORT_FILE_STIX_ID=ChangeMe # Valid UUIDv4
CONNECTOR_EXPORT_FILE_CSV_ID=ChangeMe # Valid UUIDv4
CONNECTOR_IMPORT_FILE_STIX_ID=ChangeMe # Valid UUIDv4
CONNECTOR_IMPORT_FILE_PDF_OBSERVABLES_ID=ChangeMe # Valid UUIDv4
```

As OpenCTI has a dependency on ElasticSearch, you have to set the `vm.max_map_count` before running the containers, as mentioned in the [ElasticSearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode).

```bash
$ sudo sysctl -w vm.max_map_count=1048575

```

To make this parameter persistent, please update your `/etc/sysctl.conf` file and add the following line at the end:

```bash
$ vm.max_map_count=1048575
```

## Run

### Using single node Docker

You can deploy without using Docker swarm, with a the `docker-compose` command. After changing your `.env` file, just type:

```bash
$ sudo docker-compose up -d
```

### Using Docker swarm

In order to have the best experience with Docker, we recommend using the Docker stack feature. In this mode you will have the capacity to easily scale your deployment. If your virtual machine is not a part of a Swarm cluster, please use:

```bash
$ sudo docker swarm init
```

Then, you have to put your environment variables in the `/etc/environment` and then:

```bash
$ sudo source /etc/environment
$ sudo docker stack deploy --compose-file docker-compose.yml opencti
```

You can now go to [http://localhost:8080](http://localhost:8080/) and log in with the credentials configured in your environment variables.

## Update

### Using single node Docker

```bash
$ sudo docker-compose stop
$ sudo docker-compose pull
$ sudo docker-compose up -d
```

### Using Docker swarm

For each of services, you have to run the following command:

```bash
$ sudo docker service update --force service_name
```

## Deploy behind a reverse proxy

If you want to use OpenCTI behind a reverse proxy with a context path, like `https://myproxy.com/opencti`, please change the base_path configuration.

```yaml
- APP__BASE_PATH=/opencti
```

By default OpenCTI use websockets so don't forget to configure your proxy for this usage, an example with `Nginx`:

```bash
location / {
    proxy_cache               off;
    proxy_buffering           off;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    chunked_transfer_encoding off;
    proxy_pass http:/YOUR_UPSTREA_BACKEND;
  }
```

## Data persistence

If you wish your OpenCTI data to be persistent while in production, you should be aware of the `volumes` section for `ElasticSearch`, `MinIO`, `Redis` and `RabbitMQ` services in the `docker-compose.yml`.

Here is an example of volumes configuration:

```
volumes:
  esdata:
    driver: local
    driver_opts:
      o: bind
      type: none
  s3data:
    driver: local
    driver_opts:
      o: bind
      type: none      
  redisdata:
    driver: local
    driver_opts:
      o: bind
      type: none
  amqpdata:
    driver: local
    driver_opts:
      o: bind
      type: none
```

## Memory configuration

OpenCTI default `docker-compose.yml` file does not provide any specific memory configuration. But if you want to adapt some dependencies configuration, you can find some links below.

### OpenCTI - Platform

OpenCTI platform is based on a NodeJS runtime, with a memory limit of **512MB by default**. We do not provide any option to change this limit today. If you encounter any `OutOfMemory` exception, please open a [Github issue](https://github.com/OpenCTI-Platform/opencti/issues/new?assignees=&labels=&template=bug_report.md&title=).

### OpenCTI - Workers and connectors

OpenCTI workers and connectors are Python processes. If you want to limit the memory of the process, we recommend to directly use Docker to do that. You can find more information in the [official Docker documentation](https://docs.docker.com/compose/compose-file/).

If you do not use Docker stack, think about --compatibility option.

### ElasticSearch

ElasticSearch is also a JAVA process. In order to setup the JAVA memory allocation, you can use the environment variable `ES_JAVA_OPTS`.

The minimal recommended option today is -Xms8G -Xmx8G.

You can find more information in the [official ElasticSearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html).

### Redis

Redis has a very small footprint and only provides an option to limit the maximum amount of memory that can be used by the process. You can use the option `--maxmemory` to limit the usage.

You can find more information in the [Redis docker hub](https://hub.docker.com/r/bitnami/redis/).

### MinIO

MinIO is a small process and does not require a high amount of memory. More information are available for Linux here on the [Kernel tuning guide](https://github.com/minio/minio/tree/master/docs/deployment/kernel-tuning).

### RabbitMQ

The RabbitMQ memory configuration can be find in the [RabbitMQ official documentation](https://www.rabbitmq.com/memory.html). RabbitMQ will consumed memory until a specific threshold, therefore it should be configure along with the Docker memory limitation.