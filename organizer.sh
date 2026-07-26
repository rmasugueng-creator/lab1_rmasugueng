#!/bin/bash
# 1. Create the archive directory if it doesn't already exist
if [ ! -d "archive" ]; then
    mkdir archive
    echo "Directory 'archive' created."
fi

# 2. Make sure grades.csv exists before trying to archive it
if [ ! -f "grades.csv" ]; then
    echo "Error: grades.csv not found, nothing to archive."
    exit 1
fi

# 3. Generate a timestamp
timestamp=$(date +%Y%m%d-%H%M%S)

# 4. Build the new archived filename
archived_name="grades_${timestamp}.csv"

# 5. Move and rename grades.csv into archive/
mv grades.csv "archive/${archived_name}"

# 6. Recreate an empty grades.csv for the next batch of grades
touch grades.csv

# 7. Append a line to organizer.log (the file accumulates entries across runs)
echo "${timestamp} | original: grades.csv | archived: archive/${archived_name}" >> organizer.log

echo "Archiving complete: archive/${archived_name}"
echo "A new empty grades.csv has been created."
echo "Entry added to organizer.log."