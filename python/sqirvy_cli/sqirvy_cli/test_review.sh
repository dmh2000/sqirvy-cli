
#!/bin/bash


echo "==============================================================="
python main.py -c review -m claude-3-5-haiku-latest main.py
echo "==============================================================="
python main.py -c review -m gemini-2.0-flash main.py
echo "==============================================================="
python main.py -c review -m gpt-4-turbo main.py
echo "==============================================================="
python main.py -c review -m llama3.3-70b main.py
echo "==============================================================="

