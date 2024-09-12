# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /ru_cococo_website

# Copy the current directory contents into the container at /ru_cococo_website
COPY . /ru_cococo_website

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait-for-it script into the container
COPY wait-for-it.sh /ru_cococo_website/wait-for-it.sh	
RUN chmod +x /ru_cococo_website/wait-for-it.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run wait-for-it script and then start flask
CMD ["./wait-for-it.sh", "db:3307", "-s", "--timeout=0", "--", "flask", "run", "--host=0.0.0.0"]
