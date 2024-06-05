from datetime import datetime
from .. import igdb


GameRaw = dict
GameFinished = dict

EMPTY_GAME_DATA = {
    "id": "",
    "title": "",
    "release": datetime(1970, 1, 1).isoformat(),
    "page": "",
    "poster": "",
}  # fmt: skip

def _game_cleanup(game_data: GameRaw) -> GameRaw:
    keys = list(EMPTY_GAME_DATA.keys())
    clean = {}
    for k in keys:
        clean[k] = game_data.get(k, EMPTY_GAME_DATA[k])
    return clean


def _fill_missing_fields(game_raw: GameRaw, igdb_data: dict) -> GameRaw:
    data = game_raw
    # TODO: implement
    return data


class StoreBase:
    #! Don't Overwrite in child classes
    @classmethod
    def get_free_games(cls) -> list[GameFinished]:
        games_store = cls.get_free_games_store()
        games_store = [_game_cleanup(g) for g in games_store]
        igdb_data = [
            igdb.get_game(g["title"], g["release"]) for g in games_store
        ]

        data = []
        for i, game in enumerate(games_store):
            game = _fill_missing_fields(game, igdb_data[i])
            data.append({
                "store": game,
                "igdb": igdb_data[i],
            })  # fmt: skip

        return data

    #* Overwrite in child classes
    @classmethod
    def get_free_games_store(cls) -> list[GameRaw]:
        raise NotImplementedError()

    #* May Overwrite in child classes
    @classmethod
    def validate_urls(cls, data: list[dict]) -> list[dict]:
        # TODO: implement
        return data

    def __init__(self):
        raise NotImplementedError()
