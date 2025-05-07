import os
import subprocess
import sys
import pathlib

def get_comfyui_dir():
    """
    Dynamically determines the ComfyUI base directory.
    Handles both portable and standard installations, 
    assuming the script is in a subdirectory of ComfyUI.
    """
    script_path = pathlib.Path(__file__).resolve()  # Full, absolute path
    current_dir = script_path.parent

    # Check for common directory structures
    if (current_dir.name == "scripts" and (current_dir.parent / "custom_nodes").is_dir() and (current_dir.parent / "venv").is_dir()):
        return current_dir.parent  # ComfyUI/scripts/ ... ComfyUI/
    elif current_dir.name == "python_embeded" and (current_dir.parent.parent / "custom_nodes").is_dir() and (current_dir.parent.parent / "venv").is_dir():
        return current_dir.parent.parent # ComfyUI/python_embeded/ ... ComfyUI/
    elif current_dir.name == "ComfyUI" and (current_dir.parent / "custom_nodes").is_dir() and (current_dir.parent / "venv").is_dir():
        return current_dir.parent
    else:
        # If the script is directly in the ComfyUI folder
        if (current_dir / "custom_nodes").is_dir() and (current_dir / "venv").is_dir():
          return current_dir
        print("Error: Could not determine ComfyUI directory.  Please place this script in the 'scripts' directory or the main ComfyUI directory.")
        sys.exit(1)

def activate_venv(venv_path):
    """Activates the virtual environment."""

    venv_path = pathlib.Path(venv_path).resolve()  # Ensure absolute path
    
    # Determine activate script based on OS (more robust)
    if os.name == "nt":  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
    else:  # Assume POSIX (Linux, macOS)
        activate_script = venv_path / "bin" / "activate"

    if not activate_script.exists():
        print(f"Error: Virtual environment not found at {venv_path}")
        sys.exit(1)

    #  Source the activate script (OS-specific)
    if os.name == "nt":
        subprocess.run([activate_script], shell=True, check=True)  # Windows
    else:
        subprocess.run([f"source {activate_script}",], shell=True, executable="/bin/bash", check=True) # POSIX
    
    #  Set VIRTUAL_ENV (more reliable)
    os.environ["VIRTUAL_ENV"] = str(venv_path)
    print(f"Activated virtual environment: {venv_path}")

def install_requirements(custom_nodes_dir):
    """Installs requirements.txt from each custom node directory."""

    custom_nodes_dir = pathlib.Path(custom_nodes_dir).resolve()
    if not custom_nodes_dir.exists():
        print(f"Error: Custom nodes directory not found at {custom_nodes_dir}")
        sys.exit(1)

    for node_dir in os.listdir(custom_nodes_dir):
        node_path = (custom_nodes_dir / node_dir).resolve()
        if node_path.is_dir():
            requirements_file = (node_path / "requirements.txt").resolve()
            if requirements_file.exists():
                print(f"Found requirements.txt in {node_dir}. Installing...")
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
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

def main():
    comfyui_dir = get_comfyui_dir()
    venv_path = comfyui_dir / "venv"
    custom_nodes_dir = comfyui_dir / "custom_nodes"

    activate_venv(venv_path)
    install_requirements(custom_nodes_dir)

if __name__ == "__main__":
    main()