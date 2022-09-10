FROM python:2.7.18

WORKDIR /app

COPY . .

RUN hg clone https://foss.heptapod.net/pypy/pypy .pypy	

RUN pip install flake8
RUN pip install pytest==4.6.11
RUN pip install flake8

ENV PYTHONPATH=/app:/app/.pypy/

ENTRYPOINT ["pytest", "./test"]
