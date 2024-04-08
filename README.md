# Docker-Tor

## Overview

Just some simple config files for running a Tor relay using Docker and managing with Nyx. 

This is as plug and play as I can make it.

copy/paste below being sure to edit any data marked <<like-this>>

Docker install docs [here](https://docs.docker.com/engine/install/)

## Dockerfile

- sudo vim Dockerfile
  ```yaml
  FROM debian:buster-slim

  RUN apt-get update && \
      apt-get install -y --no-install-recommends apt-transport-https gnupg2 curl ca-certificates && \
      apt-get clean && \
      rm -rf /var/lib/apt/lists/*
  
  RUN echo 'deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org buster main' > /etc/apt/sources.list.d/tor.list && \
      echo 'deb-src [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org buster main' >> /etc/apt/sources.list.d/tor.list && \
      curl -s https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/tor-archive-keyring.gpg >/dev/null
  
  RUN apt-get update && \
      apt-get install -y tor deb.torproject.org-keyring nyx haveged && \
      apt-get clean && \
      rm -rf /var/lib/apt/lists/*
  
  RUN mkdir -p /var/lib/tor && \
      chown -R debian-tor:debian-tor /var/lib/tor
  
  COPY torrc /etc/tor/torrc
  
  EXPOSE 9001
  EXPOSE 9051
  EXPOSE 9050
  
  USER debian-tor
  
  CMD ["tor", "-f", "/etc/tor/torrc"]

## torrc

- sudo vim torrc
  ```yaml
  DataDirectory /var/lib/tor

  ORPort 9001
  ExitPolicy reject *:* # Reject all exit traffic
  
  RelayBandwidthRate 1024 KBytes
  RelayBandwidthBurst 2048 KBytes
  
  NumEntryGuards 3
  
  ControlPort 9051
  CookieAuthentication 1
  
  ContactInfo <<YOUR_NAME>> <<YOUR_EMAIL>>

## Bring it all together

- Build Image
  ```bash
  docker build -t tor-relay .

- Run Container
  ```bash
  docker run -d --name my-tor-relay -p 9001:9001 -p 9051:9051 -p 9050:9050 tor-relay

- Monitor Logs
  ```bash
  docker exec -it my-tor-relay nyx
    
