FROM python:3.9-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends 

WORKDIR /app

# Install our requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
COPY . .

# Make port 8090 available for links and/or publish
EXPOSE 8090

# Define our command to be run when launching the container
CMD ["/app/server.py"]
ENTRYPOINT ["python3"]
