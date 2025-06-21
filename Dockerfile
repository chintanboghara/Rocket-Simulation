FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV FONTCONFIG_PATH=/tmp/fontconfig
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Create necessary directories
RUN mkdir -p /tmp/matplotlib /tmp/fontconfig results static templates && \
    chmod 777 /tmp/matplotlib /tmp/fontconfig

# Expose port for web interface
EXPOSE 5000

# Default command (can be overridden)
CMD ["python", "app.py"]