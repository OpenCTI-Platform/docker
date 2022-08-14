# OpenCTI Docker deployment

## Table of Contents
1. [Introduction](#introduction)
1. [Pre-Requisites](#pre-requisites)
1. [Clone the repository](#clone-the-repository)
1. [Configure the environment settings](#configure-the-environment-settings)
1. [Memory management settings](#memory-management-settings)
1. [Run OpenCTI](#run-opencti)

Appendices:
- [Appendix A: How to run in Docker Swarm](#A-how-to-run-in-docker-swarm)
- [Appendix B: How to update your docker instances](#B-how-to-update-your-docker-instances)
- [Appendix C: How to deploy behind a reverse proxy](#C-how-to-deploy-behind-a-reverse-proxy)
- [Appendix D: How to persist data](#D-how-to-persist-data)
- [Appendix E: Run OpenCTI in development mode](#E-run-opencti-in-development-mode)
- [Appendix F: Memory configuration: additional information](#F-memory-configuration-additional-information)


## Introduction: 
OpenCTI can be deployed using the `docker-compose` command.

For **production deployment**, we advise you to deploy ElasticSearch manually in a dedicated environment and then to start the other components using Docker.


## Pre-requisites

### 🐧 Linux:
```bash
$ sudo apt-get install docker-compose
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
$ cp .env.sample .env
```

**Important:** you must change `OPENCTI_ADMIN_TOKEN` to a valid UUIDv4 token.

In case you need to **generate a UUID**, use the following command:

**🐧 Linux:**
```
$ cat /proc/sys/kernel/random/uuid
```

**⌘ MacOS**
```bash
$ uuidgen
```

## Memory management settings

> For additional memory management information see the Memory configuration notes section

As OpenCTI has a dependency on ElasticSearch, you have to set the `vm.max_map_count` before running the containers, as mentioned in the [ElasticSearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode).

```bash
$ sudo sysctl -w vm.max_map_count=1048575
```

To make this parameter persistent, add the following to the end of your `/etc/sysctl.conf`:

```bash
$ vm.max_map_count=1048575
```

## Run OpenCTI

> The following commands will allow you to run OpenCTI in your local instance using docker. For scenarion like using docker swarm, please see this [section](#A-how-to-run-in-docker-swarm).

Load the environment setttings:

```bash
set -a ; source .env
```

### Single node Docker with Single ElasticSearch Node
Run `docker-compose` in detached (`-d`) mode:

```bash
$ sudo docker-compose up -d
```

## Multiple ElasticSearch Nodes
Update `docker-compose.yml` to use multiple nodes:
```
    environment:
      - cluster.name=docker-cluster
```

```bash
$ sudo docker-compose -f docker-compose.yml -f docker-compose-multiple-es-nodes.yml up -d
```

  > Per https://www.bluematador.com/docs/troubleshooting/aws-elasticsearch-cpu:
  - 5-10 nodes: m3.medium.elasticsearch
  - 10-20 nodes: m4.large.elasticsearch
  - 20-50 nodes: c4.xlarge.elasticsearch
  - 50-100 nodes: c4.2xlarge.elasticsearch

### Optional Elasticsearch Environment variables:
```   
    environment:
      # Optional parameters - values may vary depending on your setup
      - bootstrap.memory_lock=true
      - http.cors.enabled=true
      - http.cors.allow-origin=*
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
```
      
### Docker swarm
=======

# Appendices

## A. How to run in Docker Swarm

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

## B. How to update your docker instances

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

## C. How to deploy behind a reverse proxy

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

## D. How to persist data

The default for OpenCTI data is to be persistent.

If you do not wish the data to persist:

```bash
$ mv docker-compose.override.no-persist.yml docker-compose.override.yml
```

## E. Run OpenCTI in development mode

In order to develop OpenCTI frontend or/and backend in the most efficient manner we have provided a `docker-compose.dev.yml` which stands up the infrastructure of OpenCTI, with the expectation that you will run the OpenCTI front-end (React/GraphQL) separately.

This docker-compose exposes all necessary ports for the UI/GraphQL to attach to in order to support local development.

To run the services required for local development run:
```bash
$ sudo docker-compose up -f docker-compose.dev.yml -d
```

To configure/run the UI/GraphQL we would direct you to the [Notion documentation](https://luatix.notion.site/Frontend-1278fff370304cf09f6fd54ffb06f0b4)

## F. Memory configuration: additional information

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

## About

### Authors

OpenCTI is a product powered by the collaboration of the private company [Filigran](https://www.filigran.io), the [French national cybersecurity agency (ANSSI)](https://ssi.gouv.fr), the [CERT-EU](https://cert.europa.eu) and the [Luatix](https://www.luatix.org) non-profit organization.