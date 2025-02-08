import os
import zipfile

def zip_directory(source_dir, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
    print(f"Zipped '{source_dir}' into '{output_zip}' successfully!")

if __name__ == "__main__":
    zip_directory("src", "pi-box.birthdays.zip")
