#!/bin/bash

cd data/captcha/wav
for wav in *.wav.* ; do
sox $wav "../silence/"$wav"_".wav silence 1 0.001 2% 1 0.001 2% : newfile : restart
done
cd -
find data/captcha/silence/ -size -1000c -exec rm '{}' ';'
cd data/captcha/silence
for silence in *wav ; do 
sox $silence -n spectrogram -r -o "../image/"$silence".png"
done
cd -
