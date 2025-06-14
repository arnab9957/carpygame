#!/bin/bash

# Cleanup script for the carpygame directory
# This script keeps only the necessary files to run car_game.py

echo "Cleaning up carpygame directory..."

# Create a backup directory
mkdir -p backup_cleanup

# Move unnecessary files to backup
echo "Moving unnecessary files to backup_cleanup directory..."

# List of files to keep
KEEP_FILES=(
  "car_game.py"
  "README.md"
  "requirements.txt"
  "highscores.json"
  "bgm.jpg"
  "fonts"
  "sounds"
)

# Move all files except those in KEEP_FILES to backup
for file in *; do
  # Skip directories in KEEP_FILES
  if [[ " ${KEEP_FILES[@]} " =~ " ${file} " ]]; then
    echo "Keeping $file"
    continue
  fi
  
  # Skip the backup directory itself
  if [[ "$file" == "backup_cleanup" ]]; then
    continue
  fi
  
  # Skip hidden files and directories
  if [[ "$file" == .* ]]; then
    continue
  fi
  
  # Move the file to backup
  echo "Moving $file to backup_cleanup/"
  mv "$file" backup_cleanup/
done

echo "Cleanup complete! Only necessary files remain in the directory."
echo "Unnecessary files have been moved to the backup_cleanup directory."
echo ""
echo "Files kept:"
for file in "${KEEP_FILES[@]}"; do
  echo "- $file"
done
