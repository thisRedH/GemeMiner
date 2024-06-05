import requests
from datetime import datetime, date
from .base_store import StoreBase

_FREE_SP_URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
_STORE_BASE_URL = "https://store.epicgames.com/p/"


def _clean_result(json):
    elements = json["data"]["Catalog"]["searchStore"]["elements"][::-1]
    cleaned = []

    for e in elements:
        page = ""
        thumbnail = ""

        # epic is wierd, when pageSlug is there,
        # then productSlug isnt the right one
        try:
            page = _STORE_BASE_URL + e["catalogNs"]["mappings"][0]["pageSlug"]
        except (IndexError, TypeError):
            page = _STORE_BASE_URL + e["productSlug"]

        for image in e["keyImages"]:
            if image["type"] == "Thumbnail":
                thumbnail = image["url"]
                break

        cleaned.append({
            "id": e["id"],
            "type": e["offerType"],
            "title": e["title"],
            "release": date(1970, 1, 1).isoformat(), # Epic dosn't send a release date
            "page": page,
            "poster": thumbnail,
            "promo": e["promotions"],
            "price": e["price"]["totalPrice"],
        })  # fmt: skip

    return cleaned


def _is_promo(clean_json):
    if clean_json["price"]["discountPrice"] != 0:
        return False
    if clean_json["promo"] in ["null", []]:
        return False
    if clean_json["promo"]["promotionalOffers"] in ["null", []]:
        return False

    t = clean_json["promo"]["promotionalOffers"][0]["promotionalOffers"][0]
    start_iso, end_iso = (t["startDate"][:-1], t["endDate"][:-1])
    start_date = datetime.fromisoformat(start_iso)
    end_date = datetime.fromisoformat(end_iso)
    if start_date > datetime.now() > end_date:
        return False

    return True


class Epic(StoreBase):
    @classmethod
    def get_free_games_store(cls) -> list[dict]:
        r = requests.get(_FREE_SP_URL)
        if not r.ok:
            return None

        clean = _clean_result(r.json())
        results = []
        for game in clean:
            if _is_promo(game):
                results.append(game)

        return results
