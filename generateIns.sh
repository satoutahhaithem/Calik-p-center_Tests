#!/bin/bash

# Directory containing the instances
INSTANCE_DIR="instances"

# Check if the instance directory exists
if [ ! -d "$INSTANCE_DIR" ]; then
  echo "Instance directory $INSTANCE_DIR does not exist."
  exit 1
fi

# Loop from pmed1 to pmed40
for i in {1..40}
do
  FILENAME="pmed$i.txt"
  FILEPATH="$INSTANCE_DIR/$FILENAME"
  
  # Check if the file exists
  if [ -f "$FILEPATH" ]; then
    echo "Processing $FILENAME..."
    python3 writeInsParmMax-sat_read_from_file.py "$FILENAME"
  else
    echo "File $FILENAME does not exist."
  fi
done

echo "All instances processed."
