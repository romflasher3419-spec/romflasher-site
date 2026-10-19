::summary
Installing TWRP on the POCO X7 Pro is one fastboot command and one restart that has to go the right way. Unlock the bootloader first, back up your data, then flash the recovery image and boot straight into recovery so it sticks. Let the phone boot into Android first and the stock recovery can come back.

::body
Flashing a recovery is one of the low-risk jobs in this hobby, which is exactly why people rush it and then get confused. The flash itself takes seconds. The part that decides whether it works is what you do in the thirty seconds afterwards.

So before we start: unlock the bootloader, charge past 60%, and back up everything you care about. Not because the recovery flash is dangerous, but because unlocking the bootloader wipes the phone anyway. A backup is what turns a bad two minutes into an annoying afternoon instead of a disaster.

## What you need

- An **unlocked bootloader**. Without it fastboot will simply refuse the write, and there is no trick around that.
- **Battery above 60%**, and a period where you can leave the phone plugged in.
- A **full backup** of your data. Do it now, not later.
- The **TWRP image** for Rodin. Do not use an image built for another variant.
- A **PC with working ADB and fastboot** and the driver installed, so Windows actually sees the phone.

## Step 1 - unlock the bootloader and finish setup

Unlock the bootloader the proper way for your phone and let the phone complete its setup afterwards. This step wipes the device, which is why the backup comes before it. Do not skip ahead to the flash with a locked bootloader. The command will fail and it will look like the image is broken, when it is not.

## Step 2 - back up and charge

Copy your photos, downloads and files off the phone, and get the battery above 60%. I know it sounds like the boring instruction at the top of every guide. It is here because the flash ends with a reboot, and you do not want the phone dying during it.

## Step 3 - boot into fastboot

Power the phone off, then hold **Volume Down + Power** until the fastboot screen shows up. Connect it to the PC and check that it is visible:

`fastboot devices`

If the phone does not appear, sort the driver out before going further.

## Step 2 - flash the recovery image

With the phone in fastboot, run:

`fastboot flash recovery twrp.img`

The name on the left is the partition, so leave it as `recovery`. The name on the right is whatever you called the file you downloaded. If you are unsure, keep the file name short and simple before you run this, because a typo here is the difference between a flash and an error message.

## Step 3 - boot into recovery immediately

This is the whole job, right here. Do not let the phone boot into Android. Boot it straight into recovery, either with the key combination or with a fastboot command that sends it there. That forced boot is what makes TWRP stick.

If you let Android start up first, on some setups the stock recovery is put straight back and your next recovery boot looks like nothing happened. If that happens to you, do not panic. Nothing is broken. Boot to fastboot and go through steps 2 and 3 again.

## Step 4 - allow modifications

TWRP will ask whether to allow modifications to the system partition. Swipe to allow. If you plan to flash a ROM or flash anything else that writes to the system, you want that enabled.

## Where people get stuck

- **Booting into Android first.** This is the number one reason TWRP does not stick. Boot straight into recovery after the flash.
- **Trying it with a locked bootloader.** Fastboot will not accept the write, and it looks like the image is broken when it is not.
- **Skipping the backup.** Unlocking wiped the phone earlier, and the recovery setup itself is not the moment to discover you lost your photos.

## Common questions before you start

Do you need root for TWRP? No. An unlocked bootloader is the requirement, and that is it. Does the recovery flash wipe your data? No, the flash itself does not. The bootloader unlock is what wipes the phone, and that happens before this step. What is the usual thing that goes wrong? Booting into the system instead of recovery, which puts the stock recovery back. And can you flash a custom ROM after this? Yes. That is the normal next step, and TWRP is the tool that makes it easier.

## One honest paragraph

The recovery flash is quick, but it is not a no-risk job, and treating it as one is how people end up redoing it three times in an evening. The single habit that fixes almost every failure here is this: after the flash, get into recovery immediately, before anything else has a chance to boot.

If finding the ADB and fastboot drivers is the part that always eats your time, the free Rom Flasher tool installs them for you with a smart check, and it also handles recovery image flashes. It is free, and the link is in the downloads section.

::faq
Q: Do I need root to install TWRP?
A: No. TWRP only needs an unlocked bootloader. Root is a separate step you can do later if you want it.

Q: Does flashing TWRP wipe my data?
A: The recovery flash does not wipe anything. Unlocking the bootloader does, and you have to do that before this step, so back up before you unlock.

Q: Why does TWRP disappear and the stock recovery come back?
A: The phone booted into Android before it booted into recovery. Flash the image again and this time boot straight into recovery, without letting the system start first.

Q: What happens if I flash TWRP with a locked bootloader?
A: Fastboot refuses the write. There is no way around it. Unlock the bootloader first, finish the phone setup, then come back to the flash.

Q: Can I install a custom ROM after TWRP?
A: Yes, that is the usual next step. With TWRP in place you can wipe, sideload the ROM zip, and set the phone up from there.

Q: Which TWRP image should I use?
A: The one built for the POCO X7 Pro, codename Rodin. An image for a different variant can flash successfully and still leave you with a recovery that does not work properly.
