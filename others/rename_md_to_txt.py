import os
import sys

def rename_md_to_txt(folder_path):
    # Convert to absolute path
    folder_path = os.path.abspath(folder_path)
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if file ends with .md (case insensitive)
            if file.lower().endswith('.md'):
                old_path = os.path.join(root, file)
                # Create new filename by replacing .md with .txt
                new_file = file[:-3] + '.txt'
                new_path = os.path.join(root, new_file)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python rename_md_to_txt.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    rename_md_to_txt(folder_path)

if __name__ == '__main__':
    main()