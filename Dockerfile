FROM python:latest

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
RUN apt-get update -y
RUN apt-get install -y \
    libnss3-tools \
    curl

# Install mkcert
RUN ARCH=$(uname -m) && \
    case "$ARCH" in \
    x86_64) ARCH="amd64";; \
    aarch64) ARCH="arm64";; \
    *) echo "Unsupported architecture: $ARCH" && exit 1;; \
    esac && \
    curl -L -o /usr/local/bin/mkcert https://dl.filippo.io/mkcert/latest?for=$(uname -s)/${ARCH} && \
    chmod +x /usr/local/bin/mkcert

# Generate certificates and install local CA
RUN mkcert -install
RUN mkcert -key-file key.pem -cert-file cert.pem test.local *.test.local 127.0.0.1 ::1 localhost

# Clean up
RUN apt-get remove -y curl
RUN apt-get autoremove -y && apt-get clean

# Install Python dependencies
COPY requirements-tests.txt .
RUN pip install -r requirements-tests.txt

# Copy the application code
COPY ./setup.py .
COPY ./README.md .
COPY ./httpx_system_certs.pth .
COPY ./httpx_system_certs ./httpx_system_certs/
COPY ./tests ./tests/

# Install httpx-system-certs
RUN pip install .

# Run tests
CMD ["pytest", "-v", "-x", "--pdb", "./tests/httpx_system_certs_tests.py"]