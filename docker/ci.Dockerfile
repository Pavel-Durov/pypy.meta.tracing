FROM python:2.7.18

WORKDIR /app

RUN wget https://github.com/sharkdp/hyperfine/releases/download/v1.15.0/hyperfine_1.15.0_amd64.deb
RUN dpkg -i hyperfine_1.15.0_amd64.deb

ENV PYPY_VERSION_ARTIFACT=pypy2.7-v7.3.9-src
RUN wget https://downloads.python.org/pypy/${PYPY_VERSION_ARTIFACT}.tar.bz2
RUN tar -xvf ${PYPY_VERSION_ARTIFACT}.tar.bz2 && mv ./${PYPY_VERSION_ARTIFACT} .pypy && rm ${PYPY_VERSION_ARTIFACT}.tar.bz2

RUN pip install pytest==4.6.11
RUN wget https://packagecloud.io/github/git-lfs/packages/debian/stretch/git-lfs_3.2.0_amd64.deb
RUN dpkg -i ./git-lfs_3.2.0_amd64.deb
ENV PYTHONPATH=/app:/app/.pypy/
