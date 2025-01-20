import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import winshell

primary_path = "C:/Program Files (x86)/StarCraft II"
browser_path = primary_path + "/Support/BlizzardBrowser/BlizzardBrowser.exe"
build_path = primary_path + "/.build.info"
versions_path = primary_path + "/Versions"
backup_path = primary_path + "/Backup"
switcher_path = primary_path + "/Support64/SC2Switcher_x64.exe"
support64_path = primary_path + "/Support64"
local_path = os.getcwd()

# CDN configuration --- must be updated every ~3-4(?) weeks
cdn = "124b1d8953c97fc96ff446ccb641a89c"

# target version --- defaults to 5.0.13
target_version = "5.0.13"

# version: [build number, build info, version + build number]
version_dict = {
    "5.0.12": [
        91115,
        "\nus|1|51dfb8730d960b7914d59ef9841f29ee|" + cdn + "|06e931af72abd6f062324d830ff094ae||tpr/sc2|level3.blizzard.com us.cdn.blizzard.com|http://level3.blizzard.com/?maxhosts=4 http://us.cdn.blizzard.com/?maxhosts=4 https://blzddist1-a.akamaihd.net/?fallback=1&maxhosts=4 https://level3.ssl.blizzard.com/?fallback=1&maxhosts=4 https://us.cdn.blizzard.com/?fallback=1&maxhosts=4|Windows code US? acct-CAN? geoip-CA? enUS speech?:Windows code US? acct-CAN? geoip-CA? enUS text?|||5.0.12.91115||", "5.0.12.91115"
    ],
    "5.0.13": [
        92440,
        "\nus|1|6b36ffd0acf5bf1cd8c3e289be78d120|" + cdn + "|f5703696f8f01d56ea9db9d115099dc7||tpr/sc2|level3.blizzard.com kr.cdn.blizzard.com blizzard.gcdn.cloudn.co.kr|http://blizzard.gcdn.cloudn.co.kr/?maxhosts=4 http://kr.cdn.blizzard.com/?maxhosts=4 http://level3.blizzard.com/?maxhosts=4 https://blizzard.gcdn.cloudn.co.kr/?fallback=1&maxhosts=4 https://blzddist1-a.akamaihd.net/?fallback=1&maxhosts=4 https://blzddistkr1-a.akamaihd.net/?fallback=1&maxhosts=4 https://kr.cdn.blizzard.com/?fallback=1&maxhosts=4 https://level3.ssl.blizzard.com/?fallback=1&maxhosts=4|Windows code US? acct-USA? geoip-US? enUS speech?:Windows code US? acct-USA? geoip-US? enUS text?|||5.0.13.92440||", "5.0.13.92440"
    ],
    "5.0.14": [
        93333,
        "us|1|8453c2f1c98b955334c7284215429c36|" + cdn + "|f5703696f8f01d56ea9db9d115099dc7||tpr/sc2|level3.blizzard.com us.cdn.blizzard.com|http://level3.blizzard.com/?maxhosts=4 http://us.cdn.blizzard.com/?maxhosts=4 https://blzddist1-a.akamaihd.net/?fallback=1&maxhosts=4 https://level3.ssl.blizzard.com/?fallback=1&maxhosts=4 https://us.cdn.blizzard.com/?fallback=1&maxhosts=4|Windows code US? acct-USA? geoip-US? enUS speech?:Windows code US? acct-USA? geoip-US? enUS text?:Windows code US? acct-USA? geoip-US? koKR speech?:Windows code US? acct-USA? geoip-US? koKR text?|||5.0.14.93333||", "5.0.14.93333"
    ]
}

def main():
    # Get desired game version and user StarCraft II installation path
    [target_version, primary_path] = select_version_and_install_path()

    # Prepare installation folder by moving unneeded/important files
    backup_files()

    # Move needed game dependencies
    move_base()

    # Add build info and CDN configuration
    add_build_info()

    # Create SC2Switcher shortcut
    create_shortcut()

def select_version_and_install_path():
    root = tk.Tk()
    root.withdraw()

    while(True):
        # Ask the user to select a game version
        selected_version = tk.StringVar(value = "Select a version")

        dropdown = ttk.Combobox(root, textvariable=selected_version)
        dropdown['values'] = ("5.0.12", "5.0.13")  # Add dropdown options
        dropdown.state(["readonly"])  # Make it read-only
        dropdown.pack(pady=10, padx=10)

        confirm_button = ttk.Button(
            root, 
            text="Confirm",
            command=lambda: root.destroy())
        confirm_button.pack(pady=10)

        # Ask the user to find their StarCraft II install folder
        user_response = messagebox.askokcancel("Folder Selection", "In the next window, please select your StarCraft II installation folder.\nNote: This folder should be named 'StarCraft II',\nand is usually under Program Files (x86) on your main drive.\n(Click OK to continue)")
        # If user selects "Cancel", quit
        if not user_response:
            sys.exit(0)

        # Open file explorer dialog
        folder_path = filedialog.askdirectory(title="Select a folder")
        # If user selects "Cancel", quit
        if not folder_path:
            sys.exit(0)

        # User did not find a StarCraft II-related folder
        elif "StarCraft II" not in folder_path:
            user_response = messagebox.askokcancel("Invalid Selection", "That path does not contain a folder named 'StarCraft II'.\nPlease try again.")
            if not user_response:
                sys.exit(0)
            else:
                continue

        # User found documents folder, not game files folder
        elif "Documents" in folder_path:
            messagebox.askokcancel("Invalid Selection", "Find your StarCraft II installation folder,\nnot your StarCraft II documents folder!")
            if not user_response:
                sys.exit(0)
            else:
                continue

        # Just in case the user went too deep into the folder
        if not folder_path.endswith("StarCraft II") or folder_path.endswith ("StarCraft II/StarCraft II"):
            temp_string = folder_path.split("StarCraft II")[0]
            # messagebox.showinfo("Adjusting Selection","Input detected: " + folder_path + "\nDefaulting to: " + temp_string + "StarCraft II")
            folder_path = temp_string + "StarCraft II"
            print(folder_path)
        break

    return [selected_version, user_response]

def move_base():
    # Check if build folders already exist, and delete them if present

    # Move the appropriate build folder
    build_string = str(version_dict[target_version][0])
    source = f"{local_path}/Base" + build_string
    dest = f"{versions_path}/Base" + build_string
    shutil.copytree(source, dest, dirs_exist_ok = True)

def backup_files():
    base_name = "Base" + str(version_dict[target_version][0])

    if not os.path.exists(backup_path):
        os.mkdir(backup_path)

    # Move all non-essential version files into backup folder
    for folder in os.listdir(versions_path):
        if folder != "Base"

def rename_browser():
    source = browser_path
    dest = browser_path + ".bak"
    try:
        if os.path.isfile(source):
            if not os.path.isfile(dest):
                os.rename(source, dest)
            else:
                os.remove(source)
    except Exception as e:
        print(f"An error occurred while renaming BlizzardBrowser.exe: {e}")

def add_build_info():
    insertion_string = version_dict[target_version][1]

    target = "Product!STRING:0"
    try:
        with open(build_path, 'r') as file:
            content = file.read()
        if target not in content:
            print(f"Target text '{target}' not found in file")
            return
        
        substring = version_dict[target_version][2]
        if substring not in content:
            new_content = content.replace(target, target + insertion_string)
        else:
            print("Build info already added.")
            return
        
        with open(build_path, 'w') as file:
            file.write(new_content)

        print("Build info successfully added.")
    except Exception as e:
        print(f"An error occurred while adding build info: {e}")

def create_shortcut():
    try:
        target = switcher_path
        shortcut = local_path + "/SC2Switcher_x64.exe - Shortcut.lnk"
        with winshell.shortcut(shortcut) as link:
            link.path = target
            link.description = "SC2Switcher Shortcut"
    except Exception as e:
        print(f"An error occurred while creating a shortcut: {e}")

main()