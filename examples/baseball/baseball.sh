#!/bin/bash


schedule="extract the information about the baseball games for the specified date \
    and reformat the information in a json structure. \
    include team abbreviations, team full names, time, current scores if any. \
    output the json only, do not add any description"

html='create a web page using html, css and javascript, in a single file, \
    that loads the data from "http://localhost:8080/schedule/json" containing baseball schedule information. \
    the web site should be modern with a dark theme using dark blue, purple and yellow. \
    wrap each team name with a link to search google for information about the team name.\
    output the html only, do not add any description'

server='create a simple python web server that opens the home page "index.html" and also serves the json \
    data store in "schedule.json". the web server should listen on port 8080. \
    use the standard http.server module. \
    output the code only, do not add any description'

date > date.txt
echo "Extracting the baseball schedule"
echo $schedule | ../../bin/sqirvy-cli query  \
   --model gemini-2.5-flash-preview-04-17    \
   date.txt                                  \
   https://www.mlb.com/schedule > schedule.json

echo "Creating the web page"
echo $html | ../../bin/sqirvy-cli code       \
   --model claude-3-7-sonnet-latest schedule.json  > index.html

echo "Creating the web server"
echo $server | ../../bin/sqirvy-cli code      \
   --model gemini-2.5-pro-preview-03-25       \
   index.html                                 \
   > server.py

./strip.sh schedule.json 
./strip.sh index.html
./strip.sh server.py

# start the server
python server.py

# open the web page server.html in the default web browser
# xdg-open http://localhost:8080/index.html



