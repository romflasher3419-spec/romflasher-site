::summary
Lunaris AOSP v3.12 installs on the POCO X7 Pro (rodin) in three clicks with the Rom Flasher tool on the phone, and you do not need a PC or TWRP. You connect the phone, let it reboot into fastboot, pick the ROM file or the extracted folder, and let it flash. It is a clean AOSP base on Android 16, and it wipes your data.

::body
Custom ROM installs usually come with homework: a PC, a recovery, a command you have to type exactly right. Lunaris AOSP v3.12 on the POCO X7 Pro, codename rodin, drops all three. It is three clicks in the tool, and then you are looking at Android 16 on a clean AOSP base.

Maintained for rodin by @rakmoparte, with the ROM itself from the Lunaris AOSP team. The security patch is September 2026.

## What you get

- A clean AOSP base with Lunaris additions, not a skinned OEM layer
- Android 16 with a September security patch
- First boot, initial setup and daily use all shown before you commit
- A look at the interface and the ROM features
- No PC and no TWRP anywhere in the process

The point of an AOSP base is what is missing. No extra services, no launcher pushing its own store, no apps you uninstall on day one. If that is what you want, this is the shortest route to it.

## What you need

- A POCO X7 Pro (rodin)
- The Lunaris AOSP v3.12 package built for rodin
- The free Rom Flasher tool on the phone
- A complete backup, because this wipes your data
- Battery above half and a cable you trust

## Step 1 - open the tool and connect the phone

Open the tool on the phone and connect it to the target device. Let it detect the phone before you pick anything. If the connection drops here, it will drop later too, so sort the cable now.

## Step 2 - reboot into fastboot when it asks

The tool will ask to reboot the phone into fastboot. Confirm on the device screen when the prompt appears. Read that prompt properly instead of tapping through it, because this is the one screen that decides what happens next.

## Step 3 - pick the ROM file in the Flash section

Choose the ROM file, or the extracted folder, in the Flash section. Both work. If the folder route looks confusing, take the file and let the tool handle the unpacking.

## Step 4 - let it flash

Start the flash and leave everything alone. Do not unplug anything while it runs. Do not open another app on the phone. Do not check on progress by waking the screen.

## Step 5 - first boot

First boot takes a few minutes, then Android 16 setup begins. If it feels stuck, it probably is not. The boot animation on a first boot after a clean flash sits there longer than you would expect.

Do not touch the phone until the setup wizard appears. Interrupting the first boot is how a good flash turns into a long night.

## Where people get stuck

- Wrong file for the model. rodin only. Another device's package is the fastest route to a brick, and there is no recovering from that with a tool.
- Tapping through the flash path prompt without reading it. Slow down for that one screen.
- Panicking at first boot. The boot animation sits there longer than you would expect.
- Flashing with a low battery or a cable that has been bent in a pocket for a year.

## The honest part

Three clicks sounds too easy, and that is because the tool is hiding the work, not skipping it. The files are still being written, the data is still being wiped, and the first boot is still slow. What you have lost is the typing, not the risk.

That is still a good trade. Most failed first attempts at flashing are typing and driver mistakes, not bad ROMs.

## Who should install it

Install it if you want a clean AOSP build on Android 16 and you have never had the patience for a PC setup. It is also good for anyone who flashed before, hated the process, and wants the same result with fewer steps.

Skip it if you want a heavily customised system. AOSP is deliberately plain. If you like themed launchers and a pile of built-in options, read a build like that instead.

The tool doing the work here is the free Rom Flasher tool, and it is free. The link is in the downloads section, next to the ROM package.

::faq
Q: Can I install Lunaris AOSP without a PC?
A: Yes. The tool runs on the phone and handles the whole flash, so there is no PC, no TWRP and no command line. You only need the ROM package, the tool and a cable you trust.

Q: Does Lunaris AOSP v3.12 wipe my data?
A: Yes. Moving to a custom ROM means a full data wipe, so back up your photos and chats before you start. Expect the Android 16 setup wizard on first boot.

Q: How long does the first boot take?
A: A few minutes, and it will feel longer than it is. The boot animation sits there while the system builds itself for the first time. Do not touch anything until setup begins.

Q: Which file do I pick in the Flash section, the zip or the folder?
A: Either. You can select the ROM package or the extracted folder, and the tool accepts both. If you are unsure, pick the file and let the tool unpack it.

Q: Is Lunaris AOSP v3.12 Android 16?
A: Yes. It is a clean AOSP base on Android 16 with a September security patch, maintained for the POCO X7 Pro by @rakmoparte. The ROM itself is from the Lunaris AOSP team.
