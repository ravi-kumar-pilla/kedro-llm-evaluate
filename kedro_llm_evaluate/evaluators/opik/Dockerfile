FROM python:3.10-slim

# Install Git (and any other OS deps)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       git \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Clone the Opik repo
RUN git clone https://github.com/comet-ml/opik.git /opt/opik

# Make the opik.sh script executable
RUN chmod +x /opt/opik/opik.sh

# Expose the Opik port
EXPOSE 5173

WORKDIR /opt/opik

# Launch Opik on container start
ENTRYPOINT ["./opik.sh"]