#!/bin/bash

# Install Python (if not already installed)
brew install python3.10

# Install virtualenv (if not already installed)
pip install virtualenv

# Create a virtual environment
virtualenv -p python3.10 venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
