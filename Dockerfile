# Using the python 3.9.0 base image
FROM python:3.9.0

# Set the working directory inside the container
WORKDIR /workspace

# Copy files into the container
COPY tracking_application ./tracking_application
COPY requirements.txt /workspace/

# Update apt-get and install dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    xauth \
    vlc \
    && apt-get clean && rm -rf /var/lib/apt/lists/* 

# Install Python dependencies
RUN pip install -r requirements.txt

# Set the working directory to tracking_application
WORKDIR /workspace/tracking_application

# Make the tracking scripts executable
RUN chmod +x scripts/tracking_livecam.sh
RUN chmod +x scripts/tracking_240p.sh
RUN chmod +x scripts/tracking_360p.sh
RUN chmod +x scripts/tracking_480p.sh
RUN chmod +x scripts/tracking_720p.sh

# Keep the container running indefinitely
CMD ["tail", "-f", "/dev/null"]
