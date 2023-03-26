FROM python:3.9

WORKDIR /code

COPY ./ /code/

RUN adduser --system --no-create-home nonroot

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

USER nonroot

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
