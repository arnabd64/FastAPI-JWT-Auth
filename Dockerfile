# STEP 1: Pull base image from docker hub
# for all available tags
# visit: https://hub.docker.com/_/python
ARG TAG=3.11-slim-python
FROM python:${TAG}

# STEP 2: install python dependencies
COPY requirements.txt .
RUN python3 -m pip install --progress-bar off -r requirements.txt

# STEP 3: create an user
ARG USER=admin
RUN useradd -m ${USERNAME}
# set the environment variables
ENV USERNAME=${USER}
ENV HOME=/home/{USERNAME}
ENV PATH=${HOME}/.local/bin:${PATH}
# switch user
USER ${USERNAME}

# copy source code
WORKDIR ${HOME}/app
COPY --chown=${USERNAME} . .

# run the application
EXPOSE ${PORT}
CMD ["python", "main.py"]
