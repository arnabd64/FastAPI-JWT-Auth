# Pull base Debian base
# To get all the available tags
# Visit: https://hub.docker.com/_/debian
ARG TAG=bookworm
FROM debian:${TAG}

# Install ZSH
RUN apt update && \
    apt install -y git curl zsh

    
# create an user
ARG USERNAME=dev
RUN useradd -m --shell=/usr/bin/zsh ${USERNAME}
ENV USER=${USERNAME}
ENV HOME=/home/${USER}
ENV PATH=${HOME}/.local/bin:${PATH}
USER ${USER}

# Change the working directory
WORKDIR ${HOME}

# install oh my zsh
RUN zsh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh) --unattended"

ENTRYPOINT [ "zsh" ]