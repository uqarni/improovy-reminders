import os
import redis
import platform
import openai 
from main import improovy_reminder

# Connect to Redis server
redis_host = os.environ.get("REDIS_1_HOST")
redis_port = 25061
redis_password = os.environ.get("REDIS_1_PASSWORD")

operating_system = platform.system()

# Set the CA certificates file path based on the operating system
if operating_system == 'Linux':
    ssl_ca_certs = "/etc/ssl/certs/ca-certificates.crt"
elif operating_system == 'Darwin':  # macOS
    ssl_ca_certs = "/etc/ssl/cert.pem"  # Update to macOS path
else:
    raise ValueError(f"Unsupported operating system: {operating_system}")

rd = redis.Redis(host=redis_host, port=redis_port, password=redis_password, ssl=True, ssl_ca_certs=ssl_ca_certs)


# improovy_reminder()

