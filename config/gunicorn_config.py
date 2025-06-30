# gunicorn_config.py
import multiprocessing

# Bind to Render's internal port (10000)
bind = "0.0.0.0:10000"

# Worker settings (optimized for Render free tier)
workers = 1                   # Reduce workers to avoid OOM errors
threads = 2                   # Use threads for concurrency
timeout = 30                  # Kill workers after 30s of inactivity
keepalive = 5                 # Keep-alive connections
max_requests = 500            # Restart workers after 500 requests
max_requests_jitter = 50      # Randomize worker recycling
preload_app = True            # Load app before forking (saves memory)