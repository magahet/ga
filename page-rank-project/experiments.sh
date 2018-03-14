#!/bin/bash

python pageRank.py -i large.txt -a 0.75
python pageRank.py -i large.txt -a 0.85
python pageRank.py -i large.txt -a 0.95

python pageRank.py -i large.txt -a 0.75 -s
python pageRank.py -i large.txt -a 0.85 -s
python pageRank.py -i large.txt -a 0.95 -s
