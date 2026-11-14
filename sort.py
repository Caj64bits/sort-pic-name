import os
import shutil
from datetime import datetime
from PIL import Image, ExifTags


def rename_and_move_pictures(source_folder, destination_folder):
    # Ensure source directory exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    # Create destination directory if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Supported image extensions
    valid_extensions = (".jpg", ".jpeg", ".png", ".tiff", ".webp")

    # Counter for renamed files
    count = 0

    for filename in os.listdir(source_folder):
        if not filename.lower().endswith(valid_extensions):
            continue

        source_path = os.path.join(source_folder, filename)

        # Try to get the date taken from EXIF data
        date_taken = None
        try:
            with Image.open(source_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    # Find the tag ID for 'DateTimeOriginal'
                    for tag_id, value in exif_data.items():
                        tag_name = ExifTags.TAGS.get(tag_id)
                        if tag_name == "DateTimeOriginal":
                            # Format is usually 'YYYY:MM:DD HH:MM:SS'
                            date_taken = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                            break
        except Exception as e:
            print(f"Could not read EXIF for {filename}: {e}")

        # Fallback to file modification time if EXIF is missing
        if not date_taken:
            timestamp = os.path.getmtime(source_path)
            date_taken = datetime.fromtimestamp(timestamp)

        # Format date as YYYY-MM-DD_HH-MM-SS
        base_name = date_taken.strftime("%Y-%m-%d_%H-%M-%S")
        file_ext = os.path.splitext(filename)[1].lower()

        new_filename = f"{base_name}{file_ext}"
        destination_path = os.path.join(destination_folder, new_filename)

        # Handle naming conflicts if two photos were taken at the exact same second
        counter = 1
        while os.path.exists(destination_path):
            new_filename = f"{base_name}_{counter}{file_ext}"
            destination_path = os.path.join(destination_folder, new_filename)
            counter += 1

        # Copy the file to the new folder (change to shutil.move if you want to move instead of copy)
        shutil.copy2(source_path, destination_path)
        print(f"Copied & Renamed: {filename} -> {new_filename}")
        count += 1

    print(f"\nDone! Processed {count} pictures into '{destination_folder}'.")


# Example usage:
if __name__ == "__main__":
    SOURCE = "./"  # Replace with your source folder path
    DESTINATION = "./sorted_pictures"  # Replace with your destination folder path

    rename_and_move_pictures(SOURCE, DESTINATION)
