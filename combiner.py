import os
from PyPDF2 import PdfMerger

# Path to your "sorted" folder
base_path = input("Enter the path name of the folder with the SORTED PDFs to combine.")  # change this to your folder

# Loop through each folder in the sorted directory
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    
    if os.path.isdir(folder_path):
        # Get all PDF files in this folder
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
        
        if not pdf_files:
            continue
        
        # Sort files by year in filename (latest first)
        pdf_files.sort(reverse=True, key=lambda x: ''.join(filter(str.isdigit, x)))
        
        # Create a Combined subfolder
        combined_folder = os.path.join(folder_path, "Combined")
        os.makedirs(combined_folder, exist_ok=True)
        
        # Output file path
        output_file = os.path.join(combined_folder, f"{folder}_combined.pdf")
        
        # Merge PDFs
        merger = PdfMerger()
        for pdf in pdf_files:
            merger.append(os.path.join(folder_path, pdf))
        
        merger.write(output_file)
        merger.close()
        
        print(f"Merged {len(pdf_files)} files into {output_file}")