FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV API_BASE_URL=https://petstore3.swagger.io/api/v3
ENV PYTHONPATH=/app:/app/src
CMD ["pytest", "--alluredir=allure-results"]
