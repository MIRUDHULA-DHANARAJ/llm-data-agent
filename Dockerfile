# Use a lightweight official Python container runtime
FROM python:3.11-slim

# Set system environment constraints for python stability
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Establish application directory framework inside the container
WORKDIR /app

# Install system dependencies needed for compiling python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy python dependencies layout list into the work container context
COPY requirements.txt .

# Install dependencies cleanly with no cache footprint to minimize image overhead
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application script files into the execution environment 
COPY . .

# Run the mock relational database initialization setup sequence script
RUN python setup_db.py

# Expose Streamlit's operational networking gateway port
EXPOSE 8501

# Command execution pattern to launch the portal microservice on startup
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
