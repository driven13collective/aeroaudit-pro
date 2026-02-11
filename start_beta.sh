#!/bin/bash
# Install any missing F1-specific AI tools
pip install ultralytics

# Start the Reflex app in production mode
# --env prod removes the 'debug' lag for your testers
reflex run --env prod --frontend-port 3000 --backend-port 8000
