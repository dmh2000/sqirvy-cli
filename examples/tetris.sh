#!/bin/bash

# this script does the following:
# - creates a directory called tetris
# - uses "sqirvy-cli plan" and gemini-1.5-flash to create a design for a web app
# - uses "sqirvy-cli code"    and claude-3-7-sonnet-latest to generate code for the design
# - uses #sqirvy-cli review"  and gpt-4o-mini to review the code
# - starts a web server to serve the generated code

design="create a design specification for a web project that is a \
    simple web app that implements a simple tetris game clone.       \
    the game should include a game board with a grid, a score display, and a reset button \
    Code should be html, css and javascript, in a single file named index.html. \
    Output will be markdown.  "

export BINDIR=../bin  
make -C ../cmd

# you will need API keys for each of these invocations. If you don't have one for a particular 
# mode, you can change the model to one you have an API key for. use "">sqirvy-cli models" to see available models
# all context is pipelined through the processing units
rm -rf tetris && mkdir tetris 
echo $design | \
$BINDIR/sqirvy-cli plan   -m gemini-1.5-flash                           | tee tetris/plan.md    | \
$BINDIR/sqirvy-cli code   -m claude-3-7-sonnet-latest tetris/plan.md    | tee tetris/index.html | \
$BINDIR/sqirvy-cli review -m gpt-4o-mini              tetris/index.html  >tetris/review.md   

python -m http.server 8080 --directory tetris 


