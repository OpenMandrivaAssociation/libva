#!/bin/sh
# We have to exclude some YYYYMMDD and DDMMYYYY tagged versions
git ls-remote --tags https://github.com/intel/libva 2>/dev/null|awk '{ print $2; }' |sed -e "s,refs/tags/,,;s,_,.,g;s,-,.,g;s,^v\.,,;s,^v,,;s,^$PKGNAME\.,," |grep -E '^[0-9.]+$' |grep -v '20[0-9][0-9][0-9][0-9][0-9][0-9]' |grep -v '[0-9][0-9][0-9][0-9]20[0-9][0-9]' |sort -V |tail -n1
