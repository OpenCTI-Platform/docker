
### Docker swarm setup

The guide below highlights the steps to deploy the OpenCTI services using a Swarm stack.

### Prerequisites

Download and install Docker as described in [Get Docker](https://docs.docker.com/get-docker/)

### Node Labels



### Swarm Configuration

Hosts that participate in the same Docker swarm should be able to connect **to each other** using the [following protocols and ports](https://docs.docker.com/engine/swarm/swarm-tutorial/#open-protocols-and-ports-between-the-hosts):

* TCP:
  * 2376
  * 2377
  * 7946
* UDP:
  * 4789
  * 7946
* ESP (IP protocol 50)

### Deploying with Portainer

#### Deploy Portainer itself

To be able to manage applications running on Docker Swarm using Portainer's web UI, you have to deploy Portainer itself.

To deploy Portainer:

1. Copy `docker-compose.portainer.yml` to the swarm managers.

2. Deploy the Portainer's stack in the swarm:

   ```bash
   docker stack deploy -c docker-compose.portainer.yml portainer
   ```

3. Assuming that you have SSH port forwarding set up as per example below, you should be able to connect to Portainer's web UI by opening the following URL:

   <http://localhost:9000/>

   and logging in with the following credentials:

   * username: `admin`
   * password: `temppassword`

#### Deploy CFA Open CTI using Portainer

To deploy CfA's Open CTI services using Portainer's web UI:

1. Go to Portainer's web UI, select the `primary` endpoint, open a list of *Stacks* in the menu on the left, and click on *Add stack*;
2. Name the stack `cfa-opencti`, and either:
   * paste the contents of production's `docker-compose.yml` in the *Web editor* section, or
   * upload the prepared `docker-compose.yml` from your computer in the *Upload* section, or
   * make Portainer read production's `docker-compose.yml` from a private, authenticated Git repository in the *Repository* section;
3. Set any *Environment variables* as defined in the `docker-compose.yml`
4. Click *Deploy the stack* and wait for the stack to deploy.

#### Portainer's tips and gochas

* To update a running stack with a newer production `docker-compose.yml`, open the *Editor* tab in the `cfa-opencti` stack page, update the Compose configuration, and click *Update the stack*;
* Feel free to use Portainer's features to scale the services, update their configuration via environment variables, update resource limits, etc., using the web UI, just make sure to reflect the changes that you've made in the private authenticated Git repository with production `docker-compose.yml`.

### Deploying manually

To deploy services, change the current directory to the one with production's `docker-compose.yml` and then run:

```bash
docker stack deploy -c docker-compose.yml cfa-opencti
```

To update services (e.g. after updating configuration in `docker-compose.yml` or pushing new container images), run the same command again.

To stop all services by stopping and removing all the containers, run:

```bash
docker stack rm cfa-opencti
```