<p align="center">
   <a href="https://github.com/Geo-Comm/airflow-provider-io">
    <img src="../../docs/source/_static/logo.svg" alt="Logo" height="80">
  </a>
</p>
<h1 align="center">
  io-baseimage
</h1>
  <h3 align="center">
  Build the base <a href="https://www.docker.com/">Docker</a> image for IO.
</h3>

<br/>

This is the base [Docker](https://www.docker.com/) image for IO.  It is built
on [Ubuntu](https://ubuntu.com/) and includes:

* [pyenv](https://github.com/pyenv/pyenv)
* [GDAL](https://gdal.org/)


## Getting Started

To get a local copy of the repository and bootstrap the environment, run:

```shell
git clone git@github.com:Geo-Comm/io-baseimage.git && \
  cd ./io-baseimage && \
  ./scripts/bootstrap.sh
```

## Building the Image

To build the image, run:

```shell
just build
```

## Running the Image

The project includes a simple
[Docker Compose](https://docs.docker.com/compose/) file (`docker-compose.yml`)
that you can use to run the image.

While you can run `docker compose` directly, the `just` file includes a
recipie that sets up the environment before bringing up the container.

To run the image with Docker Compose, run:

```shell
just up
````


## Development

### just

The project includes a [just](https://github.com/casey/just) file to simplify
common tasks.  To see the available commands, run:

```shell
just --list
```

### Modifying the Image

As with any Docker image, the
[Dockerfile](https://docs.docker.com/reference/dockerfile/) is the source of
truth.  You can modify this file directly, but if you just need to modify
the versions of components, you can do so in the `build.env` file.
