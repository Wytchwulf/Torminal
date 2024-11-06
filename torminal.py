import docker
import os
import argparse

def create_dockerfile_tor():
    dockerfile_tor = """
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
"""
    with open('Dockerfile.tor', 'w') as f:
        f.write(dockerfile_tor)

def create_torrc(your_name, your_email, nickname):
    torrc_content = f"""
DataDirectory /var/lib/tor

Nickname {nickname}

ORPort 9001
ORPort [::]:9001

ExitRelay 0
ExitPolicy reject *:*

RelayBandwidthRate 1024 KBytes
RelayBandwidthBurst 2048 KBytes

NumEntryGuards 3

ControlPort 9051
CookieAuthentication 1

ContactInfo {your_name} {your_email}
"""
    with open('torrc', 'w') as f:
        f.write(torrc_content)

def create_dockerfile_snowflake():
    dockerfile_snowflake = """
FROM alpine:latest

RUN apk add --no-cache tor snowflake

EXPOSE 3478
EXPOSE 9002

CMD ["tor", "-f", "/etc/tor/torrc-snowflake"]
"""
    with open('Dockerfile.snowflake', 'w') as f:
        f.write(dockerfile_snowflake)

def build_and_run_containers(tor_data_directory):
    client = docker.from_env()

    # Build Tor image
    client.images.build(path=".", dockerfile="Dockerfile.tor", tag="tor-relay")

    # Run Tor container with persistent storage
    client.containers.run(
        "tor-relay",
        name="my-tor-relay",
        ports={
            "9001/tcp": ("::", 9001),       # IPv6
            "9001/tcp": ("0.0.0.0", 9001),  # IPv4
            "9051/tcp": 9051,
            "9050/tcp": 9050
        },
        volumes={
            os.path.abspath(tor_data_directory): {'bind': '/var/lib/tor', 'mode': 'rw'}
        },
        restart_policy={"Name": "always"},
        detach=True
    )

    # Build Snowflake image
    client.images.build(path=".", dockerfile="Dockerfile.snowflake", tag="snowflake-proxy")

    # Run Snowflake container
    client.containers.run(
        "snowflake-proxy",
        name="my-snowflake-proxy",
        ports={
            "3478/tcp": ("::", 3478),
            "3478/tcp": ("0.0.0.0", 3478),
            "9002/tcp": ("::", 9002),
            "9002/tcp": ("0.0.0.0", 9002)
        },
        restart_policy={"Name": "always"},
        detach=True
    )

def main():
    parser = argparse.ArgumentParser(description="Build and run Tor relay and Snowflake proxy containers.")
    parser.add_argument("--name", required=True, help="Your name")
    parser.add_argument("--email", required=True, help="Your email address")
    parser.add_argument("--nickname", required=True, help="Relay nickname")
    parser.add_argument("--tor-data-directory", required=True, help="Directory for Tor persistent data")

    args = parser.parse_args()

    # Create necessary files
    create_dockerfile_tor()
    create_torrc(args.name, args.email, args.nickname)
    create_dockerfile_snowflake()

    # Build and run the containers
    build_and_run_containers(args.tor_data_directory)

if __name__ == "__main__":
    main()
