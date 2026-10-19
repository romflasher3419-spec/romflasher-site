::summary
BananaDroid on the MI 11X is an unofficial Android 12L build for the alioth platform, which means it is a community release rather than an official device drop. Here is the full flash walkthrough, plus what the ROM actually gives you once it boots.

::body
Sometimes you do not want the ROM everyone is posting about. You want the one nobody has tried yet, boot it up, and see what happens. BananaDroid on alioth is that kind of pick. It is unofficial for this device, and that word is worth understanding before you flash.

Unofficial does not mean broken. It means this build comes from a community developer rather than the ROM team's own device list. Nobody signed off on it as an official release for the MI 11X, POCO F3 or Redmi K40. That is not a reason to skip it. It is a reason to read the release post properly and keep a backup ready.

## What you need before you start

- An unlocked bootloader on the alioth.
- A custom recovery that can handle an Android 12L zip. An old recovery will fail on the first step and send you hunting for the wrong problem.
- The BananaDroid build for alioth specifically. Not a build for a similar-sounding device.
- Firmware that matches the base the build expects. Unofficial builds are often pickier here than official ones.
- A full backup, because a clean flash wipes you clean.

## Step 1 — move the ROM zip into internal storage

Keep the zip on the phone, in internal storage. If the build asks you to format data after the flash, you will have a recovery session where your PC connection is not available, and a zip sitting on your desktop is useless at that point.

## Step 2 — boot into recovery and back up first

Always first. Take a full backup of system and data before you wipe anything. With an unofficial build this matters more, not less — you are the only test lab this build has.

## Step 3 — wipe data, cache and Dalvik

Clean flash. Wipe data, cache and Dalvik. If you are coming from another ROM on a different Android base, this is not optional, and neither is the format afterwards.

## Step 4 — flash the ROM zip

Flash it and let it finish. Do not touch the phone, do not unplug anything, and do not take the silence at the end of the progress bar as a failure.

## Step 5 — format data if the build asks

If the installer asks for a data format, do it. This is usually about the encryption setup changing. Refusing the format is the number one reason people sit and stare at a looping boot animation.

## Step 6 — reboot and wait out the first boot

The first boot on a clean flash of an unofficial build is slow. Give it the time it needs. The setup wizard will appear when it is ready.

## Step 7 — use it for a day before deciding

Do not make a call on this ROM in the first hour. Run setup, install your normal apps, and live with it for a day. Battery readings in the first few hours mean nothing because the phone is still settling.

## What BananaDroid actually gives you

It is an Android 12L base, so the core is the Android 12 feature set. Themed system colours that pull from your wallpaper, the updated notification shade and quick settings, and the privacy indicators in the status bar that tell you when an app is using the camera or microphone.

On top of stock Android 12L, BananaDroid adds its own customisation layer. That is where it differs from a bare AOSP build:

- A customisation section in settings for the status bar, quick settings and lock screen.
- Gesture options that go a bit further than the stock set.
- Its own accent-colour handling, separate from the standard Android theming.

The feel is light. There is no MIUI shell loading on top of everything, and on alioth that is most of the point.

What you should not expect is polish that matches a mainline ROM. An unofficial build might have a bug the official build already fixed. That is the trade you are making, and it is a fair one as long as you know.

## Where people get stuck

- **Treating an unofficial build like an official one.** No backup, no reading the release post, then a bootloop with no way back. Back up first.
- **Mixing zips from a different device or a different firmware base.** The flash succeeds, the boot does not.
- **Expecting mainline polish.** An unofficial port or community build usually has rough edges. Some features may not work, and that is normal for this category.

## Who should install this

Flash BananaDroid if you enjoy trying builds that most people have not run, and you are comfortable rolling back when something does not work. If you want a ROM you can set up once and forget, take an official release for alioth instead. Both are valid. They are just different jobs.

Do keep one thing in mind: an unofficial build can stop getting updates without warning, because the developer is doing this in their own time. That is not a complaint about anyone, it is just how community builds work. Keep the zip you flashed somewhere safe so you can return to a known state.

If the flashing side of this is where you get stuck, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks so Windows actually sees the phone. It is free, and the link is in the downloads section.

::faq
Q: What does unofficial mean for a custom ROM?
A: It means the build comes from a community developer rather than the ROM team's own device list. Nothing is guaranteed by the main team, so read the release post carefully and keep a backup before you flash.

Q: Is BananaDroid safe to flash on the MI 11X?
A: It is a community build, so treat it that way. Flash it with a full backup on hand and a known-good zip you can roll back to. There is no official approval process behind an unofficial release.

Q: Which Android version is BananaDroid on?
A: This alioth build sits on the Android 12L base. That gives you the Android 12 feature set — themed colours, the updated notification shade, privacy indicators — plus a customisation layer added by the ROM.

Q: Do I need to wipe data before flashing BananaDroid?
A: Yes, and format data too if the installer asks. A clean flash is the only reliable way to move onto an Android 12L base, and skipping the data format is the most common cause of a bootloop.

Q: Can I go back to MIUI if I do not like it?
A: Yes. Download the fastboot package for your exact model and flash it from your PC. That wipes the phone again, so take anything you want to keep off it first.
