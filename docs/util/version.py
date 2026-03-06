"""Script to save the latest release tag as an environment file."""

import git

import logging

from docs import conf
from docs.util import core


_logger = logging.getLogger(__name__)


def get_latest_release() -> git.TagReference:
    repo = git.Repo()
    _logger.info(f"Repo: {repo.working_tree_dir}")
    _logger.info(f"Active branch: {repo.active_branch}")

    release_tags = [tag for tag in repo.tags
                    if conf.RELEASE_REGEX.match("refs/tags/" + tag.name)]

    return release_tags[-1]


if __name__ == "__main__":
    core.configure_logging()

    latest_release = get_latest_release()
    _logger.info(f"Latest release: {latest_release.name}")

    with open(conf.ENV_FILE, "w") as file:
        file.write(f"{conf.ENV_LATEST_RELEASE}={latest_release.name}\n")
