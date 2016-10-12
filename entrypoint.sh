#!/bin/bash

set -e

args=("$@")

# Compile egg-info directory for each package in src directory
if [ -d ./src ]; then
    for pkj in src/*; do ( cd $pkj && if [ ! -d $pkj.egg-info ]; then python setup.py egg_info &> /dev/null; fi  ) done
fi

case $1 in
    run)
        /srv/webapp/bin/instance fg
        ;;
    initdata)
        cp -r /srv/webapp/data/filestorage /srv/webapp/var/filestorage
        cp -r /srv/webapp/data/blobstorage /srv/webapp/var/blobstorage
        /srv/webapp/bin/instance fg
        ;;
    *)
        exec "$@"
        ;;
esac
