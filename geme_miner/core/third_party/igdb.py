from datetime import date


def get_game(name: str, release_date: date = None) -> dict:
    # TODO: implement

    if isinstance(release_date, str):
        try:
            release_date = date.fromisoformat(release_date)
        except ValueError:
            release_date = None

    return {
        "id":       "TODO",
        "title":    name, #TODO: query from igdb
        "release":  release_date.isoformat(), #TODO: query from igdb
        "poster":   "TODO",
    }  # fmt: skip
