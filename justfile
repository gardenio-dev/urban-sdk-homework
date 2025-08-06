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

notebooks:
    #!/usr/bin/env bash
    set -aeo pipefail
    source .env
    # Create the notebooks directory if it doesn't exist.
    mkdir -p notebooks
    pushd notebooks
    # Start the Jupyter Notebook server.
    jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# # Perform project setup steps.
# setup:
#     #!/usr/bin/env bash
#     set -aeo pipefail
#     source .env
#     # Install VS Code extensions.
#     cat .vscode/extensions.json | \
#         jq -r '.recommendations[]' | \
#         xargs -n 1 sh -c 'code --install-extension "$1"' --
#     # Install Python dependencies and the current package.
#     uv pip install -e .[dev] --system
#     pip install -e . --no-deps
#     # Set up the pre-commit hooks.
#     pre-commit install --hook-type commit-msg
#     # Since we're using pyenv, we need to rehash to make sure the new
#     # executables are available.
#     pyenv rehash

# Perform project setup steps.
setup:
    #!/usr/bin/env bash
    set -aeo pipefail
    touch .env
    source .env
    
    if [ "${DEV_CONTAINER:-0}" = "1" ]; then
        echo "Setting up development container environment..."
        
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
        
        echo "Development container setup complete!  Have fun!"
    else
        echo "Setting up local development environment..."
                
        # Create virtual environment if it doesn't exist
        if [ ! -d ".venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv .venv
        fi
        
        # Activate the virtual environment.
        source .venv/bin/activate
        
        # Upgrade pip.
        pip install --upgrade pip
        
        # Install uv if not available
        if ! command -v uv >/dev/null 2>&1; then
            echo "Installing uv..."
            pip install uv
        fi
        
        # Install Python dependencies and the current package.
        echo "Installing Python dependencies..."
        uv pip install -e .[dev]
        pip install -e . --no-deps

        # Set up the pre-commit hooks.
        pre-commit install --hook-type commit-msg
        
        echo "Local setup complete!"
        echo "To activate the virtual environment, run: source .venv/bin/activate"
        echo "Have fun!"
    fi