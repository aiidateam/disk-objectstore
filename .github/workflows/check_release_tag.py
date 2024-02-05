"""Check that the GitHub release tag matches the package version."""

import argparse
import pathlib
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("GITHUB_REF", help="The GITHUB_REF environmental variable")
    parser.add_argument("INIT_PATH", help="Path to the init file")
    args = parser.parse_args()
    assert args.GITHUB_REF.startswith(
        "refs/tags/v"
    ), f'GITHUB_REF should start with "refs/tags/v": {args.GITHUB_REF}'
    tag_version = args.GITHUB_REF[11:]
    data = pathlib.Path(args.INIT_PATH).read_text("utf8")
    pypi_version = re.search(r"__version__ = ['\"](.*?)['\"]", data).group(1)
    assert (
        tag_version == pypi_version
    ), f"The tag version {tag_version} != {pypi_version} specified in {args.INIT_PATH}"
