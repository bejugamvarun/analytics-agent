#!/bin/bash

# Navigate to the root project directory
cd "$(dirname "$0")/../.." || exit 1

uv sync
