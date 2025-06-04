import os
import shutil
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import winshell

primary_path = "C:/Program Files (x86)/StarCraft II"
browser_path = ""
build_path = ""
versions_path = ""
backup_path = ""
switcher_path = ""
support64_path = ""
local_path = os.getcwd()

# CDN configuration --- must be updated every ~3-4(?) weeks
cdn = "dea194011a8a3ca967f9813c979bc893"

# idk why I ended up needing to have this here but I guess I do
build_init = "Branch!STRING:0|Active!DEC:1|Build Key!HEX:16|CDN Key!HEX:16|Install Key!HEX:16|IM Size!DEC:4|CDN Path!STRING:0|CDN Hosts!STRING:0|CDN Servers!STRING:0|Tags!STRING:0|Armadillo!STRING:0|Last Activated!STRING:0|Version!STRING:0|KeyRing!HEX:16|Product!STRING:0"

# version to restore --- defaults to 5.0.13
target_version = "5.0.13"

# version: [build number, build info, version + build number]
version_dict = {
    "5.0.12": [
        91115,
        "\nus|1|51dfb8730d960b7914d59ef9841f29ee|" + cdn + "|06e931af72abd6f062324d830ff094ae||tpr/sc2|level3.blizzard.com us.cdn.blizzard.com|http://level3.blizzard.com/?maxhosts=4 http://us.cdn.blizzard.com/?maxhosts=4 https://blzddist1-a.akamaihd.net/?fallback=1&maxhosts=4 https://level3.ssl.blizzard.com/?fallback=1&maxhosts=4 https://us.cdn.blizzard.com/?fallback=1&maxhosts=4|Windows code US? acct-CAN? geoip-CA? enUS speech?:Windows code US? acct-CAN? geoip-CA? enUS text?|||5.0.12.91115||",
        "5.0.12.91115"
    ],
    "5.0.13": [
        92440,
        "\nus|1|6b36ffd0acf5bf1cd8c3e289be78d120|" + cdn + "|f5703696f8f01d56ea9db9d115099dc7||tpr/sc2|level3.blizzard.com us.cdn.blizzard.com|http://level3.blizzard.com/?maxhosts=4 http://us.cdn.blizzard.com/?maxhosts=4 https://blzddist1-a.akamaihd.net/?fallback=1&maxhosts=4 https://level3.ssl.blizzard.com/?fallback=1&maxhosts=4 https://us.cdn.blizzard.com/?fallback=1&maxhosts=4|Windows code US? acct-USA? geoip-US? enUS speech?:Windows code US? acct-USA? geoip-US? enUS text?|||5.0.13.92440||",
        "5.0.13.92440"
    ],
    "5.0.14": [
        93333,
        "\nus|1|8453c2f1c98b955334c7284215429c36|" + cdn + "|f5703696f8f01d56ea9db9d115099dc7||tpr/sc2|level3.blizzard.com us.cdn.blizzard.com|http://level3.blizzard.com/?maxhosts=4 http://us.cdn.blizzard.com/?maxhosts=4 https://blzddist1-a.akamaihd.net/?fallback=1&maxhosts=4 https://level3.ssl.blizzard.com/?fallback=1&maxhosts=4 https://us.cdn.blizzard.com/?fallback=1&maxhosts=4|Windows code US? acct-USA? geoip-US? enUS speech?:Windows code US? acct-USA? geoip-US? enUS text?|||5.0.14.93333||",
        "5.0.14.93333"
    ]
}

def main():
    # Get desired game version and user StarCraft II installation path
    global target_version, primary_path, browser_path, build_path, versions_path, backup_path, switcher_path, support64_path
    [target_version, primary_path] = select_version_and_install_path()
    print(f"Version selected: {target_version}")
    print(f"Installation folder: {primary_path}")
    browser_path = os.path.join(primary_path, "Support/BlizzardBrowser/BlizzardBrowser.exe")
    build_path = os.path.join(primary_path, ".build.info")
    versions_path = os.path.join(primary_path, "Versions")
    backup_path = os.path.join(primary_path, "Backup")
    switcher_path = os.path.join(primary_path, "Support64/SC2Switcher_x64.exe")
    support64_path = os.path.join(primary_path, "Support64")

    # Prepare installation folder by moving unneeded or important files
    backup_files()
    # Move needed game dependencies
    move_base()
    # Remove BlizzardBrowser.exe, forcing offline mode
    remove_browser()
    # Add build info and CDN configuration
    add_build_info()
    # Create SC2Switcher shortcut
    create_shortcut()

def select_version_and_install_path():
    root = tk.Tk()
    root.title("Select StarCraft II version to recover")

    # Variable to store selected version
    selected_version = tk.StringVar(value="Select a version")

    # Set window size and center it on the screen
    window_width, window_height = 400, 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Configure grid for centering
    root.grid_columnconfigure(0, weight=1)  # Center column
    root.grid_rowconfigure(0, weight=1)  # Space above dropdown
    root.grid_rowconfigure(2, weight=1)  # Space below button

    # Create a dropdown
    dropdown = ttk.Combobox(root, textvariable=selected_version, state="readonly")
    dropdown['values'] = ("5.0.12", "5.0.13")
    dropdown.grid(row=0, column=0, pady=10, padx=10)

    # To store the folder path
    folder_path = None

    messagebox.showwarning("CLOSE ALL SC2-RELATED PROGRAMS BEFORE PROCEEDING!", "Close all StarCraft II-related programs before proceeding\n(StarCraft II.exe, Battle.net, Agent.exe, the map editor, any other StarCraft II/Blizzard-related programs etc.)")

    # Function to handle confirmation and folder selection
    def on_confirm():
        nonlocal folder_path  # Access the folder_path variable defined outside
        if selected_version.get() == "Select a version":
            messagebox.showwarning("Warning", "Please select a game version.")
            return

        # Folder selection dialog
        user_response = messagebox.askokcancel(
            "StarCraft II Installation Folder Selection",
            "In the next window, please select your StarCraft II installation folder.\n"
            "Note: This folder should be named 'StarCraft II',\n"
            "and is usually under Program Files (x86) on your main drive.\n(Click OK to continue)"
        )
        if not user_response:
            sys.exit(0)

        folder_path = filedialog.askdirectory(title="Select your StarCraft II installation folder")
        if not folder_path:
            sys.exit(0)

        # User did not select a folder named "StarCraft II"
        if "StarCraft II" not in folder_path:
            messagebox.showerror("Invalid Selection", "The selected folder does not contain 'StarCraft II'. Please try again.")
            folder_path = None  # Reset folder_path for retry
            return

        # User selected the StarCraft II folder in Documents
        elif "Documents" in folder_path:
            messagebox.showerror("Invalid Selection", "Do not select the 'StarCraft II' Documents folder. Try again.")
            folder_path = None  # Reset folder_path for retry
            return

        # Handles paths that go too deep into the installation folder
        if not folder_path.endswith("StarCraft II") or folder_path.endswith("StarCraft II/StarCraft II"):
            folder_path = folder_path.split("StarCraft II")[0] + "StarCraft II"
        
        root.destroy()  # Close the window after successful selection

    # Create a confirm button
    confirm_button = ttk.Button(root, text="Confirm", command=on_confirm)
    confirm_button.grid(row=1, column=0, pady=10)

    # Start the GUI event loop
    root.mainloop()

    # Return the results
    return [selected_version.get(), folder_path]

def backup_files():
    base_name = f"Base{version_dict[target_version][0]}"

    # Create backup folder if it doesn't already exist
    os.makedirs(backup_path, exist_ok=True)

    # Move all non-essential version files into backup folder
    for folder in os.listdir(versions_path):
        folder_path = os.path.join(versions_path, folder)
        dest_path = os.path.join(backup_path, folder)

        # Check if folder contains the correct build .exe
        if folder != base_name:
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
            else:
                shutil.move(folder_path, dest_path)

    # Copy BlizzardBrowser.exe into backup folder
    if os.path.isfile(browser_path) and not os.path.isfile(f"{backup_path}/BlizzardBrowser.exe"):
        shutil.copy(browser_path, backup_path)

    # Copy build info into backup folder
    if os.path.isfile(build_path) and not os.path.isfile(f"{backup_path}/.build.info"):
        shutil.copy(build_path, backup_path)

    print(f"Non-pertinent files successfully moved to {backup_path}.")                 

def move_base():
    # Move the desired version/build folder
    build_string = f"{version_dict[target_version][0]}"
    source = f"{local_path}/Base" + build_string
    dest = f"{versions_path}/Base" + build_string
    shutil.copytree(source, dest, dirs_exist_ok = True)

def remove_browser():
    # Delete BlizzardBrowser.exe --- cutting off the connection to Battle.net servers
    try:
        if os.path.isfile(browser_path):
            os.remove(browser_path)
    except Exception as e:
        print(f"An error occurred while removing BlizzardBrowser.exe: {e}")

def add_build_info():
    try:
        # Gather needed values
        insertion_string = version_dict[target_version][1]
        # print(insertion_string)
        substring = version_dict[target_version][2]
        # print(substring)
        target = "Product!STRING:0"

        with open(build_path, 'r+') as file:
            content = file.read()
            if not content:
                file.write(build_init)
                content = build_init
        
            # If substring is already present, the target version build info is already present
            if substring in content:
                print("Build info already present. Skipping build info addition.")
                return

            # Add the build info and write back
            new_content = content.replace(target, target + insertion_string)
            file.seek(0)
            file.write(new_content)

        print("Build info added successfully.")
    except Exception as e:
        print(f"An error occurred while adding build info: {e}")

def create_shortcut():
    try:
        shortcut = os.path.join(local_path, "SC2Switcher_x64.exe - Shortcut.lnk")
        with winshell.shortcut(shortcut) as link:
            link.path = switcher_path
            link.description = "SC2Switcher Shortcut"
        print(f"SC2Switcher shortcut created successfully.")
    except Exception as e:
        print(f"An error occurred while creating a shortcut: {e}")

main()
print(f"This terminal will close automatically in 10 seconds...")
time.sleep(10)