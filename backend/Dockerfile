# Use a slim version of Ubuntu as base image
FROM ubuntu:lunar-20231004

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, venv, and necessary dependencies
RUN apt-get update && \
    apt-get upgrade -y python3.11 && \
    apt-get install -y \
    python3-pip \
    python3.11-venv \
    gcc \
    zlib1g \
    && apt-get remove -y libxpm4 \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and update PATH
ENV VIRTUAL_ENV=/opt/venv
RUN python3.11 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy your application files
COPY requirements.txt .
COPY app.py .
COPY bot_logic ./bot_logic
COPY app_utils ./app_utils
COPY .env .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e bot_logic
RUN python3 bot_logic/make_embeddings.py

# Set Flask environment variables
ENV FLASK_ENV=development
ENV FLASK_APP=app.py

# Add version as label
ARG CURRENT_VERSION
LABEL version=$CURRENT_VERSION

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
