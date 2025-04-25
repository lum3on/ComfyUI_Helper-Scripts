# 1. Install

Place the install_custom_nodes_requirements.bat above your ComfyUI folder.
Place the instal_custom_n_nodes_requirements.py inside your ComfyUI folder.

# 2. Run

Just double-click on the .bat and install all requirements.txt in your custom_nodes subfolders.

# 3. Summary

This tool automates the installation of dependencies for all custom nodes in a ComfyUI installation, streamlining the setup process for users with multiple custom nodes.

# 4. Motivation

Currently users are getting highly frustrated when they break their venv. Some installations like sageattention + triton require different cuda, pytorch, cuddn configurations and 3d-pack others. To sort this out more easily and to repair the dependencies for all custom_nodes this can be an update_all feature targeted for custom_node requirements

# 5. Details

Functionality:

Batch Script (install_custom_nodes.bat): A Windows batch script that activates the ComfyUI virtual environment and executes the Python script. It is placed one directory above the ComfyUI folder (e.g., C:\Tools\Comfy-Portable), dynamically locates the ComfyUI directory, and ensures the virtual environment and Python script are correctly accessed.

Python Script (install_custom_nodes_requirements.py): Scans the custom_nodes directory (e.g., C:\Tools\Comfy-Portable\ComfyUI\custom_nodes) for requirements.txt files in each custom node subdirectory. It is placed in the ComfyUI folder (e.g., C:\Tools\Comfy-Portable\ComfyUI). It installs the specified dependencies using pip within the ComfyUI virtual environment, skipping nodes without requirements.txt.

Features:

Automates dependency installation for custom nodes like comfyui-reactor, ComfyUI-Manager, etc.
Handles permissions issues by recommending Administrator mode.
Skips already installed packages to avoid redundant installations.
Provides clear output for success or errors per node.

Benefits:

Saves time for users managing numerous custom nodes.
Reduces errors from manual dependency installation.
Portable and adaptable to different ComfyUI directory structures.

Use Case:

Ideal for ComfyUI users with extensive custom node setups.

# 6. Credentials

brought to you by sirolim
https://www.linkedin.com/in/peter-schwarz-a00495172/