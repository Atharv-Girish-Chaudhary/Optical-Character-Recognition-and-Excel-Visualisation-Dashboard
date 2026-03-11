import os

def create_root_folder_dir(root_folder_names: list) -> None:
    """
    Create directories for each folder name in the provided list if they don't already exist.

    Args:
        root_folder_names (list): List containing root folder names.

    Raises:
        Exception: If directory creation fails.
    """
    try:
        for folder_name in root_folder_names:
            folder_path = os.path.join(os.getcwd(), folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder created or already exists: {folder_path}")
    except OSError as e:
        raise Exception(f"Failed to create directories for {root_folder_names}: {e}")

def create_sub_folder_dir(root_folder_name: str, sub_folder_name: str) -> str:
    """
    Create a subfolder inside the specified root folder if it doesn't already exist.

    Args:
        root_folder_name (str): Name of the root folder.
        sub_folder_name (str): Name of the subfolder to be created.

    Returns:
        str: Absolute path of the subfolder.

    Raises:
        Exception: If subfolder creation fails.
    """
    try:
        sub_folder_dir = os.path.join(os.getcwd(), root_folder_name, sub_folder_name)
        os.makedirs(sub_folder_dir, exist_ok=True)
        print(f"Subfolder created or already exists: {sub_folder_dir}")
        return sub_folder_dir
    except OSError as e:
        raise Exception(f"Failed to create sub-folder '{sub_folder_name}' in '{root_folder_name}': {e}")

if __name__ == "__main__":
    create_root_folder_dir([r'testing\Test 1', r'testing\Test 2'])
    create_sub_folder_dir(r'testing\Test 1', r'testing\Sub Test 1')
