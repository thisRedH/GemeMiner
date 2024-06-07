import math
from time import sleep


SUBREDDIT_JSON_URL = "https://www.reddit.com/r/{sub}/new.json?sort=new&limit={limit}&sort=new&after={after}"


def subreddit_get_raw_posts(
    sub: str, limit: int = 25, after: str = ""
) -> list[dict]:
    import requests

    r = requests.get(
        SUBREDDIT_JSON_URL.format(sub=sub, limit=limit, after=after)
    )
    if not r.ok:
        return None

    data = r.json().get("data")
    if data is None:
        return None

    return data.get("children")


def calc_downvotes(upvotes: int, upvote_ratio: float) -> int:
    if upvotes is None or upvote_ratio is None:
        return None

    return int(math.floor((int(upvotes) / float(upvote_ratio)) - upvotes))


def subreddit_serialize_post(post: dict) -> dict:
    from markdown import markdown

    data = post.get("data")
    if data is None:
        return None

    return {
        "id":                   data.get("id"),
        "name":                 data.get("name"),
        "title":                data.get("title"),
        "permalink":            data.get("permalink"),
        "link_flair_text":      data.get("link_flair_text"),
        "created_utc":          data.get("created_utc"),
        "author_name":          data.get("author_fullname"),
        "author_display_name":  data.get("author"),
        "votes": {
            "ratio":            data.get("upvote_ratio"),
            "up":               data.get("ups"),
            "down":
                calc_downvotes(data.get("ups"), data.get("upvote_ratio")),
        },
        "data": {
            "url":              data.get("url"),
            "selftext_md":      data.get("selftext"),
            "selftext_html":    markdown(data.get("selftext"), output_format="html"),
        }
    }  # fmt: skip


def subreddit_get_newest(sub: str, count: int = 25) -> list[dict]:
    """
    Retrieves the newest posts from a specified subreddit.

    Args:
        sub (str): The name of the subreddit.
        count (int): The number of posts to retrieve. Defaults to 25. Max 100.

    Returns:
        list[dict]: A list of serialized posts.
    """

    posts = subreddit_get_raw_posts(sub, count)
    posts = [subreddit_serialize_post(post) for post in posts]

    return posts


def subreddit_get_page(
    sub: str, page: int, count: int = 25, sleep_time: float = 1.0
) -> list[dict]:
    """
    Retrieves a page of posts from a specified subreddit.

    Args:
        sub (str): The name of the subreddit.
        page (int): The page number to retrieve.
        count (int): The number of posts to retrieve per page.
        sleep_time (int): The time in seconds to sleep between requests.

    Returns:
        list[dict]: A list of serialized posts.
        None: If error.

    Raises:
        ValueError: If the count is less than 3.
        ValueError: If the page is less than 1.
        ValueError: If the count is greater than 100.
        ValueError: If the page is greater than 10.

    Note:
        The function will retrieve all pages until it reaches the your page.
        So if you want to get page 5, it needs to retrieve data from reddit 5 times.
    """

    if page > 10:
        raise ValueError(
            "page must be less than or equal to 10. "
            "Use _subreddit_get_page() if you really want more than 10 pages"
        )

    return _subreddit_get_page(sub, page, count, sleep_time)


def _subreddit_get_page(
    sub: str, page: int, count: int, sleep_time: float
) -> list[dict]:
    after = ""

    if page < 1:
        raise ValueError("page must be greater than or equal to 1")
    if count <= 2:
        raise ValueError("count must be greater than 2")
    if count > 100:
        raise ValueError("count must be less than or equal to 100")

    try:
        while page > 0:
            posts = subreddit_get_raw_posts(sub, count, after)
            after = posts[-1].get("data").get("name")
            page -= 1
            if page > 0:
                sleep(sleep_time)
    except (IndexError, TypeError):
        return None

    posts = [post for post in posts if post is not None]

    posts = [subreddit_serialize_post(post) for post in posts]
    return posts
