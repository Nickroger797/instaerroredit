# Use official Python image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy all files to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make script executable
RUN chmod +x start.sh

# Expose port for Flask
EXPOSE 8080

# Start both Flask server and bot
CMD ["./start.sh"]
