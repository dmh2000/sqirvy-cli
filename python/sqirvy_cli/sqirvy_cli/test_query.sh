#!/bin/bash

echo "==============================================================="
echo "good morning ,how are you today?" | python main.py query -m claude-3-5-haiku-latest
echo "==============================================================="
echo "good morning ,how are you today?" | python main.py query -m gemini-2.0-flash
echo "==============================================================="
echo "good morning ,how are you today?" | python main.py query -m gpt-4-turbo
echo "==============================================================="
echo "good morning , how are you today?" | python main.py query -m llama3.3-70b
echo "==============================================================="

