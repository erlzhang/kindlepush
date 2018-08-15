# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import datetime
# coding=utf-8

import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 

class KindlePipeline(object):
    def process_item(self, item, spider):
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        
        d = "posts/" + date + "/"

        result = re.findall(r'(?<=\/)(\d+)(_\d+)?(?=.shtml)', item["url"])
        filename = result[0][0]
        if ( not result[0][1] or result[0][1] == "" ):
            f = open(d + filename + '.md', 'w')
            f.write('# ' + item["title"] + '\n\n')
            f.write(item["content"])
            f.close
            summary = open(d + 'SUMMARY.md', 'a+')
            summary.write('* [' + item['title'] + '](' + filename + '.md)\n')
            summary.close()
        else:
            f = open(d + filename + '.md', 'a+')
            f.write(item["content"])
            f.close
        return
