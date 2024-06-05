from datetime import datetime
from . import igdb

EMPTY_GAME_DATA = {
    "id": "",
    "title": "",
    "release": datetime(1970, 1, 1).isoformat(),
    "page": "",
    "poster": "",
}  # fmt: skip


def _game_cleanup(game_data: dict) -> dict:
    keys = list(EMPTY_GAME_DATA.keys())
    clean = {}
    for k in keys:
        clean[k] = game_data.get(k, EMPTY_GAME_DATA[k])
    return clean


def _fill_missing_fields(game_data: dict, igdb_data: dict) -> dict:
    # TODO: implement
    return game_data


class StoreBase:
    #! Overwrite in child classes
    @classmethod
    def get_free_games_store(cls) -> list[dict]:
        raise NotImplementedError()

    @classmethod
    def get_free_games(cls) -> list[dict]:
        games_data = cls.get_free_games_store()
        games_data = [_game_cleanup(g) for g in games_data]
        igdb_data = [
            igdb.get_game(g["title"], g["release"]) for g in games_data
        ]

        data = []
        for i, game in enumerate(games_data):
            game = _fill_missing_fields(game, igdb_data[i])
            data.append({
                "store": game,
                "igdb": igdb_data[i],
            })  # fmt: skip

        return data

    @classmethod
    def validate_urls(cls, data: list[dict]) -> list[dict]:
        # TODO: implement
        return data

    def __init__(self):
        raise NotImplementedError()
