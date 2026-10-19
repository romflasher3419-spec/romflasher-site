::summary
RiceDroid on Android 13 is a heavily customisable AOSP build for the Xiaomi 11T Pro. You flash it with fastboot and a recovery: unlock the bootloader, format data in recovery, flash the ROM, add GApps if you want Google services, then boot. Stock MIUI's camera processing and the Xiaomi extras do not come with it, so expect to set the phone up yourself.

::body
RiceDroid is the ROM you pick when stock software feels like it keeps deciding things for you. There is a switch for almost everything, and the whole interface bends until it matches how you actually use the phone. That is the point of it.

The cost is the usual AOSP trade. You leave behind Xiaomi's camera processing and the MIUI extras, and you build the experience yourself instead of inheriting it.

## What this ROM actually is

A clean AOSP base sitting under a deep pile of options. Launcher, status bar, quick settings — all of it can be reshaped. Out of the box the setup stays close to plain Android, and nothing is forced on you until you go and change it. Security patches follow the source as it updates.

If that sounds like work, it is a little. If it sounds like fun, this is your build.

## What you need before you start

- The **ADB and Fastboot driver** installed on your PC. If Device Manager shows an unknown device, fix that before anything else.
- **Platform Tools** extracted somewhere you can find them.
- A **recovery** for the 11T Pro. TWRP or OrangeFox both work here — pick one and stick with it.
- **vbmeta** for the AOSP build, in case the package you download asks for it.
- A full backup and a battery above 50%.

## Step 1 - unlock the bootloader if it is not already done

Unlocking wipes the phone, and you have to wait out the unlock timer, so do this days before you actually plan to flash. If your bootloader is already unlocked, skip straight ahead. Nothing later works while it is locked.

## Step 2 - driver, cable, and confirm fastboot sees the phone

Install the driver, plug the phone in, and reboot it into fastboot mode. Run:

`fastboot devices`

You want a serial number and the word `fastboot`. No serial number means the driver is not working, and no amount of retrying the flash will fix that. Sort it out now.

## Step 3 - boot recovery and format data first

This is the step people skip and it is the one that costs them the evening. Boot into your recovery, then format data before you flash anything. Flashing the ROM first and wiping after gives you a boot that looks fine for a minute and then falls over.

Format data. Not just wipe. Format.

## Step 4 - flash the ROM, then GApps if you want Google

Flash the ROM package from recovery. If your build needs vbmeta, flash that too, in the order the package tells you to.

Then decide about Google services. If you want the Play Store and the rest of it, flash a GApps package right after the ROM, in the same recovery session. Skip it and you will boot into a phone with no Play Store and no obvious way to get one.

## Step 5 - reboot to system and set up from scratch

First boot takes a while. Longer than you expect, and it may sit on the logo for a few minutes. Let it. Then you get the setup wizard and a phone that is yours to shape.

## Where people get stuck

- **Flashing before formatting data.** You will boot, everything looks great, and then it falls over. Format first, always.
- **Skipping GApps.** Then wondering where the Play Store went. It does not come back on its own — you flash it, or you do the whole job again.
- **Missing the firmware requirement.** An Android 13 build wants the right firmware under it. Check what your device tree asks for before you flash a newer base on top of old firmware.

## What you should know before committing

The camera is the honest one. Xiaomi's processing does not come with an AOSP build, so photos will look different — not worse in every light, but different, and you may not like it in low light. If the camera is why you bought the phone, think about whether that trade suits you.

Also expect a couple of evenings of setup, not one. The ROM gives you the options; you still have to pick.

If the driver and platform tools side of this feels like the annoying part, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks so you are not hunting through Device Manager. It is free, and the link is in the downloads section.

## One last thing

Do a full boot and finish the setup wizard before you start restoring anything. If something is going to break, you want it breaking on an empty phone, not on top of two hours of restored files.

::faq
Q: Does flashing RiceDroid wipe my data?
A: Yes. Moving from MIUI onto an AOSP build means a data wipe, and you should format data in recovery anyway before you flash. Copy your photos, downloads and anything you care about off the phone first, and expect the setup wizard on first boot.

Q: Do I need to install GApps separately?
A: Yes, if you want Google services. RiceDroid ships as an AOSP build without the Play Store. Flash a GApps package right after the ROM, in the same recovery session, or you will boot into a phone with no Play Store.

Q: Will the Xiaomi camera still work after flashing?
A: The camera app still opens, but Xiaomi's image processing does not come with an AOSP build, so photos will look different from stock MIUI. Some people are fine with it, some are not — try it before you make the phone your daily.

Q: Do I need to flash vbmeta?
A: Only if the package you download asks you to. Some AOSP builds on this device need a vbmeta image flashed to clear verification, others do not. Read the notes that come with your download and follow them.

Q: Can I go back to stock MIUI later?
A: Yes. A fastboot ROM for your exact model plus platform tools will put stock MIUI back. Going back means another data wipe, so plan for it the same way you plan the flash.
