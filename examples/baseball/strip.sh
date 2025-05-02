#!/bin/bash

# Check if a file argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <file>"
  exit 1
fi

# Remove the first line if it starts with "```"
sed -i '1{/^```/d}' "$1"

# Remove the last line if it starts with "```"
sed -i '$ {/^```/d}' "$1"
