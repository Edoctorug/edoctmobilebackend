# Base image
FROM python:3.9-slim

# Working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the server port
EXPOSE 8000

# Command to start the server
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "patientdoctor_chat.wsgi"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "patientdoctor_chat.asgi", "-w","1","-k","uvicorn.workers.UvicornWorker"]
