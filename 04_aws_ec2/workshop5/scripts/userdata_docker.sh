#!/bin/bash
apt update -y
apt install -y docker.io

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

mkdir -p /opt/app-site
cat << 'EOFHTML' > /opt/app-site/index.html
<h1>Servidor provisionado automáticamente con Docker</h1>
<p>EC2 + User Data + Docker Nginx Container</p>
EOFHTML

docker run -d \
  --name web-automated \
  --restart always \
  -p 80:80 \
  -v /opt/app-site:/usr/share/nginx/html:ro \
  nginx:alpine
