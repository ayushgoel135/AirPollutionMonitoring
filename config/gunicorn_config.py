# Render-specific settings
bind = "0.0.0.0:10000"
workers = 1  # Only 1 worker for free tier
threads = 2  # Lightweight concurrency
timeout = 30
keepalive = 5
max_requests = 100  # Restart workers frequently
preload_app = True  # Critical for memory