import os


def ensure_directory(directory_path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_unique_filename(directory, base_name, extension):
    """Generate a unique filename in the given directory"""
    counter = 1
    while True:
        if counter == 1:
            filename = f"{base_name}.{extension}"
        else:
            filename = f"{base_name}_{counter}.{extension}"

        full_path = os.path.join(directory, filename)
        if not os.path.exists(full_path):
            return full_path
        counter += 1