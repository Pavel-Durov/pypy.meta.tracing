# TODO: Complete docker file!
FROM python:2.7.18

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYPYLOG=jit-log-opt:logfile 
ENV PYTHONPATH=${PWD}/pypy/

RUN python ${PWD}/pypy/rpython/translator/goal/translate.py --opt=jit ${PWD}/tutorial.py

ENTRYPOINT [ "*-c", "example_programs/99bottles.b" ]
