#!/bin/bash

# Activate the virtual environment
. $(poetry env info --path)/bin/activate

# Run the command
exec "$@"