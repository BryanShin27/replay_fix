import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import winshell

primary_path = "C:/Program Files (x86)/StarCraft II"
browser_path = primary_path + "/Support/BlizzardBrowser/BlizzardBrowser.exe"
build_path = primary_path + "/.build.info"
versions_path = primary_path + "/Versions"
backup_path = primary_path + "/Backup"
switcher_path = primary_path + "/Support64/SC2Switcher_x64.exe"
support64_path = primary_path + "/Support64"
local_path = os.getcwd()

def main():
    # Get user StarCraft II installation location
    primary_path = select_folder()
    
    # Step 0: Copy old files into a backup
    # Step 1: Ensure Battle.net or anything related is not running
    # Step 2: Ensure that the only binary within the Versions folder is 92440
    move_base_92440()
    backup_files()

    # Step 3: Rename StarCraft II/Support/BlizzardBrowser/BlizzardBrowser.exe
    if rename_browser():
        return
    
    # Step 4: Add build info to .build.info
    # Step 5: Replace the outdated CDN with the current one
    add_build_info()

    # Step 6: Create a shortcut of StarCraft II/Support64/SC2Switcher_x64.exe
    create_shortcut()
    # Step 7: Ensure Battle.net is shut off and launch SC2Switcher_x64.exe shortcut
    
    print("Script complete.")
    return

def select_folder():
    root = tk.Tk()
    root.withdraw()

    while(True):
        # tell the user to find their StarCraft II install folder
        user_response = messagebox.askokcancel("Folder Selection", "In the next window, please select your StarCraft II installation folder.\nNote: This folder should be named 'StarCraft II',\nand should be under C:\Program Files (x86) if you did not manually set it.\n(Click OK to continue)")
        if not user_response:
            sys.exit(0)

        # open file explorer dialog
        folder_path = filedialog.askdirectory(title="Select a folder")
        if not folder_path:
            sys.exit(0)

        # user did not find a StarCraft II-related folder
        elif "StarCraft II" not in folder_path:
            user_response = messagebox.askokcancel("Invalid Selection", "That path does not contain a folder named 'StarCraft II'.\nPlease try again.")
            if not user_response:
                sys.exit(0)
            else:
                continue

        # user found documents folder, not game files folder
        elif "Documents" in folder_path:
            messagebox.askokcancel("Invalid Selection", "Find your StarCraft II installation folder,\nnot your StarCraft II documents folder!")
            if not user_response:
                sys.exit(0)
            else:
                continue

        # just in case the user went too deep into the folder
        if not folder_path.endswith("StarCraft II"):
            temp_string = folder_path.split("StarCraft II")[0]
            # messagebox.showinfo("Adjusting Selection","Input detected: " + folder_path + "\nDefaulting to: " + temp_string + "StarCraft II")
            folder_path = temp_string + "StarCraft II"
            print(folder_path)
        break
        
    return folder_path

def move_base_92440():
    # delete existing Base92440, if present
    if os.path.isdir(f"{versions_path}/Base92440"):
        shutil.rmtree(f"{versions_path}/Base92440")
    
    # move Base92440 folder
    source = f"{local_path}/Base92440"
    dest = f"{versions_path}/Base92440"
    shutil.copytree(source, dest, dirs_exist_ok = True)
    
def backup_files():
    if not os.path.exists(backup_path):
        os.mkdir(backup_path)

    # Move non-92440 version files into backup folder
    for folder in os.listdir(versions_path):
        if folder != "Base92440":
            if not os.path.isdir(f"{backup_path}/{folder}"):
                print(os.path.isdir(f"{backup_path}/{folder}"))
                source = versions_path + "/" + folder
                dest = backup_path
                shutil.move(source, dest)
            else:
                shutil.rmtree(f"{versions_path}/{folder}")

    # Copy BlizzardBrowser.exe into backup folder
    if os.path.isfile(browser_path) and not os.path.isfile(f"{backup_path}/BlizzardBrowser.exe"):
        source = browser_path
        dest = backup_path
        shutil.copy(source, dest)

    # Copy build info into backup folder
    if os.path.isfile(build_path) and not os.path.isfile(f"{backup_path}/.build.info"):
        source = build_path
        dest = backup_path
        shutil.copy(source, dest)

def rename_browser():
    source = browser_path
    dest = browser_path + ".bak"
    try:
        if os.path.isfile(source):
            if not os.path.isfile(dest):
                os.rename(source, dest)
            else:
                os.remove(source)
        print("BlizzardBrowser.exe renamed successfully.")
    except:
        print("BlizzardBrowser.exe failed to rename, exiting program.")
        return 1
    return 0

def add_build_info():
    insertion_string = "\nus|1|6b36ffd0acf5bf1cd8c3e289be78d120|124b1d8953c97fc96ff446ccb641a89c|f5703696f8f01d56ea9db9d115099dc7||tpr/sc2|level3.blizzard.com kr.cdn.blizzard.com blizzard.gcdn.cloudn.co.kr|http://blizzard.gcdn.cloudn.co.kr/?maxhosts=4 http://kr.cdn.blizzard.com/?maxhosts=4 http://level3.blizzard.com/?maxhosts=4 https://blizzard.gcdn.cloudn.co.kr/?fallback=1&maxhosts=4 https://blzddist1-a.akamaihd.net/?fallback=1&maxhosts=4 https://blzddistkr1-a.akamaihd.net/?fallback=1&maxhosts=4 https://kr.cdn.blizzard.com/?fallback=1&maxhosts=4 https://level3.ssl.blizzard.com/?fallback=1&maxhosts=4|Windows code US? acct-USA? geoip-US? enUS speech?:Windows code US? acct-USA? geoip-US? enUS text?|||5.0.13.92440||"
    target = "Product!STRING:0"
    try:
        with open(build_path, 'r') as file:
            content = file.read()
        if target not in content:
            print(f"Target text '{target_text}' not found in file")
            return
        
        substring = "5.0.13.92440"
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