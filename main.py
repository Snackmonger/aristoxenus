#!/usr/bin/env python3
"""
Entrypoint for the Aristoxenus library's command-line interface, which exposes
a few of the features provided by the library.
"""

# pylint: disable=no-value-for-parameter
from cli.app import aristoxenus


if __name__ == "__main__":
    aristoxenus()
