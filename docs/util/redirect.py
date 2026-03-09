"""Script to generate a site index redirection to the latest release version."""

from docs.util import core, version

import shutil
import pathlib
import logging


_logger = logging.getLogger(__name__)


def main(build_dir: str) -> None:
    core.configure_logging()

    build_path = pathlib.Path(build_dir)
    _logger.info(f"Build dir: {build_path}")


    latest_release = version.get_latest_release()

    # Rename latest release docs subfolder to "latest"
    for dir in build_path.iterdir():
        if dir.name == latest_release.name:
            _logger.info(f"Renaming {dir.name} to \"latest\"")
            dir.rename(build_path / "latest")

    # Copy root index.html redirection file
    index_file_source = pathlib.Path("docs/util/index.html")
    index_file_destination = build_path / "index.html"
    shutil.copyfile(index_file_source, index_file_destination)

    _logger.info(f"Site index created at file://{index_file_destination.absolute()}")
