# Please Read
This is a simple healthcheck container that will fetch the endpoint and flag itself with Healthy after all endpoints are healthy

## Available Container Environments
- WORKER -> workers amount to fetch the endpoints default is 4
- SHOW_LOG -> disable show log .... 
  - note that it will affect the memory consumption as Flask will still run
  - override the container command to ==CMD ["tail", "-f", "/dev/null"]== instead if you don't want to run flask
- TARGET_DIR -> You might never need to change this at all

## To override the healthcheck config, define this in the compose service
```
healthcheck:
    test: ["CMD", "python3", "check.py"]
    interval: 5s
    timeout: 20s
    start_period: 5s
    retries: 3
```

## Notes that the performance is expected to be bad
- There is also Flask process that will run to show healthcheck log in container log
- It is written in python
- The base image is not minimal