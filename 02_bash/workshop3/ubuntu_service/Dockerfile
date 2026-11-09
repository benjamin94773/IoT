FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    grep \
    gawk \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY monitor.sh /app/monitor.sh
COPY analiza.sh /app/analiza.sh

RUN chmod +x /app/monitor.sh /app/analiza.sh

CMD ["bash"]