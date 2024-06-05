from .base_store import StoreBase

# _FREE_SP_URL = "https://catalog.gog.com/v1/catalog?limit=99&price=between%3A0%2C0&order=desc%3Atrending&discounted=eq%3Atrue&productType=in%3Agame%2Cpack%2Cdlc%2Cextras&page=1&countryCode=US&locale=en-US&currencyCode=EUR"
_FREE_SP_URL = "https://catalog.gog.com/v1/catalog?limit=99&price=between:0,0&order=desc:trending&discounted=eq:true&productType=in:game,pack,dlc,extras&page=1&countryCode=US&locale=en-US&currencyCode=EUR"


class GoG(StoreBase):
    @classmethod
    def get_free_games_store(cls) -> list[dict]:
        raise NotImplementedError("FIXME: implement")
