# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /decode_

# Copy the current directory contents into the container at /zero_
COPY . /decode_

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "decoding_the_roads.main:app", "--host", "0.0.0.0", "--port", "8080"]