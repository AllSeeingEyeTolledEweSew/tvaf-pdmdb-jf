# Copyright (c) 2021 AllSeeingEyeTolledEweSew
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

"""Tools to maintain a Jellyfin library of public-domain media streamed via tvaf."""

import argparse
import csv
import pathlib
from typing import cast
from typing import Iterator
from typing import NamedTuple
import urllib.parse

import importlib_resources


class _MovieTorrentEntry(NamedTuple):
    imdb: str
    infohash: str
    file_index: int


def _iter_movie_torrent_entries() -> Iterator[_MovieTorrentEntry]:
    def _iter_lines() -> Iterator[str]:
        with importlib_resources.open_text("tvaf_pdmdb_jf", "movie-torrents.csv") as fp:
            for line in fp:
                if line.startswith("#"):
                    continue
                yield line

    reader = csv.reader(_iter_lines())
    for row in reader:
        imdb, infohash, file_index = row
        yield _MovieTorrentEntry(imdb.lower(), infohash.lower(), int(file_index))


def _generate_movies(args: argparse.Namespace) -> None:
    base_path = cast(pathlib.Path, args.path)
    base_url = cast(str, args.base_url)

    for entry in _iter_movie_torrent_entries():
        name = f"[imdbid={entry.imdb}]"
        version = f"{entry.infohash}.{entry.file_index}"
        path = base_path / name / f"{name} - {version}.strm"
        relative = f"tvaf/v1/1114{entry.infohash}/i/{entry.file_index}"
        url = urllib.parse.urljoin(base_url, relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{url}\n")


def generate() -> None:
    """Generates a Jellyfin library of public domain media streamed via tvaf."""
    parser = argparse.ArgumentParser(
        description="Generates a collection of *.strm files suitable for use as a "
        "Jellyfin library location. The *.strm files will point to tvaf URLs, using "
        "tvaf to stream media from bittorrent.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--base_url", default="http://127.0.0.1:8000", help="base tvaf url"
    )
    parser.add_argument(
        "--type", choices=["movies"], help="library type", required=True
    )
    parser.add_argument("path", type=pathlib.Path)

    args = parser.parse_args()
    if args.type == "movies":
        _generate_movies(args)
