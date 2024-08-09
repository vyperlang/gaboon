from argparse import Namespace
import os
import tomli_w
import subprocess
import re
from gaboon.config import Config, get_config, initialize_global_config
from gaboon._dependency_helpers import get_base_install_path, freeze_dependencies
from gaboon.constants.vars import (
    REQUEST_HEADERS,
    PACKAGE_VERSION_FILE,
    DEPENDENCIES_FOLDER,
)
from pathlib import Path
from base64 import b64encode
import requests
from tqdm import tqdm
import shutil
import zipfile
from io import BytesIO
from gaboon.logging import logger
from urllib.parse import quote
import tomllib


def main(args: Namespace):
    if args.package_name is None:
        _install_dependencies()
    else:
        _pip_install(args.package_name, args.verbose)


def _install_dependencies():
    config = get_config()
    dependencies = config.get_dependencies()
    for package_id in dependencies:
        _pip_install(package_id)


def _pip_install(package_id: str, verbose: bool = False) -> str:
    path = get_base_install_path()

    # TODO: Allow for multiple versions of the same package to be installed
    cmd = ["uv", "pip", "install", package_id, "--target", str(path)]

    # TODO: report which version of the package has been installed
    # TODO: `--upgrade` and `--force` options.
    capture_output = not verbose
    subprocess.run(cmd, capture_output=capture_output, check=True)

    freeze_dependencies()
