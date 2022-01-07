import os


class LibraryShortener:
    """
    Utility class responsible for shortening library
    names to short numbers based on local mapping file.
    """

    def __init__(self, path: str) -> None:
        self._path = path

        self._names = self._read_names()

    def shorten(self, name: str) -> int:
        """Shorten library name to number and return it."""

        # Name already exists.
        if name in self._names:
            return self._names.index(name)

        # Name has to be added to mapping file.
        self._write_name(name)
        self._names.append(name)

        return len(self._names) - 1

    def get_name(self, short: int) -> str:
        """Get full library name based on short number."""

        if not 0 <= short < len(self._names):
            raise ValueError(f'Short {short} is not found')

        return self._names[short]

    def _read_names(self) -> list[str]:
        if not os.path.exists(self._path):
            return []

        # Return lines without \n.
        with open(self._path) as f:
            return [line[:-1] for line in f.readlines()]

    def _write_name(self, name: str):
        with open(self._path, 'a') as f:
            f.write(f'{name}\n')