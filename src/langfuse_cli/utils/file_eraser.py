import os
import shutil


def clean_datasets_dir(datasets_target_dir: str) -> None:
    if not os.path.exists(datasets_target_dir):
        return

    for filename in os.listdir(datasets_target_dir):
        file_path = os.path.join(datasets_target_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
