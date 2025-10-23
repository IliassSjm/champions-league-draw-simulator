# Champions League Draw Simulator - Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY champions_league_draw.py .
COPY statistics.py .
COPY export_json.py .
COPY demo.py .
COPY test_draw.py .
COPY draw_visualizer.html .
COPY web_interface.html .
COPY requirements.txt .

# Create a non-root user
RUN useradd -m -u 1000 ucl && chown -R ucl:ucl /app
USER ucl

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Default command
CMD ["python3", "champions_league_draw.py"]

# Labels
LABEL maintainer="iliass.sjm@icloud.com"
LABEL description="UEFA Champions League Draw Simulator"
LABEL version="1.0.0"

