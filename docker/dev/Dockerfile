ARG DEBIAN_FRONTEND=noninteractive
ARG BASE=ubuntu:latest
ARG PROJECT=urban-sdk-homework
FROM ${BASE} AS build
SHELL ["/bin/bash", "-c"]

USER root
# Update the distribution.
RUN apt-get update -y

# Install dev dependencies.
RUN DEBIAN_FRONTEND=noninteractive && apt-get install -y \
    curl \
    jq \
    sudo \
    vim

# Configure sudo for the non-root user.
RUN usermod -aG sudo ${NONROOT} && \
    echo "${NONROOT} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/${NONROOT} && \
    chmod 0440 /etc/sudoers.d/${NONROOT}

# Install development tools.
USER ${NONROOT}
# Install just.
RUN mkdir -p ${NONROOT_HOME}/bin
ENV PATH="~/bin:$PATH"
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | \
    bash -s -- --to ~/bin
# Install uv.
RUN eval "$(pyenv init -)" && \
    pip install pip --upgrade && \
    pip install uv

# Prepare the project directory.
USER ${NONROOT}
ENV PROJECT=${PROJECT}
ENV PROJECT_HOME=${NONROOT_HOME}/${PROJECT}
RUN mkdir -p ${PROJECT_HOME}
WORKDIR ${NONROOT_HOME}
