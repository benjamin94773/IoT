#!/bin/bash
apt update -y
apt install -y nginx

systemctl enable nginx
systemctl start nginx

cat > /var/www/html/index.html <<'EOFHTML'
<h1>Servidor provisionado automáticamente</h1>
<p>EC2 + User Data</p>
EOFHTML
