::summary
Evolution X on the POCO X7 Pro is a clean Android 15 build, and the flash itself is short. The part people miss is the vendor image: flash the vendor first, then the ROM, or the phone sits on the logo or boots to a black screen.

::body
Evolution X is the ROM I keep coming back to because it stays close to stock Android without being boring about it. On the POCO X7 Pro the flashing job is genuinely short. The trap is not in the commands. It is in the order, and in one file people decide they can skip.

They cannot. This is the guide that works.

## What you need

- An unlocked bootloader on the POCO X7 Pro. This is the first step and it wipes the phone, so plan for it.
- The Evolution X ROM package for this device.
- The matching vendor image. Both files, not one.
- ADB and fastboot on your PC, with a driver that sees the phone.
- A full backup, because this wipes everything.

Do not grab a package built for a different device because the file name looked close enough. That is how a short job turns into a long evening.

## Step 1 - back up everything first

Photos, chats, downloads, the lot. Move them off the phone and check they actually arrived. Flashing wipes internal storage, and there is no undo for the things you forgot.

While you are here, write your IMEI down. It is the one thing you cannot recreate later.

## Step 2 - set up ADB and fastboot on the PC

Install the tools, connect the phone once it is in fastboot mode, and confirm the PC sees it before you do anything else:

`fastboot devices`

You want a serial number back. An empty line means the driver is wrong, and no amount of retrying the flash will fix that. Sort it now.

## Step 3 - boot the phone into fastboot

Boot the POCO X7 Pro into fastboot mode and connect the cable. Use a port directly on the PC, not a hub, and a cable that is not falling apart.

## Step 4 - flash the vendor image first

The vendor image goes on before the ROM, exactly as shown, and it has to match this build. This is the step people skip, and it is the single most common reason a phone ends up sitting on the logo or showing nothing at all.

Do the vendor first. Then move on.

## Step 5 - flash the Evolution X ROM

With the vendor in place, flash the Evolution X package. Let it finish writing before you touch anything. Recovery comes next.

## Step 6 - format data, then reboot

Boot into recovery and format data. Do this before the first boot, not after. Formatting data after the phone has already tried to boot is how you end up in a loop, wondering what you did wrong.

Then reboot to system.

## Step 7 - wait out the first boot

The first boot takes a few minutes, and it always takes longer than you expect. Leave the phone alone. Do not unplug it, do not hold buttons, do not assume it is stuck at the two-minute mark.

## Where people get stuck

- **Flashing the ROM without the vendor.** Black screen, every time. This is the one to remember.
- **Formatting data after the first boot instead of before.** That ordering loops the phone and forces a second attempt.
- **Using a package for a different device.** If the build is not for the POCO X7 Pro, stop. File names are not a compatibility test.

## One honest note before you start

Read the release notes for the exact build you download, and check whether Google apps are included or whether you have to sideload them yourself. Builds change between releases and the notes are the place that stays current.

Everything else about this flash is routine. Once it settles you land on a clean Android 15 build, restore your data and get on with your day.

If the driver setup is the part that keeps tripping you up, the free Rom Flasher tool handles ADB and fastboot installation for you.

::faq
Q: Do I need the vendor image to flash Evolution X?
A: Yes. The vendor image goes on first, then the ROM. Skip it and the phone usually sits on the logo or boots to a black screen.

Q: Does flashing Evolution X wipe my data?
A: Yes. The install wipes internal storage, and unlocking the bootloader already wiped it once. Back up your photos and chats before you begin.

Q: Should I format data before or after the first boot?
A: Before. Format data in recovery as part of the install. Doing it after the phone has tried to boot is what causes boot loops.

Q: Does this ROM include Google apps?
A: That depends on the specific build you download. Check the release notes before you flash, and sideload a GApps package if the build does not include them.
