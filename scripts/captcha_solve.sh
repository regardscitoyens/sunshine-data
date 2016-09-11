#!/bin/bash

wav=$1

if ! test "$wav"; then
	echo "capchta needed";
	exit 1;
fi

silence="data/captcha/silence/$$.wav"

if ! test -e data/captcha/collection.db ; then
	findimagedupes -t 98% -f data/captcha/collection.db data/captcha/collection/*png
fi

sox $wav $silence"_".wav silence 1 0.001 2% 1 0.001 2% : newfile : restart 2> /dev/null
find data/captcha/silence/ -size -1000c -exec rm '{}' ';'
for s in $silence"_"*wav ; do
image=$(echo $s | sed 's/silence/image/')".png"
sox $s -n spectrogram -r -o $image
echo $image >> /tmp/$$.tmp
cp data/captcha/collection.db /tmp/$$.db
echo -n $(findimagedupes -t 98% -f /tmp/$$.db $image | sed 's/^\([^ ]*collection[^ ]*\) \(.*\)/\2 \1/' | sort | sed 's/.*collection./\ncollection/g' | grep collection | sed 's/collection//' | sed 's/_.*//') | sed 's/ //g'
done
echo
rm /tmp/$$.db /tmp/$$.tmp
