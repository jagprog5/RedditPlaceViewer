#!/bin/bash
if [ -z "$2" ]; then
    echo "Needs 2 parameters. the downloaded file's path, followed by the sorted file's path"
    exit 255
fi
if [ -f "$2" ]; then
    echo "$(basename "$2") already exists."
    exit 254
fi
if [ -f "$1" ]; then
    echo "$(basename "$1") already downloaded."
else
    curl "https://storage.googleapis.com/justin_bassett/place_tiles" -o "$1"
    CURLVAL=$?
    echo $CURLVAL
    if [ $CURLVAL != 0 ]; then
        exit $CURLVAL
    fi
fi
echo "Sorting the file by timestamp (this will take a while)..."
sort "$1" > "$2"