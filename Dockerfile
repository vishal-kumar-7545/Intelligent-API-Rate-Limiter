FROM python

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "uvicorn", "api_rate_limiter.app.main:app", "--port", "8000", "--reload"]