::summary
ColorOS 16 is running on the POCO X7 Pro as an Android 16 port based on the ACE 5
Racing build. You unpack it on a PC and run the fastboot installer instead of
sideloading in recovery. Most things work, but fingerprint, face unlock, NFC and
vibration are not ready yet.

::body
If you have only ever flashed ROMs by sideloading a zip in recovery, ColorOS 16 on
the POCO X7 Pro is a different kind of evening. There is no recovery step. You
unpack the ROM on a PC, put the phone in fastboot, run a batch file, answer a
couple of questions and the script does the rest, including the reboot.

That is why I would call this the friendliest port to try. The installer does the
work. The catch is not in the flashing at all, it is in what the port can and
cannot do yet, so start with the list.

## What works

- Closing background apps, fixed
- Battery icon showing correctly
- Setup, plus Play Store install and Google login
- SMS sending and the camera
- Brightness, vibration and Bluetooth
- MTP, OTG and deep sleep
- Dolby Atmos and RAM Plus
- Blur effects, game spoofing and a Google Photos spoof
- MEET_BASIC_INTEGRITY passes

Calls, messages, camera, Bluetooth and file transfer all behaved for me. For a
first release of a port, that is a solid place to be.

## What is not there yet

- Fingerprint unlock
- Face unlock
- NFC
- Double tap to unlock
- Play Store is not preinstalled, so you get it from the app market and log in
- Vibration was listed as coming in earlier notes, though the working list also
  mentions it, so do not be surprised either way

This is the part that decides whether the port is for you. If you unlock your
phone with your fingerprint fifty times a day, this is not the build for your
main phone yet. If you keep your phone unlocked at home and want to see ColorOS
16 on this hardware, you will have a good time.

## What you need

- The ColorOS 16 ROM download for this port
- A PC to unpack it on
- ADB and Fastboot driver installed, so fastboot sees the phone
- A full backup, because this is a clean flash
- An unlocked bootloader and a cable you trust

## Step 1 - unpack the ROM on the PC

Extract the download into a folder you can find again. Use a proper extraction
tool, not the built-in Windows one, so the folder structure and the batch file
stay where the script expects them.

## Step 2 - boot to fastboot and check the connection

Power the phone off, then hold Volume Down and Power until the fastboot screen
appears. Run:

`fastboot devices`

Confirm the serial number shows up before you run anything at all. Running the
installer against a phone the PC cannot see is how people end up convinced the
ROM is broken.

## Step 3 - run the installer

Start the installer batch file in the ROM folder. It asks whether you want a
clean flash, and the answer you want is yes. This is a port from a different
phone, so do not stack it on top of what is already there.

## Step 4 - pick your root option

The installer then asks which root method you want, with option 4 for no root at
all. Pick the one you actually want. If this is a phone you use for banking apps
and you are not chasing root for a specific reason, option 4 is the safer choice
and it is one keypress away.

## Step 5 - let it run

Wait. It reboots on its own when it is finished, and there is also a key to press
if you would rather start the reboot yourself. Do not unplug the cable while it
is working.

First boot is slow, as it is on any port. Let it finish.

## Where people get stuck

- **Running the installer with no device detected.** Check with `fastboot
  devices` first. It takes ten seconds and saves an hour.
- **Choosing a root option you do not need.** Root changes what banking and
  streaming apps will do. If you do not have a reason, pick no root.
- **Expecting a fingerprint reader.** It is not in this release. Set a PIN and a
  pattern before you flash if you rely on your finger.
- **Pulling the cable during the flash.** Same rule as always, and it matters
  more here because the script reboots on its own at the end.

## Who should install this

Install it if you want to see what ColorOS 16 feels like on POCO hardware, you
have a backup phone for anything important, and you are fine entering a PIN. The
install itself is genuinely easy thanks to the fastboot installer, which is the
part that surprised me most.

Skip it if you live in a payment app or you unlock with your fingerprint every
hour. Wait for a later update. Ports get better quickly, and this one has a lot
already working.

One practical note if Google apps matter to you: since Play Store is not in the
build, sort that out early rather than after you have restored your apps. It is a
short detour, but doing it first saves confusion.

If the driver side is what usually stops you before you start, the free Rom
Flasher tool installs the ADB and fastboot driver in a couple of clicks. It is
free, and the link is in the downloads section.

::faq
Q: Is ColorOS 16 on the POCO X7 Pro an official ROM?
A: No. It is a port based on the ACE 5 Racing build, flashed with a fastboot installer, not something Xiaomi ships for this phone.

Q: Does the fingerprint reader work on this port?
A: Not in this release. Fingerprint and face unlock are both listed as coming later, along with NFC and double tap to unlock. Use a PIN or pattern for now.

Q: How do I install ColorOS 16 on the POCO X7 Pro?
A: Unpack the ROM on a PC, boot the phone into fastboot, confirm the PC detects it, then run the installer batch file in the ROM folder. Answer yes to a clean flash and pick your root option.

Q: Is a clean flash required for this port?
A: Yes. It comes from a different phone, so flashing it over your current system is asking for trouble. The installer asks you first, and the answer is yes.

Q: Do I need root for this ROM?
A: No. The installer offers option 4 for no root, and that is the better choice if you use banking or streaming apps that object to root.
