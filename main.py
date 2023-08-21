import os
import datetime
import shutil
import piexif

def modify_exif(image_path, time_delta):
    try:
        # Load Exif data
        exif_data = piexif.load(image_path)

        if "Exif" in exif_data:
            exif_dict = exif_data["Exif"]

            if piexif.ExifIFD.DateTimeOriginal in exif_dict:
                original_date = exif_dict[piexif.ExifIFD.DateTimeOriginal]
                original_date_str = original_date.decode("utf-8")

                # Parse the current date time from Exif
                exif_date_time = datetime.datetime.strptime(original_date_str, "%Y:%m:%d %H:%M:%S")

                # Check if the photo was taken between midnight and 3 AM
                if 0 <= exif_date_time.hour < 3:
                    # Subtract 2 hours from the photo's date time
                    new_date_time = exif_date_time - datetime.timedelta(hours=time_delta)

                    # Format the new date time to Exif format
                    new_exif_date = new_date_time.strftime("%Y:%m:%d %H:%M:%S")
                    exif_dict[piexif.ExifIFD.DateTimeOriginal] = new_exif_date.encode("utf-8")

                    # Save the modified Exif data
                    exif_data["Exif"] = exif_dict
                    exif_bytes = piexif.dump(exif_data)
                    piexif.insert(exif_bytes, image_path)

                    return True

        return False
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {e}")
        return False

def modify_images_in_folder(input_folder, output_folder):
    # Number of hours to subtract from the photo's date time
    time_delta = 3

    if not os.path.isdir(input_folder):
        print("Invalid input folder path.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        if filename.lower().endswith(('.jpg', '.jpeg')):
            # Copy and modify Exif data for photos
            shutil.copy2(file_path, output_path)
            modify_exif(output_path, time_delta)

if __name__ == "__main__":
    input_folder = "C:/Users/jie95/Desktop/Foto di iCloud da Matthew Chen"
    output_folder = "C:/Users/jie95/Desktop/NEW EXIF"
    modify_images_in_folder(input_folder, output_folder)



