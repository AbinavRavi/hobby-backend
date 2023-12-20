FROM python:3.11-slim

COPY . .

RUN pip install poetry 

RUN poetry install --no-dev

CMD ["poetry","run","uvicorn", "data_hub.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000