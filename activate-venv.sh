#!/bin/bash

# Check if the .venv directory exists
if [ ! -d ".venv" ]; then
    # Create a virtual environment if it does not exist
    python3 -m venv .venv
    echo "Virtual environment '.venv' created."
fi

# Activate the virtual environment
source .venv/bin/activate

# Open a new shell in the activated environment
exec "$SHELL"
