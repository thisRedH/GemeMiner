from datetime import date


def get_game(name: str, release_date: date = date(1970, 1, 1)) -> dict:
    # TODO: implement
    if isinstance(release_date, str):
        release_date = date.fromisoformat(release_date)

    return {
        "id":       "TODO",
        "title":    name, #TODO: query from igdb
        "release":  release_date.isoformat(), #TODO: query from igdb
        "poster":   "TODO",
    }  # fmt: skip
