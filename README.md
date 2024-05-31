# Torminal

## Overview

This project aims to reduce friction in setting up a Tor relay using Docker and managing with Nyx. 

Make sure to edit any data marked "<<like-this>>"

Don't Forget you will need to open port 9001 on your firewall

Docker install docs [here](https://docs.docker.com/engine/install/)

# Quick-Start

```bash
git clone https://github.com/Wytchwulf/Torminal/
cd Torminal
```
```python
"""
Edit Torminal.sh with your name and email
"""
```

```bash
chmod +x Torminal.sh
```

```bash
./Torminal.sh
```
# Alt: Manual - Copy-Paste method.

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
  ```

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
  ```

## Bring it all together

- Build Image
  ```bash
  docker build -t tor-relay .
  ```

- Run Container
  ```bash
  docker run -d --name my-tor-relay -p 9001:9001 -p 9051:9051 -p 9050:9050 --restart always tor-relay
  ```

- Monitor Logs
  ```bash
  docker exec -it my-tor-relay nyx
  ```
    
