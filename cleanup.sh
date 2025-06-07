#!/bin/bash

# Create a backup directory if it doesn't exist
mkdir -p backup_old_files

# Move optimization and temporary files to backup
echo "Moving optimization and temporary files to backup..."
mv optimize_*.py backup_old_files/ 2>/dev/null
mv performance_*.txt backup_old_files/ 2>/dev/null
mv temp_fix.txt backup_old_files/ 2>/dev/null
mv car_game.py.bak backup_old_files/ 2>/dev/null
mv car_game_optimized.py backup_old_files/ 2>/dev/null
mv quick_performance_fix.py backup_old_files/ 2>/dev/null

# Keep only the main game file and necessary modules
echo "Keeping essential files..."
# Rename car_game_fixed.py to car_game.py (the optimized version becomes the main file)
if [ -f car_game_fixed.py ]; then
    echo "Setting car_game_fixed.py as the main game file..."
    mv car_game.py backup_old_files/ 2>/dev/null
    cp car_game_fixed.py car_game.py
fi

# Keep essential files
ESSENTIAL_FILES=(
    "car_game.py"
    "time_attack_challenge.py"
    "game_modes.py"
    "race_mode.py"
    "README.md"
    "requirements.txt"
    "highscores.json"
    "bgm.jpg"
    "integration_guide.txt"
)

# Keep directories
ESSENTIAL_DIRS=(
    "fonts"
    "sounds"
)

echo "Cleanup complete. Essential files and directories have been preserved."
echo "Temporary and optimization files have been moved to backup_old_files/"
echo ""
echo "Essential files kept:"
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "- $file"
    fi
done

echo ""
echo "Essential directories kept:"
for dir in "${ESSENTIAL_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "- $dir/"
    fi
done
