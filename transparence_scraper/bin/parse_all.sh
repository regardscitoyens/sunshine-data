#!/bin/bash

scrapy crawl ts_list 2> /dev/null > /tmp/labos.csv

sort /tmp/labos.csv | awk -F ';' '{print $2}' | while read labo; do
    echo "Try $labo" 1>&2
    for type in conventions avantages ; do
	for semestre in 2012S1 2012S2 2013S1 2013S2 2014S1 ; do
	    echo "INFO: $type $labo $semestre" 1>&2
	    while scrapy crawl "ts_"$type -a entreprise="$labo" -a semestre="$semestre" -o $type".csv" 2> /tmp/scrapy.log && grep ERROR /tmp/scrapy.log ; do
		sleep 10
	    done
	    cat /tmp/scrapy.log >> /tmp/scrapy.tout.log
	done
    done
done;
