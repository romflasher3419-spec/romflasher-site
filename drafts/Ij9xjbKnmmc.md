::summary
Superior OS Android 13 on the Xiaomi 11T Pro is a generic system image, so you flash it with fastboot rather than from recovery. The order is: enter fastbootd, flash vbmeta with verity and verification disabled, erase system, flash the system image, reboot to recovery, then wipe data. Skipping the vbmeta line is the fastest way into a boot loop.

::body
A GSI is not a device-specific build. It rides on top of your vendor and your kernel, which is exactly why the results vary from phone to phone. On my 11T Pro, Superior OS booted and SELinux sat at enforcing. That is not a promise about your device, because your vendor and kernel are not mine. It is just what happened.

The commands below are the ones from the clip, in the same order. The order is the whole job here. Do them out of sequence and you will be chasing a boot loop for an hour.

## What you need

- An unlocked bootloader. Unlocking wipes data, and there is no shortcut around that.
- Platform Tools on the PC, with working ADB and fastboot. If `fastboot devices` prints nothing, fix that before going further.
- The Superior OS Android 13 GSI image, built for ARM64.
- The vbmeta file. This is not optional for a GSI flash.
- A backup, because the wipe at the end clears your data.

## Step 1 - boot to fastboot

Plug the phone in, boot into fastboot mode, and confirm the PC can see it:

`fastboot devices`

A serial number and the word `fastboot` must come back. No serial number means a driver problem, and no fastboot command will work until that is sorted.

## Step 2 - enter fastbootd

`fastboot reboot fastboot`

This moves you from the bootloader into fastbootd, which is the userspace fastboot that can actually write logical partitions. This is the step people miss. In the old bootloader fastboot you can flash a few physical partitions, but system is a logical partition on a modern phone, and you need fastbootd to touch it. If a command later says the partition does not exist, you are in the wrong fastboot.

## Step 3 - flash vbmeta with verity and verification off

`fastboot --disable-verity --disable-verification flash vbmeta <vbmeta file>`

This is the line that decides whether the phone boots at all. A GSI is not signed the way the stock system is, so with verity and verification left on, the bootloader refuses the image and you land in a loop. Disabling both in the same command writes the flags and the vbmeta together, which is what you want.

If someone tells you to flash vbmeta without those flags, they are describing a different method. Do not mix the two.

## Step 4 - erase system

`fastboot erase system`

You are replacing the system partition outright, so start from a clean one. Leftover pieces of the previous system are what cause a build to boot and then fall apart a few minutes later.

## Step 5 - flash the system image

`fastboot flash system <system image>`

This one takes a while, longer than a normal partition flash. Let it finish. Do not pull the cable when the progress seems stuck, and do not close the window. When it completes it should report OK on the whole image.

## Step 6 - reboot to recovery

`fastboot reboot recovery`

You want recovery here, not system. From recovery you wipe data, and the wipe has to happen on the installed build rather than after the first boot.

## Step 7 - wipe data and reboot

In Mi Recovery, choose the wipe data option, then reboot. First boot on a GSI is slower than a normal ROM because the system is setting itself up for the first time against your vendor. Give it several minutes before you decide anything is wrong.

## Where people get stuck

- **Skipping the vbmeta line.** The single most common cause of a boot loop. Disable verity and verification in the same command that flashes vbmeta.
- **Staying in bootloader fastboot.** If `erase system` or `flash system` complains about a missing partition, you never entered fastbootd. Run the reboot step again.
- **Not erasing system first.** A flash over the old system leaves a mess. Erase, then flash.
- **Judging the first boot too early.** A GSI's first boot can sit on the logo far longer than you are used to.

## An honest word about GSIs

The build itself reported no bugs, and SELinux works both in enforcing and permissive. That part was clean. The hardware side is not the GSI's problem. Camera quality, calls, and any vendor-specific feature come from your vendor and kernel, not from Superior OS. On one phone those will be fine and on another they will not, even with the same image.

Build details, for the record: Android 13, generic system image, phh-treble, ARM64. GApps and Slim variants are available, Vanilla is not, so plan for a build that already includes Google apps. The maintainer is listed as @ChonDoe.

If getting ADB, fastboot and the driver onto your PC is the part that slows you down, the free Rom Flasher tool on GitHub does that part in a couple of clicks. It is free, and the link is in the downloads list.

::faq
Q: Why do I have to erase system before flashing a GSI?
A: A GSI replaces the system partition completely. Erasing first means nothing from the old system is left to conflict with the new image, which is what stops the build booting and then failing minutes later.

Q: What does the vbmeta command actually do?
A: It writes the vbmeta partition with verity and verification disabled, so the bootloader stops refusing an image it has not signed off on. A GSI is not signed like the stock system, so leaving those checks on gives you a boot loop.

Q: Will the camera and calls work on a GSI?
A: Those come from your vendor and kernel, not from Superior OS. The GSI reported no internal bugs, but camera quality, call audio and vendor features depend entirely on what your phone's vendor image provides.

Q: Can I skip unlocking the bootloader?
A: No. Unlocking comes first, and fastboot has to see the phone before any command works at all. Unlocking also wipes your data, so back up before you start.

Q: What is fastbootd and why does it matter?
A: It is userspace fastboot, entered with a reboot command from the bootloader. It can write logical partitions, and system is one of those on a modern phone. If you are not in fastbootd, system operations fail.

Q: Why is the first boot taking so long?
A: A GSI builds its system on first boot against your vendor, so it is slower than a normal ROM. Give it several minutes on the logo before you assume something failed, and do not interrupt it.
