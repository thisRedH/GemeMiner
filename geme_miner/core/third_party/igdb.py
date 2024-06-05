from datetime import date


def get_game(name: str) -> dict:
    # TODO: implement

    return {
        "id":       "TODO",
        "title":    name, #TODO: query from igdb
        "release":  date(1970, 1, 1).isoformat(), #TODO: query from igdb
        "poster":   "TODO",
    }  # fmt: skip
