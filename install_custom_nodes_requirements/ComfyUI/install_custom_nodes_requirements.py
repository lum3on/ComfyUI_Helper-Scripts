import os
import subprocess
import sys

def find_venv(comfyui_dir):
    """Find the virtual environment directory."""
    # Common venv names and locations
    possible_venvs = [
        os.path.join(comfyui_dir, "venv"),
        os.path.join(comfyui_dir, ".venv"),
        os.path.join(comfyui_dir, "env"),
        os.path.join(os.path.dirname(comfyui_dir), "venv"),
        os.path.join(os.path.dirname(comfyui_dir), ".venv")
    ]

    for venv_path in possible_venvs:
        if os.path.exists(os.path.join(venv_path, "Scripts", "activate.bat")):
            return venv_path

    # If no venv found, ask the user
    print("Virtual environment not automatically detected.")
    user_venv = input("Please enter the full path to your virtual environment directory (or press Enter to create a new one): ")

    if user_venv.strip():
        if os.path.exists(os.path.join(user_venv, "Scripts", "activate.bat")):
            return user_venv
        else:
            print(f"Error: The specified path '{user_venv}' does not appear to be a valid virtual environment.")
            print("A valid virtual environment should contain a Scripts/activate.bat file.")
            sys.exit(1)
    else:
        # Create a new venv if user didn't specify one
        new_venv_path = os.path.join(comfyui_dir, "venv")
        print(f"Creating a new virtual environment at {new_venv_path}...")
        try:
            subprocess.run([sys.executable, "-m", "venv", new_venv_path], check=True)
            print("Virtual environment created successfully.")
            return new_venv_path
        except subprocess.CalledProcessError:
            print("Error creating virtual environment. Please create it manually.")
            sys.exit(1)

def activate_venv(venv_path):
    """Activate the virtual environment by updating PATH and VIRTUAL_ENV."""
    activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
    if not os.path.exists(activate_script):
        print(f"Error: Virtual environment not found at {venv_path}")
        sys.exit(1)

    venv_bin = os.path.join(venv_path, "Scripts")
    os.environ["PATH"] = f"{venv_bin};{os.environ['PATH']}"
    os.environ["VIRTUAL_ENV"] = venv_path
    print(f"Activated virtual environment: {venv_path}")

def install_requirements(custom_nodes_dir):
    """Install requirements.txt from each custom node directory."""
    if not os.path.exists(custom_nodes_dir):
        print(f"Custom nodes directory not found at {custom_nodes_dir}. Creating it...")
        try:
            os.makedirs(custom_nodes_dir, exist_ok=True)
            print(f"Created custom nodes directory at {custom_nodes_dir}")
            return  # No custom nodes to process yet
        except Exception as e:
            print(f"Error creating custom nodes directory: {e}")
            sys.exit(1)

    for node_dir in os.listdir(custom_nodes_dir):
        node_path = os.path.join(custom_nodes_dir, node_dir)
        if os.path.isdir(node_path):
            requirements_file = os.path.join(node_path, "requirements.txt")
            if os.path.exists(requirements_file):
                print(f"Found requirements.txt in {node_dir}. Installing...")
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "-r", requirements_file],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    print(f"Successfully installed requirements for {node_dir}")
                    print(result.stdout)
                except subprocess.CalledProcessError as e:
                    print(f"Error installing requirements for {node_dir}:")
                    print(e.stderr)
            else:
                print(f"No requirements.txt found in {node_dir}")

def get_comfyui_dir():
    """Automatically detect the ComfyUI directory path."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if this script is already in the ComfyUI directory
    if os.path.exists(os.path.join(script_dir, "main.py")) and os.path.exists(os.path.join(script_dir, "folder_paths.py")):
        return script_dir

    # If not, check if we're in a subdirectory of ComfyUI
    parent_dir = os.path.dirname(script_dir)
    if os.path.exists(os.path.join(parent_dir, "main.py")) and os.path.exists(os.path.join(parent_dir, "folder_paths.py")):
        return parent_dir

    # If we still haven't found it, allow the user to specify the path
    print("ComfyUI directory not automatically detected.")
    user_path = input("Please enter the full path to your ComfyUI directory: ")

    if os.path.exists(os.path.join(user_path, "main.py")) and os.path.exists(os.path.join(user_path, "folder_paths.py")):
        return user_path
    else:
        print(f"Error: The specified path '{user_path}' does not appear to be a valid ComfyUI directory.")
        print("A valid ComfyUI directory should contain main.py and folder_paths.py files.")
        sys.exit(1)

def main():
    comfyui_dir = get_comfyui_dir()
    print(f"Using ComfyUI directory: {comfyui_dir}")

    venv_path = find_venv(comfyui_dir)
    custom_nodes_dir = os.path.join(comfyui_dir, "custom_nodes")

    activate_venv(venv_path)
    install_requirements(custom_nodes_dir)

if __name__ == "__main__":
    main()