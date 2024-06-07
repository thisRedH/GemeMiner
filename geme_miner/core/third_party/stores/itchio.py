from .base import StoreBase


_SALE_PAGE_URL = "https://itch.io/games/on-sale?format=json&page={page}"
_MAX_PAGES = 30


def _query_pages() -> dict:
    import requests

    content = ""
    for i in range(_MAX_PAGES):
        r = requests.get(_SALE_PAGE_URL.format(page=i + 1))
        if not r.ok:
            continue

        json = r.json()
        if (
            json is None
            or json.get("num_items") in [None, 0]
            or json.get("content") is None
        ):
            break

        content += str(json.get("content"))
    return content


def _parse_content(content: str) -> list[dict]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content, "html.parser")
    items = soup.find_all("div", recursive=False)

    parsed = []
    for item in items:
        cell = item.find("div", class_="game_cell_data")

        discount = cell.find("div", class_="sale_tag").text
        if discount != "-100%":
            continue

        id = item.attrs["data-game_id"]
        title_tag = cell.find("a", class_="game_link")
        title = title_tag.text
        page = title_tag.attrs["href"]
        poster = item.find("img", "lazy_loaded").attrs["data-lazy_src"]

        platform_wrapper = cell.find("div", class_="game_platform")
        if platform_wrapper is None:
            platforms = []
        else:
            platform_tags = platform_wrapper.find_all(
                "span", attrs={"title": True}
            )
            platforms = [pt.attrs["title"] for pt in platform_tags]
            platforms = [p.replace("Download for ", "") for p in platforms]

        parsed.append({
            "id": id,
            "title": title,
            "page": page,
            "poster": poster,
            "platforms": platforms,
        })  # fmt: skip

    return parsed


class ItchIO(StoreBase):
    @classmethod
    def get_free_games_store(cls) -> list[dict]:
        content = _query_pages()
        parsed = _parse_content(content)
        return parsed
