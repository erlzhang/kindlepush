#!/bin/bash

ls_date=`date +%Y%m%d`

cd posts
mkdir ${ls_date}
cd ${ls_date}
gitbook init

cd ../..
scrapy crawl ckxx

cd posts
cd ${ls_date}
gitbook mobi ./ ./../../ebooks/${ls_date}.mobi

cd ../..
echo "kindle推送-${ls_date}" | mutt -s "kindle推送-${ls_date}" icily0719@kindle.cn -a "ebooks/${ls_date}.mobi"
