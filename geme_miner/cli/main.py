#!/usr/bin/env python
from sys import exit, stdout, stderr
from geme_miner.cli import args, config


def _stores(arg_stores):
    from geme_miner.core.third_party.stores import StorefrontEnum

    data = {}
    stores = [StorefrontEnum[str.upper(x)] for x in arg_stores]
    for s in stores:
        if isinstance(s.value, list):
            for store in s.value:
                data[store.__name__.lower()] = store.get_free_games()
        else:
            data[s.value.__name__.lower()] = s.value.get_free_games()
    return data

def _reddit(subs: list[str], count: int):
    from geme_miner.core.third_party.reddit import Subreddit
    from time import sleep

    data = {}
    for sub in subs:
        p = Subreddit(sub, count).get_newest()
        data[sub] = p
        sleep(1.2)

    return data

def default_main():
    parg = args.parse()
    _pconf = config.parse(parg.config_path)

    # Lazy import to speed up --help
    from geme_miner.core import files
    from geme_miner.core.normalize import format_dict, FormatTypeEnum

    data = {}
    if not parg.no_stores:
        data = _stores(parg.stores)
    if not parg.no_reddit:
        data["reddit"] = _reddit(["FreeGameFindings", "Freegamestuff", "FreeGamesOnSteam"], 15)

    formattet = format_dict(
        data,
        FormatTypeEnum[parg.format.upper()],
    )

    if parg.output == "stdout":
        print(formattet.encode("utf-8").decode("unicode_escape"), file=stdout)
    elif parg.output == "stderr":
        print(formattet.encode("utf-8").decode("unicode_escape"), file=stderr)
    else:
        try:
            files.dump(parg.output, formattet, parg.force)
        except FileExistsError:
            print(
                f'"{parg.output}" already exists! Use --force to overwrite it',
                file=stderr,
            )
            exit(1)

    exit(0)


if __name__ == "__main__":
    default_main()
