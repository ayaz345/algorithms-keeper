from typing import Any

from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing, sansio

from . import utils
from .comments import EMPTY_ISSUE_BODY_COMMENT

router = routing.Router()


@router.register("issues", action="opened")
async def close_invalid_issue(
    event: sansio.Event,
    gh: gh_aiohttp.GitHubAPI,
    *args: Any,
    **kwargs: Any,
) -> None:
    """Close an invalid issue.

    An issue is considered invalid if:
    - It doesn't contain any description.
    """
    installation_id = event.data["installation"]["id"]
    issue = event.data["issue"]

    if not issue["body"]:
        print(f"{'[DETECTED]':<12} Empty issue body: {issue['html_url']}")
        await utils.close_pr_or_issue(
            gh,
            installation_id,
            comment=EMPTY_ISSUE_BODY_COMMENT.format(user_login=issue["user"]["login"]),
            pr_or_issue=issue,
            label="invalid",
        )