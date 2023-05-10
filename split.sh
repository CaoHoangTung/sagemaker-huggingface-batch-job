#!/bin/bash

# Input file name
filename="category_test_limited.jsonl"

# Get total number of lines in file
num_lines=$(wc -l < $filename)

# Calculate number of lines per sub file
lines_per_file=$(($num_lines / 5))
echo $num_lines

# Split the file into sub files with numbered suffixes
split -d -l $lines_per_file $filename category_test_limited_

# Rename the sub files with numbered suffixes
count=1
for file in subfile_*.jsonl
do
  mv "$file" "$count-${file#subfile_}"
  count=$((count+1))
done