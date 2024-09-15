# Official Python image from the Docker Hub
FROM python:3.12.3

# Set unbuffered output for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Copy the requirements file from your host machine to the working directory
COPY requirements.txt ./

# Install app dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Bundle app source
COPY . .

# Expose port
EXPOSE 8000

# entrypoint to run the django.sh file
ENTRYPOINT ["/app/django.sh"]