import requests
from datetime import datetime
from bs4 import BeautifulSoup
import bs4.element
from .base_store import StoreBase

# _FREE_SP_URL = "https://store.steampowered.com/search/results?force_infinite=1&specials=1&ignore_preferences=1" # debug data
_FREE_SP_URL = "https://store.steampowered.com/search/results?force_infinite=1&maxprice=free&specials=1&ignore_preferences=1"
_PIC_URL = "https://shared.steamstatic.com/store_item_assets/steam/apps/{id}/library_600x900_2x.jpg"


def _parse_search_result(html) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="search_result_row")
    parsed = []

    for item in items:
        parsed.append(_parse_item(item))

    return parsed


def _parse_item(item: bs4.element.Tag) -> dict:
    itemkey = item.attrs["data-ds-itemkey"]
    item_type, item_id = itemkey.split("_")
    item_title = item.find("span", class_="title").text
    item_page = item.attrs["href"]
    item_image = _PIC_URL.format(id=item_id)
    item_release = (
        _parse_item_reldate(item.find("div", class_="search_released"))
        .date()
        .isoformat()
    )

    return {
        "id": item_id,
        "type": item_type,
        "title": item_title,
        "release": item_release,
        "page": item_page,
        "poster": item_image,
    }  # fmt: skip


def _parse_item_reldate(item: bs4.element.Tag) -> datetime:
    d = item.text.strip()
    try:
        return datetime.strptime(d, "%d %b, %Y")
    except ValueError:
        try:
            return datetime.strptime(d, "%d. %b. %Y")
        except ValueError:
            return datetime(1970, 1, 1)


class Steam(StoreBase):
    @classmethod
    def get_free_games_store(cls) -> list[dict]:
        r = requests.get(_FREE_SP_URL)
        if not r.ok:
            return None

        parsed = _parse_search_result(r.content)
        return parsed
