#!/bin/bash

findimagedupes -t 98% data/captcha/image/* | sed 's/.png//g' | sed 's/image/silence/g' > /tmp/matches.txt
for match in $(awk '{print $1}' /tmp/matches.txt);
do
	letter=""
	echo $match
	play $match > /dev/null 2>&1 ;
	read letter ;
	if test "$letter"; then
		image=$(echo $match | sed 's/silence/image/' | sed 's/$/.png/') 
		ln $image "data/captcha/collection/"$(ls -i $image | cut -d ' ' -f 1)"_"$letter".png"
	fi
done
