#!/bin/sh

rsync -Lrtvz --exclude=ko.po  translationproject.org::tp/latest/grub/ po

autogenerated="en@quot en@hebrew de@hebrew en@arabic en@piglatin de_CH"


for x in $autogenerated; do
    rm "po/$x.po";
done


(
    (
	cd po && ls *.po| cut -d. -f1
	for x in $autogenerated; do
	    echo "$x";
	done
    ) | sort | uniq | xargs
) >po/LINGUAS
