# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=myproject.settings

CMD ["python", "manage.py", "makemigrations"]

CMD ["python", "manage.py", "migrate"]

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]