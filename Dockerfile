FROM python:3.10-slim

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

RUN apt-get update && \
    apt-get install -y git curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache --upgrade pip \
    && pip install --no-cache \
        notebook \
        jupyterlab \
        pyarrow \
        "git+https://github.com/ibis-project/ibis.git#egg=ibis-framework[sqlite,duckdb,clickhouse]" \
    && find /usr/local/lib/python3.10/site-packages/ -follow -type f -name '*.a' -delete \
    && find /usr/local/lib/python3.10/site-packages/ -follow -type f -name '*.pyc' -delete \
    && find /usr/local/lib/python3.10/site-packages/ -follow -type f -name '*.js.map' -delete

COPY --chown=${NB_UID} examples ${HOME}
COPY --chown=${NB_UID} tutorial ${HOME}

USER ${USER}
WORKDIR ${HOME}
