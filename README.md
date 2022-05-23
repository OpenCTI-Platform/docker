# OpenCTI Docker deployment

## Table of Contents
1. [Pre-Requisites](#1-pre-requisites)
2. [Clone the Repository](#2-clone-the-repository)
3. [Configure the environment](#3-configure-the-environment)
4. [Memory Management Settings](#4-memory-management-settings)
5. [Run OpenCTI - Full-stack, including UI](#5-run-open-cti-full-stack-including-ui)
6. [Run OpenCTI infrastructure with UI/GraphQL in development mode](#6-run-opencti-infrastructure-with-uigraphql-in-development-mode)

Appendices:
- [Appendix A: How to update your docker instances](#A-how-to-update-your-docker-instances)
- [Appendix B: How to deploy behind a reverse proxy](#B-how-to-deploy-behind-a-reverse-proxy)
- [Appendix C: How to persist data](#C-how-to-persist-data)
- [Appendix D: Memory configuration: additional information](#D-memory-configuration-additional-information)


## Introduction: 
OpenCTI can be deployed using the `docker-compose` command.

For production deployment, we advise you to deploy ElasticSearch manually in a dedicated environment and then to start the other components using Docker.

## 1. Pre-requisites

`docker-compose`:
### 🐧 Linux:

```bash
$ sudo apt-get install docker-compose
```
### ⌘ MacOS
Download: https://www.docker.com/products/docker-desktop



## Clone the repository

```bash
$ mkdir -p /path/to/your/app && cd /path/to/your/app
$ git clone https://github.com/OpenCTI-Platform/docker.git
$ cd docker
```

## 3. Configure the environment

Before running the `docker-compose` command, the `docker-compose.yml` file must be configured. 

There are two ways to do that:

1. Use environment variables as it is proposed and you have an exemple in the `.env.sample` file (ie. `APP__ADMIN__EMAIL=${OPENCTI_ADMIN_EMAIL}`).
1. Directly set the parameters in the `docker-compose.yml`.

If setting within the environment, you can reference the methodology in the  [Environment setup on OpenCTI's Notion page](https://luatix.notion.site/Environment-setup-606996f36d904fcf8d434c6d0eae4a00#28b76731cae44cf0a59e70e4c84c795b
) - located below for ease:

### 🐧 Linux:

```bash
sudo apt install -y jq

cd ~/docker
(cat <<EOF
OPENCTI_ADMIN_EMAIL=admin@opencti.io
OPENCTI_ADMIN_PASSWORD=CHANGEMEPLEASE
OPENCTI_ADMIN_TOKEN=$(cat /proc/sys/kernel/random/uuid)
MINIO_ROOT_USER=$(cat /proc/sys/kernel/random/uuid)
MINIO_ROOT_PASSWORD=$(cat /proc/sys/kernel/random/uuid)
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
CONNECTOR_EXPORT_FILE_STIX_ID=$(cat /proc/sys/kernel/random/uuid)
CONNECTOR_EXPORT_FILE_CSV_ID=$(cat /proc/sys/kernel/random/uuid)
CONNECTOR_EXPORT_FILE_TXT_ID=$(cat /proc/sys/kernel/random/uuid)
CONNECTOR_IMPORT_FILE_STIX_ID=$(cat /proc/sys/kernel/random/uuid)
CONNECTOR_IMPORT_DOCUMENT_ID=$(cat /proc/sys/kernel/random/uuid)
SMTP_HOSTNAME=localhost
EOF
) > .env
```

### ⌘ MacOS
```bash
brew install jq
cd ~/docker
 (cat <<EOF
OPENCTI_ADMIN_EMAIL=admin@opencti.io
OPENCTI_ADMIN_PASSWORD=CHANGEMEPLEASE
OPENCTI_ADMIN_TOKEN=$(uuidgen)
MINIO_ROOT_USER=$(uuidgen)
MINIO_ROOT_PASSWORD=$(uuidgen)
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
CONNECTOR_EXPORT_FILE_STIX_ID=$(uuidgen)
CONNECTOR_EXPORT_FILE_CSV_ID=$(uuidgen)
CONNECTOR_EXPORT_FILE_TXT_ID=$(uuidgen)
CONNECTOR_IMPORT_FILE_STIX_ID=$(uuidgen)
CONNECTOR_IMPORT_DOCUMENT_ID=$(uuidgen)
SMTP_HOSTNAME=localhost
EOF
) > .env
```

```bash
cd ~/docker 
# trick to export the .env 
export $(cat .env | grep -v "#" | xargs)
```

## 4. Memory Management Settings

> For additional memory management information see the Memory configuration notes section

As OpenCTI has a dependency on ElasticSearch, you have to set the `vm.max_map_count` before running the containers, as mentioned in the [ElasticSearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode).

```bash
$ sudo sysctl -w vm.max_map_count=1048575
```

To make this parameter persistent, add the following to the end of your `/etc/sysctl.conf`:

```bash
$ vm.max_map_count=1048575
```

## 5. Run OpenCTI - Full-stack, including UI

### Single node Docker - *not* Docker swarm

After changing your `.env` file run `docker-compose` in detached (`-d`) mode:
```bash
$ sudo docker-compose up -d
```

### Docker swarm

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

## 6. Run OpenCTI infrastructure with UI/GraphQL in development mode

In order to develop OpenCTI UI/GraphQL in the most efficient manner we have provided a `docker-compose.dev.yml` which stands up the back-end/infrastructure of OpenCTI, with the expectation that you will run the OpenCTI front-end (React/GraphQL) separately.

This docker-compose exposes all necessary ports for the UI/GraphQL to attach to in order to support local development.

To run the services required for local development run:
```bash
$ sudo docker-compose up -f docker-compose.dev.yml -d
```

To configure/run the UI/GraphQL we would direct you to the [Notion documentation](https://luatix.notion.site/Frontend-1278fff370304cf09f6fd54ffb06f0b4)

# Appendices

## A. How to update your docker instances

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

## B. How to deploy behind a reverse proxy

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

## C. How to persist data

The default for OpenCTI data is to be persistent.

If you do not wish the data to persist:

```bash
$ mv docker-compose.override.no-persist.yml docker-compose.override.yml
```

___ 

## D. Memory configuration: additional information

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
