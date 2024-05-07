# Comprehensive Docker and Docker Swarm Setup with Portainer Management

This README provides a detailed guide to setting up Docker, Docker Swarm, and managing the environment using Portainer. It includes automated scripts for installation and configuration, making it easy to deploy and manage containerized applications across multiple hosts.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Automated Docker and Docker Swarm Setup](#automated-docker-and-docker-swarm-setup)
- [Deploying Portainer](#deploying-portainer)
- [Accessing Portainer](#accessing-portainer)
- [Managing Your Setup](#managing-your-setup)
- [Contributing](#contributing)

## Prerequisites

- One or more machines with a supported operating system (e.g., Ubuntu 18.04 or later).
- Sudo or root access on each machine.
- The scripts must be executable. You might need to set the executable permission on each script before running them.

## Automated Docker and Docker Swarm Setup

Use the provided script to install Docker on each machine and configure them into a Docker Swarm cluster. The script initializes the first machine as the manager node and joins additional machines as worker nodes.

```bash
# Make the Docker installation script executable
chmod +x install_docker

# Run the script on each machine
./install_docker

```
## Deploying Portainer
After setting up Docker and Docker Swarm, deploy Portainer to manage your Docker environment through a user-friendly web interface. Use the following script to deploy Portainer on the manager node of your Swarm:

```bash
# Make the Portainer setup script executable
chmod +x setup_portainer.sh

# Run the script on the manager node
./scripts/setup_portainer.sh
```

## Accessing Portainer
Once Portainer is deployed, you can access it by navigating to:

```bash
http://<MANAGER-IP>:9000

```

Replace <MANAGER-IP> with the IP address of your Docker Swarm's manager node. The Portainer web interface will guide you through the initial setup, including connecting to your Docker Swarm cluster.

## Managing the Setup
Here are some common management tasks you can perform with Docker CLI and Portainer:

- List Docker Swarm nodes: docker node ls
- List services running on Docker Swarm: docker service ls
- Scale a service in Docker Swarm: docker service scale <SERVICE-NAME>=<REPLICAS>
- Remove a service from Docker Swarm: docker service rm <SERVICE-NAME>
- Leave Docker Swarm: For a worker node, docker swarm leave; for a manager node, docker swarm leave --force


## OpenCTI Deployment


