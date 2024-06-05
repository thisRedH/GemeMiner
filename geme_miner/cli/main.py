#!/usr/bin/env python
import sys
from geme_miner.cli import args, config, files
from geme_miner.core.data_fetcher import Steam, Epic  # , GoG
from geme_miner.core.normalize import format_dict, FormatTypeEnum


def default_main():
    parg = args.parse()
    _pconf = config.parse(parg.config_path)

    store_flags = {
        "steam": "all" in parg.stores or "steam" in parg.stores,
        "epic": "all" in parg.stores or "epic_games" in parg.stores,
        "gog": "all" in parg.stores or "gog" in parg.stores,
    }

    store_classes = {
        "steam": Steam,
        "epic": Epic,
        # "gog": GoG,
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
        print(formattet, file=sys.stdout)
    elif parg.output == "stderr":
        print(formattet, file=sys.stderr)
    else:
        try:
            files.dump(parg.output, formattet, parg.force)
        except FileExistsError:
            print(
                f'"{parg.output}" already exists! Use --force to overwrite it',
                file=sys.stderr,
            )
            sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    default_main()
