ARG TAG=3.11-slim-python
FROM python:${TAG}

COPY requirements.txt .
RUN python3 -m pip install --progress-bar off -r requirements.txt

ARG USER=admin
ENV USERNAME=${USER}
ENV HOME=/home/{USERNAME}
ENV PATH=${HOME}/.local/bin:${PATH}
RUN useradd -m ${USERNAME}
USER ${USERNAME}

WORKDIR ${HOME}/app
COPY --chown=${USERNAME} . .

EXPOSE ${PORT}
CMD ["python", "main.py"]