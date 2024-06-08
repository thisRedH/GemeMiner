import math
from enum import Enum
from time import sleep


def calc_downvotes(upvotes: int, upvote_ratio: float) -> int:
    if upvotes is None or upvote_ratio is None:
        return None

    return int(math.ceil((int(upvotes) / float(upvote_ratio)) - upvotes))


class SubredditApiUrl(Enum):
    REDDIT = "https://www.reddit.com/r/{sub}/new.json?sort=new&limit={limit}&sort=new&after={after}"
    PULLPUSH = "https://api.pullpush.io/reddit/search/submission?subreddit={sub}&size={limit}&after={after}"

    def raw_to_raw_posts(self, raw_data: dict) -> list[dict]:
        if self == self.REDDIT:
            data = raw_data.get("data")
            return data.get("children")
        elif self == self.PULLPUSH:
            return raw_data.get("data")
        else:
            raise ValueError(f"Unknown api: {repr(self)}")

    def data_from_post(self, post: dict) -> list[dict]:
        if self == self.REDDIT:
            return post.get("data")
        elif self == self.PULLPUSH:
            return post
        else:
            raise ValueError(f"Unknown api: {repr(self)}")


class Subreddit:
    def __init__(
        self,
        sub: str,
        post_per_req: int = 25,
        api: SubredditApiUrl = SubredditApiUrl.REDDIT,
    ):
        if sub is None or sub.strip() == "":
            raise ValueError(f"sub cannot be {repr(sub)}.")
        if not 5 <= post_per_req <= 100:
            raise ValueError(
                f"post_per_req must be between 5 and 100, inclusive, not {repr(post_per_req)}."
            )

        self.sub = sub
        self.count = post_per_req
        self.api = api

    def get_newest(self) -> list[dict] | int:
        """wrapper for `Subreddit.get_page`"""
        return self.get_page(1, 0)

    def get_page(self, page: int, sleep_time: float = 1.0) -> list[dict]:
        """
        Retrieves a page of posts.

        Args:
            page (int): The page number to retrieve. Starting from 0.
            sleep_time (int): The time in seconds to sleep between requests.

        Returns:
            list[dict]: A list of serialized posts.
            int: If error.
        """
        if page < 0:
            raise ValueError("page must be greater than or equal to 0")

        after = ""
        page += 1

        try:
            while page > 0:
                posts = self._request_raw_posts(after)
                if isinstance(posts, int):
                    return posts

                after = self.api.data_from_post(posts[-1]).get("name")
                page -= 1
                if page > 0:
                    sleep(sleep_time)
        except (IndexError, TypeError):
            return 0

        posts = [post for post in posts if post is not None]
        posts = [self._serialize_post(post) for post in posts]
        return posts

    def _request_raw_posts(
        self,
        after: str = "",
    ) -> list[dict] | int:
        import requests

        # fake curl to get less "429 Too Many Requests"
        r = requests.get(
            self.api.value.format(
                sub=self.sub,
                limit=self.count,
                after=after,
                headers={"User-Agent": "curl/8.4.0", "Accept": "*/*"},
            )
        )
        if not r.ok:
            return r.status_code

        return self.api.raw_to_raw_posts(r.json())

    def _serialize_post(self, post: dict) -> dict:
        from markdown import markdown

        post = self.api.data_from_post(post)
        if post is None:
            return None

        return {
            "id":                   post.get("id"),
            "name":                 post.get("name"),
            "title":                post.get("title"),
            "permalink":            post.get("permalink"),
            "link_flair_text":      post.get("link_flair_text"),
            "created_utc":          int(post.get("created_utc")),
            "author_name":          post.get("author_fullname"),
            "author_display_name":  post.get("author"),
            "votes": {
                "ratio":            float(post.get("upvote_ratio")),
                "up":               int(post.get("ups")),
                "down":
                    int(calc_downvotes(post.get("ups"), post.get("upvote_ratio"))),
            },
            "data": {
                "url":              post.get("url"),
                "selftext_md":      post.get("selftext"),
                # its better then selftext_html from reddit
                "selftext_html":    markdown(post.get("selftext"), output_format="html"),
            },
            "api": self.api.name,
        }  # fmt: skip
