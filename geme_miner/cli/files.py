import os.path


def dump(p: str, s: str, force: bool = False) -> None:
    """
    Writes the given string `s` to the file specified by `path`.

    Parameters:
        p (str): The path to the file.
        s (str): The string to write to the file.
        force (bool): If True, the file will be overwritten if it already exists.
            If False and the file already exists, an error will be raised.

    Returns:
        None
    """

    if not force and os.path.exists(p):
        raise FileExistsError(f"File {p} already exists and force=False")

    mode = "r+" if force else "f"
    with open(p, mode) as f:
        f.seek(0)
        f.write(s)
        f.truncate()
