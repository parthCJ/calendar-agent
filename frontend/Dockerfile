# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
# Path is now relative to the project root
COPY frontend/requirements.txt ./

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app code to the container
# Path is now relative to the project root
COPY frontend/streamlit_app.py ./

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable for the streamlit server
ENV STREAMLIT_SERVER_PORT 8501
ENV STREAMLIT_SERVER_HEADLESS true

# Run streamlit_app.py when the container launches
CMD ["streamlit", "run", "streamlit_app.py"]