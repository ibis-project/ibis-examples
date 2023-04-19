FROM python:3.10

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
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt \
    && find /usr/local/lib/python3.10/site-packages/ -follow -type f -name '*.js.map' -delete

COPY --chown=${NB_UID} examples ${HOME}/examples
COPY --chown=${NB_UID} tutorial ${HOME}/tutorial
COPY --chown=${NB_UID} welcome.md ${HOME}/welcome.md
COPY --chown=${NB_UID} binder.jupyterlab-workspace ${HOME}/.jupyter/lab/workspaces/default-37a8.jupyterlab-workspace

USER ${USER}
WORKDIR ${HOME}
