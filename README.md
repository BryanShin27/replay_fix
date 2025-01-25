# replay_fix

**PLEASE NOTE: Offline Mode only works for versions of the game during which you owned paid game content. If you did not own paid game content during the version of the game which you are trying to recover, this workaround will likely fail for you. Moreover, I'm not a subject matter expert on manipulating game data, nor am I associated with people like Talv who are. I have simply haphazardly written a program to automate a manual process they have described.**

Hello, stranger,

This repository contains all the files you need to view your old, broken StarCraft II replays.

I originally developed this program in order to regain access to my own tournament replays. Although I am largely retired from supporting any sort of mainstream StarCraft II, in this case, I felt what I had made was simply too useful to keep to myself, so I polished it to share.

This program currently supports versions 5.0.12 and 5.0.13, but I plan to keep it updated so long as I am able, since Blizzard will no doubt break more versions in the future.

At the heart of it all is `replay_fix.exe`, which moves some files around to trick your game into running in offline mode with a certain configuration. If you care about the details, you can read about the original method here:

- [Blizzard forum post by Talv](https://us.forums.blizzard.com/en/sc2/t/previous-version-of-the-game-replay-cannot-be-watched/28344/2)
- [Reddit post by u/losteden](https://www.reddit.com/r/starcraft/comments/1bpa5j3/comment/lc4266a/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1)

For those of you interested in the source code, you can look at `replay_fix.py`.

This program is designed to work on Windows 10 / Windows 11 computers. If you are a Mac or Linux user, you may need to consult the above links for the manual workaround.

- 1. Exit (I mean EXIT, not simply log out/minimize) StarCraft II, Battle.net, Agent.exe, the map editor, and any other StarCraft II/Blizzard-related programs.
- 2. Scroll to the top of the page, click on the green "<> Code" button, and select "Download ZIP".
- 3. Unzip the downloaded folder, open it, and run `replay_fix.exe`.
    - Your Internet browser and/or antivirus may freak out when trying to download or unzip this. If this happens, you will need to allow an exception manually.
        - Particularly, Chromium-based browsers seem to have this issue. Firefox is less alarmed.
- 4. Follow the instructions on-screen:
    - Select the desired version of StarCraft II.
    - Locate your StarCraft II installation folder.
- 5. A file named `SC2Switcher_x64.exe - Shortcut` should appear in the unzipped folder. Run it.
    - StarCraft II should load as normal, but the login screen will look a bit different, similar to `replay_fix_1.jpg`.
    - After a few seconds, the game will hang on a "Connecting to Blizzard services" dialog, as in `replay_fix_2.jpg`.
    - You can select "Play Offline" at this point, and you will be able to view old replays for the version you selected (but not any other broken versions).
    - Note that you can still live-stream or use other Internet services, but StarCraft II will not have any online functionality.
        - This means YOU CANNOT AUTOMATICALLY RETRIEVE MISSING MAP/MOD DATA.
        - If you need access to map/mod data, please download them by playing with said maps/mods in Online Mode before viewing replays in Offline Mode.

If you mess up, or are done viewing old replays and want to play the current version again, simply use Scan and Repair on StarCraft II in the Battle.net launcher.

I have no reason to believe this program will cause any serious adverse effects on your computer, but I am not responsible for any issues caused by users incorrectly following the instructions, manually tampering with their own game files to work around any bugs resulting from using this program, etc.

Your usual settings (e.g. sound, graphics, gameplay, etc.) may not be preserved in Offline Mode, so please adjust these before casting replays.

This program will need to be updated every few weeks, as Blizzard frequently rotates their CDN configuration. If it has been some time since the last update and you need to view old replays, please contact me on Discord at `randomhyperone` so I can update the CDN string. You can also find me in the [StarCraft Evolution League Discord server](https://discord.gg/VqPFXFW6A8).