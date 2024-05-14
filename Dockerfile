
FROM python:3.9-slim


RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir -r requirements.txt

# Ensure the nodes directory is in the PYTHONPATH
ENV PYTHONPATH="/app/nodes:${PYTHONPATH}"


EXPOSE 5000
EXPOSE 5001
EXPOSE 50051
EXPOSE 50052
EXPOSE 50053


ENTRYPOINT ["sh", "/app/start.sh"]
