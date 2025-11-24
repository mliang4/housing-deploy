# Use Python 3.11 as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file
COPY ./requirements.txt /code/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app folder into the container
COPY ./src /code/src

# Train the model during the build process to ensure reproducibility
# This removes the dependency on a locally trained 'models' directory
RUN python src/train.py

# Expose port 80 for FastAPI
EXPOSE 80

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "80"]