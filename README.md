# replax_fix
 
Hello, stranger,

This repository contains all the files you need to view old StarCraft II v5.0.13 replays.

At the heart of it all is `replay_fix.exe`, which moves some files around to trick your game into running in offline mode. If you care about the details, you can read about the original method here:

- [Blizzard forum post by Talv](https://us.forums.blizzard.com/en/sc2/t/previous-version-of-the-game-replay-cannot-be-watched/28344/2)
- [Reddit post by u/losteden](https://www.reddit.com/r/starcraft/comments/1bpa5j3/comment/lc4266a/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1)

For those of you interested in the source code, you can open `replay_fix.py`.

This program is designed to work on Windows 10 / Windows 11 computers. If you are a Mac or Linux user, please consult the above links for the manual workaround.

- 1. Exit (I mean EXIT, not simply log out/minimize) StarCraft II, Battle.net, Agent.exe, the map editor, and any other StarCraft II/Blizzard-related programs.
- 2. Scroll to the top of the page, click on the green "<> Code" button, and select "Download ZIP".
- 3. Unzip the downloaded folder, open it, and run `replay_fix.exe`.
    - Your Internet browser and/or antivirus may freak out when trying to download or unzip this. If this happens, you will need to allow an exception manually.
- 4. Follow the instructions to locate your StarCraft II installation folder.
- 5. A file named `SC2Switcher_x64.exe - Shortcut` should appear in the unzipped folder. Run it.
    - StarCraft II should load as normal, but the login screen will look a bit different, similar to `![this](Images/replay_fix_1.png)`.
    - After a few seconds, the game will hang on a "Connecting to Blizzard services" dialog, as in `![this](Images/replay_fix_2.png)`.
    - You can select "Play Offline" at this point, and you will be able to view v5.0.13 replays (but not any other versions).
    - Note that you can still live-stream or use other Internet services, but StarCraft II will not have any online functionality.

If you screw up, 99% of all problems should be resolved simply by launching StarCraft II the normal way or using Scan and Repair. That said, I am not responsible for any issues caused by incorrectly following the instructions.

Your usual settings (e.g. sound, graphics, gameplay, etc.) may not be preserved in Offline Mode, so please adjust these before casting replays.

This program will need to be updated every few weeks, as Blizzard frequently rotates their CDN configuration. If it has been some time since the last update and you need to view old replays, please contact me on Discord at `randomhyperone` so I can update the CDN string. You can also find me in the [StarCraft Evolution League Discord server](https://discord.gg/VqPFXFW6A8).