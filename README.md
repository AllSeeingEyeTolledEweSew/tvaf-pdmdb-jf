## tvaf-pdmdb-jf

This is a proof-of-concept demo of a streaming media library with [tvaf](https://github.com/AllSeeingEyeTolledEweSew/tvaf).

It creates a Jellyfin library of public-domain media. The media items in Jellyfin will stream from bittorrent via tvaf.

Usage:

```shell
$ tvaf_pdmdb_jf_generate --base_url http://127.0.0.1:8000/ --type movies ./movies/
$ ls -R ./movies/
./movies/:
'[imdbid=tt0011237]'  '[imdbid=tt0023238]'  '[imdbid=tt0051744]'  '[imdbid=tt0053719]'  '[imdbid=tt0060666]'  '[imdbid=tt0091419]'
'[imdbid=tt0016220]'  '[imdbid=tt0023694]'  '[imdbid=tt0052169]'  '[imdbid=tt0055830]'  '[imdbid=tt0063350]'

'./movies/[imdbid=tt0011237]':
'[imdbid=tt0011237] - da1a6e45014a212abf703baed08fc2ccbd0781fa.0.strm'

...

$ cat ./movies/\[imdbid\=tt0011237\]/\[imdbid\=tt0011237\]\ -\ da1a6e45014a212abf703baed08fc2ccbd0781fa.0.strm
http://127.0.0.1:8000/tvaf/v1/1114da1a6e45014a212abf703baed08fc2ccbd0781fa/i/0
```

## Public Domain

This project uses tvaf to stream media via bittorrent.

*To the best of the author's knowledge*, all of the media referenced in this project are in the public domain in the United States. It is **not** a violation of US copyright law to download and share these media via bittorrent.

If you believe I'm mistaken about this, please file an issue and I'll remove the offending torrents.

## Data Sources

The torrents and associated IMDB ids are maintained by hand. I cross-referenced some US public-domain movies (https://publicdomainmovies.info/) with torrents from popular search sites.

## Development Status

Since this project is a proof-of-concept demo, it is not likely to receive regular updates.
