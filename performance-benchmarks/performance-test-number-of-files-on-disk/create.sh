#!/bin/bash
chars16="0 1 2 3 4 5 6 7 8 9 a b c d e f"
for i in $chars16
do
    for j in $chars16
    do
	for k in $chars16
	do
#	    for l in $chars16
#	    do
#		touch data/$i$j$k$l
#	    done
	    touch data/$i$j$k
	done
    done
done
