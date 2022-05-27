# OpenCTI Docker deployment

## Table of Contents
1. [Introduction](#introduction)
1. [Pre-Requisites](#pre-requisites)
1. [Clone the repository](#clone-the-repository)
1. [Configure the environment settings](#configure-the-environment-settings)
1. [Memory management settings](#memory-management-settings)
1. [Run OpenCTI](#run-opencti)

Appendices:
- [How to run in Docker Swarm](#how-to-run-in-docker-swarm)
- [How to update your docker instances](#how-to-update-your-docker-instances)
- [How to deploy behind a reverse proxy](#how-to-deploy-behind-a-reverse-proxy)
- [How to persist data](#how-to-persist-data)
- [Run OpenCTI in development mode](#run-opencti-in-development-mode)
- [Additional Elasticsearch environment variables](#additional-elasticsearch-environment-variables)
- [Memory configuration: additional information](#memory-configuration-additional-information)


## Introduction: 
OpenCTI can be deployed using the `docker-compose` command.

For **production deployment**, we advise you to deploy ElasticSearch manually in a dedicated environment and then to start the other components using Docker. The `docker-compose.yml` available on this repository is not meant to be used as it is in a production environment.


## Pre-requisites

**Docker-compose** >= 2.0.0

### 🐧 Linux:
```bash
$ sudo curl -SL https://github.com/docker/compose/releases/download/v2.5.1/docker-compose-linux-x86_64 -o /usr/bin/docker-compose
$ sudo chmod +x /usr/bin/docker-compose
```

### ⌘ MacOS
Download: https://www.docker.com/products/docker-desktop


## Clone the repository

```bash
$ git clone https://github.com/OpenCTI-Platform/docker.git /<choose-a-path>/opencti-docker
$ cd /<choose-a-path>/opencti-docker
```

## Configure the environment settings

Before running the `docker-compose` command, settings must be configured. Copy the sample settings file and change it accordingly to your needs.

```bash
$ cp .env.dist .env
```

### `OPENCTI_ADMIN_TOKEN` setting

You must change `OPENCTI_ADMIN_TOKEN` to a valid UUIDv4 token.

In case you need to **generate a UUID**, use the following command:

**🐧 Linux:**
```
$ cat /proc/sys/kernel/random/uuid
```

**⌘ MacOS**
```bash
$ uuidgen
```

### `COMPOSE_PROFILES` setting

`COMPOSE_PROFILES` is a docker-compose setting that defines the profile/mode when you run `docker-compose` command. The file `docker-compose.yml` has multiple services defined and each profile associated to each service will tell to docker-compose if that service should start or not based on the profile you define in `.env` file.

There are 3 profiles available:
* `demo`: a profile to start a demonstration instance of OpenCTI with all required services.
* `testing`: a profile to start a OpenCTI with all required services and in addition, elasticsearch in cluster mode with multiple nodes.
* `development`: a profile to start only the base services like RabbitMQ, Elasticsearch, etc. for development purposes, without OpenCTI components.

## Memory management settings

> For additional memory management information see the Memory configuration notes section

As OpenCTI has a dependency on ElasticSearch, you have to set the `vm.max_map_count` before running the containers, as mentioned in the [ElasticSearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode).

```bash
$ sudo sysctl -w vm.max_map_count=1048575
```

To make this parameter persistent, execute the following command:

```bash
$ echo "vm.max_map_count=1048575" >> /etc/sysctl.conf
```

## Run OpenCTI

> The following commands will allow you to run OpenCTI in your local instance using docker. For scenarion like using docker swarm, please see this [section](#A-how-to-run-in-docker-swarm).


### Load environment settings

Please, **do not forget** to always load the environment setttings every time you open a new terminal to interact with docker-compose services. Make sure that the environment variables are loaded in the context you are running docker-compose, **including with sudo/root**.

```bash
set -a ; source .env
```

### Execute `docker-compose` command

Run `docker-compose` in detached (`-d`) mode:

```bash
$ sudo -E docker-compose up -d
```


# Appendices

## How to run in Docker Swarm

In order to have the best experience with Docker, we recommend using the Docker stack feature. In this mode you will have the capacity to easily scale your deployment. 

If your virtual machine is not already part of a Swarm cluster, initialize a swarm:

```bash
$ sudo docker swarm init
```

Put your environment variables in the `/etc/environment`:

```bash
# If you already exported your variables to .env from above:
$ sudo cat .env >> /etc/environment
$ sudo source /etc/environment
$ sudo docker stack deploy --compose-file docker-compose.yml opencti
```

You can now go to [http://localhost:8080](http://localhost:8080/) and log in with the credentials configured in your environment variables.

## How to update your docker instances

### For single node Docker

```bash
$ sudo docker-compose stop
$ sudo docker-compose pull
$ sudo docker-compose up -d
```

### For Docker swarm

For each of services, you have to run the following command:

```bash
$ sudo docker service update --force service_name
```

## How to deploy behind a reverse proxy

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

## How to persist data

The default for OpenCTI data is to be persistent.

If you do not wish the data to persist:

```bash
$ mv docker-compose.override.no-persist.yml docker-compose.override.yml
```

## Run OpenCTI in development mode

In order to develop OpenCTI frontend or/and backend in the most efficient manner we have provided a `development` profile which stands up the infrastructure of OpenCTI, with the expectation that you will run the OpenCTI front-end (React/GraphQL) separately.

This docker-compose exposes all necessary ports for the UI/GraphQL to attach to in order to support local development.

To run the services required for local development, please perform the following steps:

1. Remove any running services using `$ sudo docker-compose down`;
2. Change the `COMPOSE_PROFILES` environment variable in your `.env` file with the value `development`;
3. Execute: `$ sudo docker-compose up -d`;

To configure/run the UI/GraphQL we would direct you to the [Notion documentation](https://luatix.notion.site/Frontend-1278fff370304cf09f6fd54ffb06f0b4)


## Additional Elasticsearch environment variables

```   
    environment:
      # Optional parameters - values may vary depending on your setup
      - bootstrap.memory_lock=true
      - http.cors.enabled=true
      - http.cors.allow-origin=*
```

> Per https://www.bluematador.com/docs/troubleshooting/aws-elasticsearch-cpu:
- 5-10 nodes: m3.medium.elasticsearch
- 10-20 nodes: m4.large.elasticsearch
- 20-50 nodes: c4.xlarge.elasticsearch
- 50-100 nodes: c4.2xlarge.elasticsearch

## Memory configuration: additional information

OpenCTI default `docker-compose.yml` file does not provide a lot of specific memory configuration. But if you want to adapt some dependencies configuration, you can find some links below.

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
