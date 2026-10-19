::summary
Dyper OS 3.0.8.0 for the POCO X7 Pro is the global fastboot build, and it went back to ext4. That one detail sets the rules: you can dirty flash from 3.0.7.0, but not from an older 3.0.8.0 build. If you are already on 3.0.8.0, clean it.

::body
Dyper OS is the fully modded take on the stock ROM, so if you want MIUI and HyperOS features with more control than the factory build gives you, this is the one. The 3.0.8.0 global package is a fastboot build, which means it comes with a folder and an installer script rather than a recovery zip you sideload.

The bit that catches people is the ext4 change. It sounds like a technical footnote and it is the thing that decides whether your flash boots or loops.

## The dirty flash rule, in one line

- Coming from Dyper OS 3.0.7.0? A dirty flash is fine.
- Already on an older 3.0.8.0 build? Do a clean install instead.
- Coming from anything else, or from stock? Clean install.

Get this wrong and you will be looking at a bootloop, wondering which step you missed. You will not have missed a step. You will have dirty flashed across a filesystem change.

## What you need

- The Dyper OS 3.0.8.0 ROM package from the link below.
- The fastboot ROM folder with its installer script inside.
- A data cable and, ideally, a PC.
- Your lock screen password and fingerprints removed before you start.

## Step 1 - back up, then take the lock screen off

Back up everything you care about. Even a dirty flash can go sideways, and a clean install wipes data for certain.

Then remove your lock screen password and any registered fingerprints. I know it sounds strange, but leaving a lock screen in place is the usual cause of fingerprint trouble after the flash, and you will spend the evening re-registering the sensor instead of using the phone.

## Step 2 - extract the archive properly

Unpack the ROM archive and open the folder for your platform. There is a folder for Windows, one for Mac and one for Linux. Use 7-Zip or WinRAR rather than the built-in Windows extractor, which sometimes flattens the folder structure.

Which folder you open matters. If the installer cannot find the images, it is almost always because the wrong platform folder was opened.

## Step 3 - fastboot and a driver check

Boot the phone into Fastboot and connect it to the PC. Run `fastboot devices` and confirm you get a serial number back.

If you get nothing, stop and fix the fastboot driver. This is the step people skip, then they blame the ROM when the script reports that it cannot find the device. The ROM is fine. The driver is not.

## Step 4 - run the installer

Run the installer for your operating system. A window opens and starts printing partition names as it writes. Some lines take a while. Let it finish.

Do not unplug the cable. Do not tap the phone to see if it is alive. When the script is done, the phone reboots on its own.

## Step 5 - first boot takes longer than you think

A clean install boots slowly. Much slower than a normal boot. Give it several minutes and resist the urge to force a restart. The setup wizard will appear when it is ready.

## Doing it without a PC

There is a phone-only route. The Termux flash file in the downloads runs the flash from the phone itself, which is useful if you do not own a computer or you are away from one. The trade is that it is slower and less forgiving of mistakes, so read the steps carefully before you start it.

## What changed in 3.0.8.0

- Decrypt, plus full read and write access for system, system_ext, vendor and product.
- A monet picker added for theming.
- Everything else carries over from the previous build.

That is the whole changelog. Short build notes are a good sign on a mod ROM. It means nothing was quietly rewritten.

## One honest note

Dyper OS is a community build, so there is no official OTA support. When a new version lands you flash it yourself. That is the trade for the mods: you get the features, and you do the maintenance. Keep a copy of a stock fastboot ROM somewhere handy in case you ever want a genuinely clean phone again.

If the driver and folder side of this is what usually slows you down, the free Rom Flasher tool on GitHub puts the ADB and fastboot driver install behind a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Can I dirty flash Dyper OS 3.0.8.0?
A: Yes if you are coming from 3.0.7.0. If you are already on an older 3.0.8.0 build, do a clean install instead, because the filesystem change to ext4 makes a dirty flash end in a bootloop.

Q: Does Dyper OS 3.0.8.0 wipe my data?
A: A clean install does. Back up your photos and files first. Even on a dirty flash, keep a backup in case something goes wrong.

Q: Do I need a PC to install it?
A: No. There is a PC route with the folder installer for Windows, Mac or Linux, and a phone-only route if you would rather flash from the device itself.

Q: Why should I remove my lock screen password before flashing?
A: Leaving a password and fingerprints in place is the usual cause of fingerprint problems after the flash. Remove them first and re-register the sensor once the ROM has booted.

Q: What is new in 3.0.8.0?
A: It adds decrypt plus full read and write access for system, system_ext, vendor and product, and a monet picker. Otherwise it carries over from the previous build.
