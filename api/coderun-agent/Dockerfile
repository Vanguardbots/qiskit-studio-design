# Start from the official Red Hat UBI 9 Python 3.12 image
FROM registry.access.redhat.com/ubi9/python-312

# Switch to the root user for system-level installs
USER 0

# Install build dependencies required for some Python packages.
RUN dnf install -y openssl-devel rustc cargo openblas-devel pkgconf && \
    dnf clean all

# Switch back to the default non-root user (best practice)
USER 1001

# Need to use correct pythong version
ENV PATH="/opt-app-root/bin:${PATH}"

# Set the working directory for the application.
WORKDIR /app

# Install UV
RUN /opt/app-root/bin/python3 -m pip install uv

# Dependencies
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --python /opt/app-root/bin/python3 .

# Copy app 
COPY agent.py .
COPY log_conf.yml .

# server port.
EXPOSE 8000

# Launch server
CMD ["uvicorn", "agent:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "log_conf.yml"]
