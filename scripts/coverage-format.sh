#! /bin/bash

# Detect the operating system
if [[ "$MSYSTEM" == "MINGW64" ]]; then
  os="windows"
else
  os=$(uname | tr '[:upper:]' '[:lower:]')
fi

# Download test reporter as a static binary
echo "Downloading Code Climate test reporter"
if [[ "$os" == "darwin" ]]; then
  curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-darwin-amd64 > ./cc-test-reporter
elif [[ "$os" == "linux" ]]; then
  curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
elif [[ "$os" == "windows" ]]; then
  curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-windows-amd64 > ./cc-test-reporter.exe
else
  echo "Unsupported operating system: $os"
  exit 1
fi
chmod +x ./cc-test-reporter

# Pre-test hook
./cc-test-reporter before-build

# Format the coverage data so that Code Climate understands it
echo "Formatting coverage data"
./cc-test-reporter format-coverage --input-type coverage.py -o codeclimate.json --debug
