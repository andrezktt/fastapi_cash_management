FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock* ./

RUN uv pip compile pyproject.toml -o requirements.txt

RUN uv pip sync --system requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/ /usr/local/

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]