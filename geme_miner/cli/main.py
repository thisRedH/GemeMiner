#!/usr/bin/env python
from sys import exit, stdout, stderr
from geme_miner.cli import args, config


def default_main():
    parg = args.parse()
    _pconf = config.parse(parg.config_path)

    # Lazy import to speed up --help
    from geme_miner.core.third_party.stores import Steam, Epic, ItchIO  # , GoG
    from geme_miner.core import files
    from geme_miner.core.normalize import format_dict, FormatTypeEnum

    store_flags = {
        "steam": "all" in parg.stores or "steam" in parg.stores,
        "epic": "all" in parg.stores or "epic_games" in parg.stores,
        "gog": "all" in parg.stores or "gog" in parg.stores,
        "itchio": "all" in parg.stores or "itchio" in parg.stores,
    }

    store_classes = {
        "steam": Steam,
        "epic": Epic,
        # "gog": GoG,
        "itchio": ItchIO,
    }

    data = {}
    for k, v in store_flags.items():
        if v and store_classes.get(k) is not None:
            r = store_classes[k].get_free_games()
            r = store_classes[k].validate_urls(r)
            data[k] = r

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
