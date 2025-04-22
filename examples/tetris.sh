#!/bin/bash



part1="you are creating a tetris game using html, css and javascript. \
The code will be generated in 3 files, index.html, index.css and index.js. \
For this iteration, you will produce only the html file 'index.html'. \
The css and javascript will be generated later."

part2="you are creating a tetris game using html, css and javascript. \
The code will be generated in 3 files, index.html, index.css and index.js. \
The index.html file has already be created and is included in the prompt. \
for this iteration, you will produce only the css file 'index.css' \
The javascript will be generated later.\
Use a modern light colorscheme with lots of contrast and detail. \
Be sure the css file follows the class specifications in the index.html file."

part3="you are creating a tetris game using html, css and javascript. \
The code will be generated in 3 files, index.html, index.css and index.js. \
The index.html file has already be created and is included in the prompt. \
The index.css file has already be created and is included in the prompt. \
for this iteration, you will produce only the javascript file 'index.js' "


export BINDIR=../bin  
make -C ../cmd

# you will need API keys for each of these invocations. If you don't have one for a particular 
# mode, you can change the model to one you have an API key for. use ">sqirvy-cli models" to see available models
# all context is pipelined through the processing units
rm -rf tetris && mkdir tetris 
echo $part1 | $BINDIR/sqirvy-cli code -m gemini-2.5-pro-preview-03-25 > tetris/index.html
echo $part2 | $BINDIR/sqirvy-cli code -m claude-3-7-sonnet-latest tetris/index.html >tetris/index.css
echo $part3 | $BINDIR/sqirvy-cli code -m o4-mini tetris/index.html tetris/index.css > tetris/index.js

# remove the delimiting triple backticks if present
./strip.sh tetris/index.html
./strip.sh tetris/index.css
./strip.sh tetris/index.js


# now review the code
$BINDIR/sqirvy-cli review -m claude-3-7-sonnet-latest tetris/index.html tetris/index.css tetris/index.js > tetris/review.md
python -m http.server 8080 --directory tetris 


