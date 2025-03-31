#!/bin/bash
# test_args.sh - Test script for sqirvy_cli with various argument combinations
# run this file from the parent directory where this file is located

# Exit immediately if a command exits with a non-zero status
set -e

# Function to run a test and print status
run_test() {
  echo -e "\n\n---- $1 ----"
  if ! eval "$2"; then
    echo -e "\n❌ TEST FAILED: $1"
    exit 1
  fi
  echo -e "✅ Passed"
}

echo "==== Testing sqirvy_cli with various arguments ===="

# Test with basic required arguments
run_test "Test with basic required arguments" "python -m sqirvy_cli.main query -m gpt4 -t 0.5"

# Test with stdin input
run_test "Test with stdin input" "echo 'hello from stdin' | python -m sqirvy_cli.main query -m claude3 -t 0.7"

# Test with files and URLs
run_test "Test with files and URLs" "python -m sqirvy_cli.main code -m llama3 -t 0.8 file1.txt file2.py http://example.com"

# Test all commands
run_test "Test query command" "python -m sqirvy_cli.main query -m gpt4 -t 0.3 input.txt"

run_test "Test plan command" "python -m sqirvy_cli.main plan -m claude3 -t 0.6 project.md"

run_test "Test code command" "python -m sqirvy_cli.main code -m llama3 -t 0.9 source.py"

run_test "Test review command" "python -m sqirvy_cli.main review -m gpt4 -t 0.2 code.js"

# Test using full option names
run_test "Test with full option names" "python -m sqirvy_cli.main query --model gemini --temperature 0.4"

# Test with multiple files
run_test "Test with multiple files" "python -m sqirvy_cli.main code -m claude3 -t 0.7 file1.py file2.py file3.py"

# Test with multiple URLs
run_test "Test with multiple URLs" "python -m sqirvy_cli.main review -m gpt4 -t 0.3 http://example.com/doc1 http://example.com/doc2"

# Test with mixed files and URLs
run_test "Test with mixed files and URLs" "python -m sqirvy_cli.main plan -m llama3 -t 0.9 file.txt http://example.com data.json"

# Test command with stdin and files/URLs
run_test "Test with stdin and files/URLs" "echo 'content from stdin' | python -m sqirvy_cli.main query -m gemini -t 0.5 reference.txt http://docs.example.com"

# Test edge cases for temperature
run_test "Test with minimum valid temperature" "python -m sqirvy_cli.main code -m claude3 -t 0.001 source.py"

run_test "Test with maximum valid temperature" "python -m sqirvy_cli.main plan -m gpt4 -t 1.0 project.md"

# Test with invalid arguments (these will fail, but we handle the expected failures)
echo -e "\n\n---- Test with invalid temperature (will fail) ----"
if python -m sqirvy_cli.main query -m gpt4 -t 0; then
  echo -e "\n❌ TEST FAILED: Should have failed with invalid temperature"
  exit 1
else
  echo "Failed as expected: temperature must be > 0"
  echo -e "✅ Passed"
fi

echo -e "\n\n---- Test with invalid temperature (will fail) ----"
if python -m sqirvy_cli.main query -m gpt4 -t 1.5; then
  echo -e "\n❌ TEST FAILED: Should have failed with invalid temperature"
  exit 1
else
  echo "Failed as expected: temperature must be <= 1.0"
  echo -e "✅ Passed"
fi

# Test different argument orders (command should always be first)
run_test "Test with different argument orders" "python -m sqirvy_cli.main query -t 0.7 -m gemini file.txt"

# Test with no files/URLs
run_test "Test with no files/URLs" "python -m sqirvy_cli.main plan -m llama3 -t 0.4"

echo -e "\n==== All tests completed successfully ===="