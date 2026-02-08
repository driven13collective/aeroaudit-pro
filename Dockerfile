FROM python:3.11-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
	libgl1-mesa-glx libglib2.0-0 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python requirements
RUN pip install -r requirements.txt
RUN pip install reflex

# Initialize and Export
RUN reflex init
RUN reflex export --frontend-only --no-zip

# Run the app
CMD ["reflex", "run", "--env", "prod"]
