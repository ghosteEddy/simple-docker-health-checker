FROM python:3.13-slim

RUN pip install requests
RUN pip install flask

WORKDIR /checker
COPY check.py /checker/check.py
COPY app.py /checker/app.py

# Healthcheck that runs your Python script
HEALTHCHECK --interval=10s --timeout=30s --start-period=10s --retries=5 CMD [ "python3", "check.py" ]

# Start a dummy command to keep the container running
CMD ["python3", "app.py"]

