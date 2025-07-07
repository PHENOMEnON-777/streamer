
FROM python:3.11


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./core /code/core
COPY ./streamerapp /code/streamerapp


CMD ["uvicorn", "streamerapp.main:app", "--host", "0.0.0.0", "--port", "80"]