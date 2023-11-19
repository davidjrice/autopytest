#! /bin/bash
CODECLIMATE_BINARY_MACOS="https://codeclimate.com/downloads/test-reporter/test-reporter-latest-darwin-amd64"
CODECLIMATE_BINARY_LINUX="https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64"
CODECLIMATE_BINARY_WINDOWS="https://codeclimate.com/downloads/test-reporter/test-reporter-latest-windows-amd64"

# Detect the operating system
if [[ "$MSYSTEM" == "MINGW64" ]]; then
  os="windows"
else
  os=$(uname | tr '[:upper:]' '[:lower:]')
fi

# Download test reporter as a static binary
echo "Downloading Code Climate test reporter"
if [[ "$os" == "darwin" ]]; then
  curl -L $CODECLIMATE_BINARY_MACOS > ./cc-test-reporter
elif [[ "$os" == "linux" ]]; then
  curl -L $CODECLIMATE_BINARY_LINUX > ./cc-test-reporter
elif [[ "$os" == "windows" ]]; then
  curl -L $CODECLIMATE_BINARY_WINDOWS > ./cc-test-reporter.exe
else
  echo "Unsupported operating system: $os"
  exit 1
fi
chmod +x ./cc-test-reporter

# Pre-test hook
if [[ "$os" == "windows" ]]; then
  ./cc-test-reporter.exe before-build
else
  ./cc-test-reporter before-build
fi

# Format the coverage data so that Code Climate understands it
echo "Formatting coverage data"
if [[ "$os" == "windows" ]]; then
  ./cc-test-reporter.exe format-coverage --input-type coverage.py -o codeclimate.json --debug
else
  ./cc-test-reporter format-coverage --input-type coverage.py -o codeclimate.json --debug
fi