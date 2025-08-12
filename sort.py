import os
import shutil
import re

# Path to the folder with PDFs
SOURCE_DIR = input("Enter the path name of the folder with the PDFs to sort.")  # current directory
SORTED_DIR = os.path.join(SOURCE_DIR, "sorted")

# Create the "sorted" folder
os.makedirs(SORTED_DIR, exist_ok=True)

# Pattern to match paper codes like _qp_21.pdf or _ms_33.pdf
pattern = re.compile(r"_(qp|ms)_(\d{2})\.pdf$", re.IGNORECASE)

for filename in os.listdir(SOURCE_DIR):
    if filename.lower().endswith(".pdf"):
        match = pattern.search(filename)
        if match:
            paper_type = match.group(1).upper()  # QP or MS
            paper_code = match.group(2)          # e.g., "21", "33"
            paper_number = paper_code[0]         # first digit, e.g., "2", "3"

            # Folder name example: "Paper 2 QP" or "Paper 3 MS"
            folder_name = f"Paper {paper_number} {paper_type}"
            target_folder = os.path.join(SORTED_DIR, folder_name)
            os.makedirs(target_folder, exist_ok=True)

            # Copy the file into the new folder
            shutil.copy2(os.path.join(SOURCE_DIR, filename), target_folder)
            print(f"Copied {filename} → {folder_name}")

print("✅ Sorting complete!")