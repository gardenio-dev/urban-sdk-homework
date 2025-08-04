set shell := ["bash", "-uc"]
set dotenv-load

# Start the development container.
dev:
    #!/usr/bin/env bash
    set -a
    source .env
    pushd docker/base
    just build
    popd
    pushd docker/dev
    just build
    just up

# Kill the process using a port.
killport port:
    #!/usr/bin/env bash
    echo Attemping to kill the app listening on port {{port}}.
    kill -9 $(sudo lsof -t -i:{{port}})

# Run the pre-commit hooks.
pre-commit:
    #!/usr/bin/env bash
    pre-commit run --all-files

# Perform project setup steps.
setup:
    #!/usr/bin/env bash
    set -aeo pipefail
    source .env
    # Install VS Code extensions.
    cat .vscode/extensions.json | \
        jq -r '.recommendations[]' | \
        xargs -n 1 sh -c 'code --install-extension "$1"' --  
    # Install Python dependencies and the current package.
    uv pip install -e .[dev] --system
    pip install -e . --no-deps
    # Set up the pre-commit hooks.
    pre-commit install --hook-type commit-msg
    # Since we're using pyenv, we need to rehash to make sure the new 
    # executables are available.
    pyenv rehash
