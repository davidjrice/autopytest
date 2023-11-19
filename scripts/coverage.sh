#! /bin/bash

# COVERAGE_INPUT_FILE="coverage.xml"
COVERAGE_OUTPUT_FILE="codeclimate.json"
AGGREGATED_COVERAGE_FILE="coverage.total.json"

# Download test reporter as a static binary
echo "Downloading Code Climate test reporter"
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
chmod +x ./cc-test-reporter

# Pre-test hook
./cc-test-reporter before-build

# working_dir=$(pwd)
# Format the coverage data so that Code Climate understands it
# echo "Formatting coverage data"
# for dir in coverage-*; do
# if [[ -d $dir ]]; then
#     input="$dir"/$COVERAGE_INPUT_FILE
#     output="$dir"/$COVERAGE_OUTPUT_FILE

#     # Extract the platform name from the directory name
#     platform=${dir#coverage-}
#     platform=${platform%-*}
#     python_version=${dir##*-}

#     # Set the prefix based on the platform name
#     prefix=$working_dir
#     if [[ "$platform" == "macOS" ]]; then
#       prefix="/Users/runner/work/autopytest/autopytest"
#     elif [[ "$platform" == "Windows" ]]; then
#       prefix="D:/a/autopytest/autopytest"
#     fi

#     echo "Formatting coverage data in $input for $platform on Python $python_version"
#     ./cc-test-reporter format-coverage "$input" --input-type coverage.py  --output "$output" --prefix "$prefix" --debug
# fi
# done

parts=$(find . -name $COVERAGE_OUTPUT_FILE | wc -l)
files=$(find . -name $COVERAGE_OUTPUT_FILE)

echo "Found $parts coverage parts"
echo "Found $files coverage files"

# Sum coverage data
echo "Summing coverage data"
# shellcheck disable=SC2086
./cc-test-reporter sum-coverage --parts "$parts" $files -o $AGGREGATED_COVERAGE_FILE
# Post-test hook
echo "Uploading coverage data"
./cc-test-reporter upload-coverage -i $AGGREGATED_COVERAGE_FILE

