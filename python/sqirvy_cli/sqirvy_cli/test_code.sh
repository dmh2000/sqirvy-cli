
#!/bin/bash

PROMPT="create a hello world program in python"
echo "==============================================================="
echo $PROMPT | python main.py -c code -m claude-3-5-haiku-latest
echo "==============================================================="
echo $PROMPT | python main.py -c code -m gemini-2.0-flash
echo "==============================================================="
echo $PROMPT | python main.py -c code -m gpt-4-turbo
echo "==============================================================="
echo $PROMPT | python main.py -c code -m llama3.3-70b
echo "==============================================================="

