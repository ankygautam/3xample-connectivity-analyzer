import os
import re

# Folder to scan (current directory)
PROJECT_DIR = "."

# Regex to match a list of numbers assigned to "features"
FEATURES_REGEX = re.compile(r'features\s*=\s*\[([^\]]+)\]|{"features"\s*:\s*\[([^\]]+)\]}')

def check_features_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            match = FEATURES_REGEX.search(line)
            if match:
                # Extract numbers
                numbers_str = match.group(1) or match.group(2)
                numbers = [x.strip() for x in numbers_str.split(",") if x.strip()]
                if len(numbers) != 3:
                    print(f"[{filepath}:{i}] WARNING: features has {len(numbers)} values -> {line.strip()}")

def main():
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith(".py"):
                check_features_in_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
