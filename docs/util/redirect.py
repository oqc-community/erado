"""Script to generate a site index redirection to the latest release version."""

from docs.util import core, version

import jinja2

import pathlib
import logging


_logger = logging.getLogger(__name__)


def main(build_dir: str) -> None:
    core.configure_logging()

    build_path = pathlib.Path(build_dir)
    _logger.info(f"Build dir: {build_path}")

    subdirs = [path.name for path in build_path.iterdir()
               if path.is_dir()]

    latest_release = version.get_latest_release()

    if latest_release.name in subdirs:
        target = latest_release.name
    elif len(subdirs) > 0:
        target = subdirs[0]
    else:
        target = None

    if target is None:
        _logger.warning("Redirect target: None (there are no subdirs!)")
        target_path = None
    else:
        # Recurse down subfolders until we find index.html
        target_path = build_path / target

        while (len(children := list(target_path.iterdir())) > 0
               and "index.html" not in (child.name for child in children)):
            first_subdir = next((child for child in children if child.is_dir()), None)
            if first_subdir is None:
                _logger.warning(f"Could not recursively find index.html in {target}")
                break
            else:
                target_path = first_subdir

        target = str(target_path.relative_to(build_path))
        _logger.info(f"Redirect target: {target}")

    with open("docs/util/index.html.jinja", "r") as file:
        template: jinja2.Template = jinja2.Template(file.read())

    index_file = build_path / "index.html"

    with open(index_file, "w") as file:
        file.write(template.render({
            "target": target,
        }))

    _logger.info(f"Site index created at file://{index_file.absolute()}")
