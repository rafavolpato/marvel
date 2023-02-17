# Use the official Python image as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'default@email.com', 'password')" | python manage.py shell
RUN python manage.py load_characters

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run script.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
