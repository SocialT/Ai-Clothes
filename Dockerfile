# Dockerfile for FastAPI + Prisma + Supabase

FROM python:3.12

WORKDIR /app

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy application code
COPY main.py /app/main.py
COPY core /app/core
COPY prisma /app/prisma

# Generate Prisma client
RUN prisma generate

EXPOSE 3000

# Add entrypoint to run migrations, then start the app
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Run the application via entrypoint (accepts extra args)
CMD ["/app/docker-entrypoint.sh", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
