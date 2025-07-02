FROM python

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "uvicorn", "api_rate_limiter.app.main:app","--host", "0.0.0.0", "--port", "8000", "--reload"]