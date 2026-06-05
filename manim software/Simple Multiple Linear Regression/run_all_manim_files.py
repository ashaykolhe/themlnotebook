import os
import subprocess
import glob


def run_all_manim_files(target_directory=".", quality_flag="-pqh"):
    """
    Finds all .py files in the target directory and renders them with Manim.

    Flags option examples:
    -pql : Low quality, play video when done
    -pqm : Medium quality, play video when done
    -pqh : High quality, play video when done
    """
    # Find all Python files in the given directory
    search_path = os.path.join(target_directory, "*.py")
    python_files = glob.glob(search_path)

    # Exclude this automation script itself from running
    current_script = os.path.basename(__file__)
    files_to_render = [f for f in python_files if os.path.basename(f) != current_script]

    if not files_to_render:
        print(f"No Python files found in '{target_directory}'")
        return

    print(f"Found {len(files_to_render)} file(s) to process.\n")

    for file_path in files_to_render:
        print("=" * 60)
        print(f"Processing file: {file_path}")
        print("=" * 60)

        # The '-a' flag instructs Manim to render ALL scene classes within the file
        command = ["manim", quality_flag, "-a", file_path,"--flush_cache"]

        try:
            # Execute the command in the system terminal
            subprocess.run(command, check=True)
            print(f"Successfully rendered: {file_path}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error rendering {file_path}: {e}\n")
        except FileNotFoundError:
            print("Error: 'manim' command not found. Please ensure Manim is installed in your environment.")
            return


if __name__ == "__main__":
    # Runs on the current folder using low quality preview settings
    # run_all_manim_files(target_directory=".", quality_flag="-pql") #change to pqh when final render
    run_all_manim_files(target_directory=".", quality_flag="-pqh")
