#!/bin/bash

# Directory containing your Git repository
REPO_DIR="/path/to/your/repo"

# Directory where archived files will be moved
ARCHIVE_DIR="$REPO_DIR/archive"

# File to push
FILE_TO_PUSH="example_rule_01.json"

# Change to the repository directory
cd $REPO_DIR

# Search for the file
FILE_PATH=$(find $REPO_DIR -name $FILE_TO_PUSH)

# Check if the file exists
if [ -f "$FILE_PATH" ]; then
  # Add the file to git
  git add "$FILE_PATH"

  # Commit changes with a message
  git commit -m "Update $FILE_TO_PUSH"

  # Push changes to the remote repository
  git push origin main

  # Create archive directory if it doesn't exist
  mkdir -p $ARCHIVE_DIR

  # Move the file to the archive directory
  mv "$FILE_PATH" "$ARCHIVE_DIR/"

  # Optionally: Remove any cached files from the git index
  git rm --cached "$ARCHIVE_DIR/$FILE_TO_PUSH"

  echo "File $FILE_TO_PUSH pushed and archived successfully."
else
  echo "File $FILE_TO_PUSH not found."
fi
