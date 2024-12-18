FROM python:3.10-slim AS builder 

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app/


FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

RUN export PYTHONPAHT=.

EXPOSE 3000

CMD [ "python", "app/main.py" ]