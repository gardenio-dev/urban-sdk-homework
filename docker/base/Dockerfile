ARG DEBIAN_FRONTEND=noninteractive
ARG UBUNTU=24.04
FROM nvidia/cuda:12.9.0-base-ubuntu${UBUNTU} AS build
SHELL ["/bin/bash", "-c"]

# Update the distribution.
RUN apt-get update -y

# Set the locale.
RUN apt-get update && apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Install build dependencies.
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get install -yqq --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    libbz2-dev \
    libffi-dev \
    libgdbm-dev \
    liblzma-dev \
    libncurses5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm-15 \
    make \
    openssh-client \
    tk-dev \
    zlib1g-dev

# Create the non-root user.
ENV NONROOT=nonroot
ENV NONROOT_HOME=/home/${NONROOT}
RUN useradd -m -s /usr/bin/bash -d \
    "/home/${NONROOT}" -u 50000 -g 0 "${NONROOT}"

# Create the standard python path directories.
RUN mkdir -p ${NONROOT_HOME}/.pythonpath
ENV PYTHONPATH=${NONROOT_HOME}/.pythonpath

# Install pyenv and python.
ARG PYTHON=3.11.8  # TODO: Get this from .python-version
USER ${NONROOT}
WORKDIR ${NONROOT_HOME}
ENV PATH="${NONROOT_HOME}/.pyenv/bin:${PATH}"
RUN curl https://pyenv.run | bash && \
    export PATH="${NONROOT_HOME}/.pyenv/bin:${PATH}" && \
    pyenv update && \
    pyenv install ${PYTHON} && \
    pyenv global ${PYTHON} && \
    echo $(pyenv versions)
RUN echo -e '# pyenv\neval "$(pyenv init -)"' >> ${NONROOT_HOME}/.bashrc

# Copy the entrypoint script.
COPY entrypoint.sh /entrypoint

# Clean up.
USER ${NONROOT}
# RUN source venv/bin/activate && pip cache purge
USER root
RUN rm -rf ${BUILD_DIR} && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the user and work directory for when the container starts.
USER ${NONROOT}
WORKDIR ${NONROOT_HOME}
ENTRYPOINT ["/bin/bash", "/entrypoint"]