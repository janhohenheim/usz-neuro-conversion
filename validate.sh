#!/bin/bash
set -e
poetry run python -m pynwb.validate "$1"
poetry run nwbinspector "$1"
