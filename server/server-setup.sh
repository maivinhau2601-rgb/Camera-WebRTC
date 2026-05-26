#!/bin/bash

sudo apt update && sudo apt install -y python3-venv

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Only real pip packages here
packages=("flask")

for pkg in "${packages[@]}"
do
    if python -c "import flask" >/dev/null 2>&1; then
        echo "$pkg OK"
    else
        echo "$pkg missing"
        echo "Installing $pkg..."
        pip install "$pkg"
    fi
done
