# Setup FREE automatic HTTPS for OpenCTI instance
Setup and automate FREE valid SSL for OpenCTI, using an OpenSource project called [Caddy Server](https://caddyserver.com/) with very minimal effort.

## About Caddy
Caddy 2 is a powerful, enterprise-ready, open source web server with **automatic HTTPS** written in Go. Caddy works well as a direct install and also using Docker.

### Using Docker
OpenCTI runs all its components in individual containers. For accessing the WebUI, by default it exposes opencti service on port 8080 locally.   

Its easy to setup reverse proxy with FREE SSL using Caddy with very minimal effort. So lets check the steps for setting it up  
- Configure DNS with A record pointing to your OpenCTI public IP address  
- Create a base folder for config file 'Caddyfile'
- Create a docker-compose file for Caddy
- Create a container using docker-compose run 


```bash
# Create a DNS A/AAAA record pointing your domain to the public IP address
cti.domain.com  A  <public-IP-address-for-OpenCTI-instance>
```
Make sure to wait for the DNS record to complete propagation (depending on TTL). Otherwise automatic SSL creation would not work.  

Caddy uses 2 volumes for data (storing certificates etc) & config.  
Create a file called 'Caddyfile' in the local folder for configuration, which will be mapped to /etc/caddy/Caddyfile through docker-compose file as below.
#### Content of configuration file called 'Caddyfile' 
```
cti.domain.com {
	reverse_proxy http://opencti:8080
}
```

#### docker-compose-caddy.yml file content below
```yaml
version: "3.7"
services:
  caddy:
    image: caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config

networks:
  default:
    external: true
    name: <your OpenCTI network name>
    
volumes:
  caddy_data:
  caddy_config:
```

Since you are running Caddy in docker, you need to make it part of OpenCTI network and don't need to expose OpenCTI 8080 port outside.
This means you can remove port setting in OpenCTI docker-compose file.

Now just get it running and Caddy will request and get SSL certificate automagically for your domain.  
> docker run -f docker-compose-caddy.yml up -d

### Resources
How Caddy automatic SSL works  
https://caddyserver.com/docs/automatic-https

Using Caddy with Load Balancer  
https://caddy.community/t/load-balancing-caddy/10467
