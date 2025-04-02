
#!/bin/bash


echo "==============================================================="
echo "a python rest api" | python main.py -c plan -m claude-3-5-haiku-latest main.py
echo "==============================================================="
echo "a python rest api" | python main.py -c plan -m gemini-2.0-flash main.py
echo "==============================================================="
echo "a python rest api" | python main.py -c plan -m gpt-4-turbo main.py
echo "==============================================================="
echo "a python rest api" | python main.py -c plan -m llama3.3-70b main.py
echo "==============================================================="

