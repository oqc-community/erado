"""CLI tool to check if a version string strictly matches the PEP 440 semantic versioning format.

If running in a GitHub CI environment, error messages are logged properly and outputs are exported to `$GITHUB_OUTPUT`.
If not, errors and outputs are printed to `stdout`.
"""
# /// script
# dependencies = [
#   "packaging<26.3",
# ]
# ///
# ruff: noqa: T201 # Allow printing in a CLI script

import contextlib
import os
import sys

import packaging.version

try:
    # Get input from command line
    if len(sys.argv) < 2 or len(sys.argv[1]) < 6:
        raise ValueError('Expected version string as a CLI argument at least 6 characters long ("vX.Y.Z").')
    version_raw = sys.argv[1]

    # Strip leading 'v' character
    if version_raw[0] != "v":
        raise packaging.version.InvalidVersion('Version string must begin with "v".')
    version_input = version_raw[1:]

    # Parse as Version instance
    version = packaging.version.Version(version_raw)

    # Extract standardised components and concatenate
    output: dict[str, str] = {
        "major": str(version.major),
        "minor": str(version.minor),
        "patch": str(version.micro),
        "pre": "" if version.pre is None else "".join(str(elt) for elt in version.pre),
        "post": "" if version.post is None else str(version.post),
        "dev": "" if version.dev is None else str(version.dev),
    }

    output["version"] = (
        output["major"]
        + "."
        + output["minor"]
        + "."
        + output["patch"]
        + output["pre"]
        + (".post" + output["post"] if output["post"] != "" else "")
        + (".dev" + output["dev"] if output["dev"] != "" else "")
    )

    # Confirm input matches standardised version format
    if version_input != output["version"]:
        raise packaging.version.InvalidVersion(
            f'Input version "{version_input}" does not match standardised "{output["version"]}".',
        )

    # Export outputs to GitHub environment if defined, else stdout
    github_output = os.environ.get("GITHUB_OUTPUT")
    with open(github_output, "a") if github_output else contextlib.nullcontext(sys.stdout) as file:
        for key, value in output.items():
            print(f"{key}={value}", file=file)

except Exception as e:
    print(
        ("::error ::" if "CI" in os.environ else "") + f"{type(e).__name__}: {str(e)}",
    )
    sys.exit(1)
