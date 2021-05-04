#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

echo "filtering records from $1"
echo "existing RSNs.txt file will be overwritten!"
# tweak below CLI arguments to modify xlfilter output
./xlfilter/xlfilter.py $1 5 300 400 > RSNs.txt
echo "beginning retrieval of search results for RSNs from PEERNGA database"
./pgmdbfind/pgmdbfind.py RSNs.txt 300 400
echo "**** DONE ****"
