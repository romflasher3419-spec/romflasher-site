::summary
LineageOS on the Xiaomi 11T Pro as a GSI is an Android 11 build that flashes through fastboot in a fixed order: enter fastbootd, flash vbmeta with verity and verification disabled, erase system, flash the system image, reboot to recovery, wipe data. This build merges the September security patches, updates the phh sources, and removes the livelock daemon.

::body
Lineage on a GSI is a different animal from a device-specific Lineage build. Everything is generic on purpose, which is the point. It is light, predictable and boring in the best way. It is also the version I keep coming back to when a phone starts feeling slow.

Here is the honest framing before the commands. A GSI rides on your vendor and kernel, not on the ROM. That means the ROM can be perfectly stable while your camera still behaves oddly, and it means two people with the same image can have completely different experiences. Lineage is not at fault for that, and no amount of reflashing fixes it.

## What is in this build

- Android 11, with September security patches merged in.
- Updated to the latest phh sources.
- The livelock daemon, llkd, removed. This is the interesting one. It is the plausible fix for the random freezes that used to hit some setups.
- Known bugs inside the ROM: none listed.
- SELinux: works both in enforcing and permissive.

That llkd change is worth pausing on. Livelock detection is meant to catch a hung process and restart it, but on some configurations it starts killing things it should not, which shows up as a random freeze or a reboot with no pattern. Removing it is the kind of fix you do not notice for weeks, and then one day you realise the phone has stopped doing the thing.

## What you need

- An unlocked bootloader, and a phone that is Treble ready. The 11T Pro is.
- The LineageOS GSI image, built for ARM64. All architectures are published for this one, so pick the right one for your device rather than grabbing the first file you see.
- The vbmeta file. A GSI flash needs it.
- Platform Tools on the PC.
- A backup, because the wipe at the end clears your data.
- A plan for Google apps. This is a vanilla build only. There is no GApps variant, so you flash Google services separately if you need them.

## Step 1 - boot to fastboot and check the PC sees the phone

Get into fastboot mode and run:

`fastboot devices`

You need a serial number back. No serial number is a driver problem, and it will not fix itself later. Sort it out now.

## Step 2 - move into fastbootd

`fastboot reboot fastboot`

System is a logical partition on this device, so you need userspace fastboot to write it. If a command later says the partition does not exist, you are still in the bootloader fastboot and you need this step again.

## Step 3 - flash vbmeta with the checks disabled

`fastboot --disable-verity --disable-verification flash vbmeta <vbmeta file>`

Do this exactly like this, with both flags in the same command. Without them the bootloader refuses the unsigned system image and you get a boot loop before you have even started.

## Step 4 - erase system

`fastboot erase system`

A GSI replaces system entirely, so start from an empty partition. This one is quick.

## Step 5 - flash the system image

`fastboot flash system <system image>`

This takes longer than the other steps. Let it run to the end and do not interrupt it while the progress looks stuck.

## Step 6 - reboot to recovery

`fastboot reboot recovery`

Recovery, not system. You need to wipe from here.

## Step 7 - wipe data and reboot

In Mi Recovery, run the wipe data option. Then reboot to system and let it settle. First boot on a GSI takes longer than a normal ROM, so give it the time.

## Where people get stuck

- **The vbmeta line.** Skipping it or leaving the flags off is the number one cause of a boot loop on a GSI install.
- **Vanilla means vanilla.** People flash this expecting Google apps to be there. They are not. Set aside time for a separate GApps flash if you need them.
- **Blaming the ROM for hardware.** If the camera is a step behind or a vendor feature is missing, that is your vendor and kernel, not Lineage. Reflashing the same image changes nothing.
- **Rushing the first boot.** Do not force a restart while the logo is still there. Wait it out.

## Who should install it

If you want the cleanest, least dramatic Android experience on a Treble phone, this is it. No bloat, no theming, nothing extra running in the background. The llkd removal is exactly the kind of fix that matters months later, when a phone would otherwise start freezing at random and you would have no idea why.

The costs are real too. Hardware features are your phone's problem, not Lineage's, and because this is vanilla you will spend an extra stretch of time getting Google services in before the phone feels like a normal daily driver.

If the ADB and fastboot driver setup is where you always lose time, the free Rom Flasher tool on GitHub handles that part in a couple of clicks, and the link is in the downloads list.

::faq
Q: Does LineageOS as a GSI need vbmeta?
A: Yes. Flash vbmeta with verity and verification disabled in the same command, before you erase or flash system. Without it the bootloader rejects the unsigned GSI image and the phone loops instead of booting.

Q: Does this LineageOS GSI include Google apps?
A: No. It is a vanilla build and there is no GApps variant published for it. If you need Play Services, flash a matching Google apps package separately after the ROM is in place.

Q: What is llkd and why was it removed?
A: llkd is the livelock daemon, used to detect and recover from a hung process. On some setups it kills things it should not, which shows up as random freezes. Removing it is the likely fix for those, and this build does exactly that.

Q: Will the camera work properly on a LineageOS GSI?
A: Camera quality and vendor features come from your vendor and kernel, not from the GSI. The ROM reported no internal bugs, but hardware behaviour depends on your device setup, so do not judge the ROM by the camera.

Q: Can I flash this on a phone that is not Treble ready?
A: No. A GSI needs a Treble-ready device with the right vendor interface. On a phone that is not ready, the image either will not boot or will boot without working hardware.

Q: How long does the first boot take after flashing a GSI?
A: Longer than a normal device-specific ROM, because the system is building itself against your vendor. Give it several minutes on the logo and do not force a restart in the middle of it.
