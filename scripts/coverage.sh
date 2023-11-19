#! /bin/bash

COVERAGE_INPUT_FILE="coverage.xml"
COVERAGE_OUTPUT_FILE="coverage.json"
AGGREGATED_COVERAGE_FILE="coverage.total.json"

# Download test reporter as a static binary
echo "Downloading Code Climate test reporter"
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
chmod +x ./cc-test-reporter

# Pre-test hook
./cc-test-reporter before-build

# Format the coverage data so that Code Climate understands it
echo "Formatting coverage data"
for dir in coverage-*; do
if [[ -d $dir ]]; then
    ./cc-test-reporter format-coverage --input-type coverage.py "$dir"/$COVERAGE_INPUT_FILE --output "$dir"/$COVERAGE_OUTPUT_FILE
fi
done

parts=$(find . -name $COVERAGE_OUTPUT_FILE | wc -l)
files=$(find . -name $COVERAGE_OUTPUT_FILE)

echo "Found $parts coverage parts"
echo "Found $files coverage files"

# Sum coverage data
echo "Summing coverage data"
./cc-test-reporter sum-coverage --output - --parts "$($parts)" "$($files)" > $AGGREGATED_COVERAGE_FILE
sum_coverage_result=$?

# Post-test hook
echo "Uploading coverage data"
./cc-test-reporter after-build --exit-code $sum_coverage_result --input $AGGREGATED_COVERAGE_FILE
