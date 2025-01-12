FROM python:3.12.8-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN prisma generate --schema=./src/app/Prisma/schema.prisma
EXPOSE 8000
CMD [ "python", "main.py" ]