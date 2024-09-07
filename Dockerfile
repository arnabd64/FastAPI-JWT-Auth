# STEP 1: Pull base image from docker hub
# for all available tags
# visit: https://hub.docker.com/_/python
ARG TAG=3.11-slim-python
FROM python:${TAG}

# STEP 2: install python dependencies
ENV REQ=/tmp/requirements.txt
COPY requirements.txt ${REQ}
RUN python3 -m pip install --progress-bar off -r ${REQ}

# STEP 3: create an user
ARG USER=admin
RUN useradd -m ${USER}

# set the environment variables
ENV USERNAME=${USER}
ENV HOME=/home/${USER}
ENV PATH=${HOME}/.local/bin:${PATH}
# switch user
USER ${USERNAME}

# copy source code
WORKDIR ${HOME}/app
COPY --chown=${USERNAME} . .

# run the application
EXPOSE ${PORT}
CMD ["python", "main.py"]
