# Production Deployment

This document describes how to run the rental listing monitor in production using Docker Compose and `systemd`. The steps assume a Linux host with Docker and Docker Compose installed and a domain configured for TLS.

## 1. Environment Setup

1. Copy `.env.example` to `.env` and fill in your API keys and database credentials.
2. Ensure ports 80 and 443 are open if you plan to serve the HTTP API through a reverse proxy.

## 2. Docker Compose

A sample `docker-compose.yml` is provided below. It builds the application image and runs the scheduler.

```yaml
version: '3'
services:
  rentbot:
    build: .
    env_file: .env
    command: poetry run rentbot run-once
    volumes:
      - ./data:/data
```

Start the container with:

```bash
docker compose up -d
```

## 3. systemd Service

For a lightweight deployment without Docker, you can run the scheduler directly under `systemd`. Create `/etc/systemd/system/rentbot.service`:

```ini
[Unit]
Description=SpiceflowNesting scheduler
After=network.target

[Service]
WorkingDirectory=/opt/spiceflownesting
EnvironmentFile=/opt/spiceflownesting/.env
ExecStart=/usr/bin/poetry run rentbot run-once
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Reload systemd and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now rentbot
```

## 4. TLS Termination

Use a reverse proxy such as Nginx with Let's Encrypt to terminate TLS. Point the proxy at the container or service on port 80/443. Certbot can automatically renew certificates:

```bash
sudo certbot --nginx -d yourdomain.com
```

## 5. Release Tagging

After merging these instructions to `main`, create a git tag and push it to mark the `v1.0` release:

```bash
git tag v1.0
git push origin v1.0
```

