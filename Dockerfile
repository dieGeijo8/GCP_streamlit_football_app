# Use the official Python image
FROM python:latest

# Expose Streamlit port
EXPOSE 8080

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the streamlit app on port 8080, listen to all available network interfaces not only local host
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

# docker build -t image_name .
# docker run -d -p 8080:8080 --name container_name image_name