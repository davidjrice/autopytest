#! /bin/bash

COVERAGE_INPUT_FILE="coverage.xml"
COVERAGE_OUTPUT_FILE="coverage.json"

# Download test reporter as a static binary
echo "Downloading Code Climate test reporter"
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
chmod +x ./cc-test-reporter

# Pre-test hook
./cc-test-reporter before-build

working_dir=$(pwd)
# Format the coverage data so that Code Climate understands it
echo "Formatting coverage data"
for dir in coverage-*; do
if [[ -d $dir ]]; then
    input="$dir"/$COVERAGE_INPUT_FILE
    output="$dir"/$COVERAGE_OUTPUT_FILE
    echo "Formatting coverage data in $input"
    ./cc-test-reporter format-coverage "$input" --input-type coverage.py  --output "$output" --prefix "$working_dir" --debug
fi
done

parts=$(find . -name $COVERAGE_OUTPUT_FILE | wc -l)
files=$(find . -name $COVERAGE_OUTPUT_FILE)

echo "Found $parts coverage parts"
echo "Found $files coverage files"

# Sum coverage data
echo "Summing coverage data"
# shellcheck disable=SC2086
./cc-test-reporter sum-coverage --parts "$parts" $files

# Post-test hook
echo "Uploading coverage data"
./cc-test-reporter after-build -t coverage.py
