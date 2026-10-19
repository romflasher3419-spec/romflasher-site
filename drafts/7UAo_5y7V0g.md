::summary
Yes, you can flash TWRP, fastboot ROMs and GSIs straight from the phone with no PC, using Termux. You install Termux plus Termux:API with the right versions for your Android release, grant storage and API permissions, then pull the tool from GitHub and run its commands one at a time. Miss any of those setup pieces and the flash tool opens and finds nothing.

::body
This is the setup everything else leans on. Before you can flash anything from Termux, Termux itself has to be right: the correct version for your Android release, the right permissions, and the tool loaded from GitHub. Skip a piece and the flash script opens and finds nothing, which is a confusing way to fail because nothing looks broken.

Two things catch people every single time. First, the Play Protect warning during install — you have to pause protection for a minute or the APK simply refuses to install. Second, storage permission, which you grant once when Termux asks.

After that it is copy, paste, enter, one command at a time. Nothing clever. Just order.

## What you need

- **Termux** — pick the APK that matches your Android version. The older build is the one for Android 13 and below.
- **Termux:API** — you need this alongside Termux, and both want their permissions granted.
- The **Termux Root Recovery Tool** from its GitHub page.
- Enough free storage on the phone for the ROM files.
- Patience for Play Protect complaining about an app that did not come from the store.

## Step 1 - install Termux and Termux:API

Install both. If Play Protect blocks the install, pause protection for a moment, finish the install, then turn it back on. Fighting Play Protect instead of pausing it is the main reason people get stuck here before they have even run a command.

## Step 2 - grant the permissions

Open Termux:API and accept what it asks for, including notification access. It is asking because the tool needs those pieces later. Deny them now and you will be back here wondering why a later step failed.

## Step 3 - run the commands, one at a time

Open Termux and work through the commands on the GitHub page in order. Do not paste the block all at once. If something fails in a pasted block, the failure scrolls past you and you keep going on a broken setup. One line, enter, look at the result, next line.

The sequence starts with updating packages, then setting up storage, then installing the API package, git, and the Android tools. From there you clone the tool from GitHub, move into its folder, make its scripts executable, install the ADB helper, and run the flash script.

## Step 4 - storage permission when it asks

The `termux-setup-storage` step is the one that gives Termux access to your files. Android will show you a permission prompt — accept it. If you skip this, the tool cannot see the ROM files sitting in your Downloads folder.

## Step 5 - install the ADB helper

This is the last piece. The ADB helper is what lets the tool actually talk to a device over USB. Without it, everything else is set up correctly and still cannot reach a phone in recovery or bootloader mode.

## Step 6 - run the flash script

Run it, and you are ready to start flashing ROMs and recoveries from the phone itself. No PC in the loop.

## Where people get stuck

- **Wrong Termux build for your Android version.** The first command then errors out and nothing after it makes sense. Match the version to your release.
- **Skipping Termux:API.** This breaks the storage and notification bits the tool relies on, and the failure shows up later, far from the cause.
- **Pasting everything at once.** A failure gets buried in the scroll and you carry on building a broken setup.

## Does this need root?

No. Termux itself does not need root for this setup, and neither does the install. Root is a separate decision you make later, on its own merits.

## One honest note

The first time through this, give yourself a clear half hour and do not rush the command step. The commands are not hard — the trap is doing them fast. Read each result, then move on.

If the PC side of flashing is what you have been putting off, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks so you are not stuck in Device Manager. It is free, and the link is in the downloads section.

::faq
Q: Does Termux need root to flash ROMs?
A: No. Termux itself does not need root for this setup, and neither does the Termux Root Recovery Tool install. Root is a separate thing you can add later if you want it, but nothing in this guide depends on it.

Q: Which Termux version should I install?
A: The one that matches your Android release. Newer builds are for Android 14 and up, and the older build is the one for Android 13 and below. Installing the wrong one is why the first command throws errors.

Q: Why does my flash tool open and find nothing?
A: Almost always a missing piece of the setup. Check that you installed Termux:API, granted storage permission when asked, and installed the ADB helper at the end. The tool needs all three to see your files and talk to the device.

Q: Do I need Termux:API as well as Termux?
A: Yes. Termux:API is a separate app and the tool depends on the storage and notification pieces it provides. Install both and grant both sets of permissions, including notification access.

Q: Can I do this without a PC?
A: Yes, that is the point of this setup. Everything here happens on the device itself — install, permissions, the tool, and the flashing. You only need a PC if you would rather flash from a computer.
