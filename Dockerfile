# FROM python:3.12-slim-bookworm

# WORKDIR /app

# COPY requirements.txt .
# RUN python -m pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 5000

# CMD ["python", "app.py"]


FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
