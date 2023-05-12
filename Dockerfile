FROM python:3.11.3

WORKDIR /app

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

ENTRYPOINT ["python", "-m", "gunicorn", "-b", "0.0.0.0:8000", "schoolTime.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]