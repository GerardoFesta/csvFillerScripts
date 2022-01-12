#!/bin/bash
cd $1

#git fetch origin master
#git reset --hard origin/master
#echo commit,data,versione > commitsInfo.csv
git log --pretty="format:%H,%ci,%d" > commitsInfo.csv
git for-each-ref --sort=creatordate --format '%(refname),%(creatordate)' refs/tags > tags.csv
