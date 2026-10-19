::summary
This is Android 17 Canary running on the POCO X7 Pro (rodin) as a Pixel-style AOSP build, installed clean from fastboot. It boots, it looks like a Pixel and it feels quick once it settles, but GCam does not work on it and the Play Store certification fix is not optional.

::body
I pulled my daily phone off its usual ROM to test this, which should tell you how curious I was about an Android 17 Canary build on the POCO X7 Pro. Here is what it is, how it flashes, and where it hurts.

Short version: it is a Pixel-style AOSP build, not HyperOS with a coat of paint. Clean flash only. Never dirty flash this one over anything.

## What it looks like once it boots

The Pixel personality is all there. Google dialer and messages are in place, the wallpaper style is the Pixel default, and the home screen uses glass-style effects that only show themselves properly after the phone has finished doing its background work.

The animations land nicely. If you have used a Pixel, you will find the layout instantly familiar, and the differences are small touches rather than a different phone.

## How the install runs

The package gives you three routes: an installer batch file for Windows, a script for Linux, and an Android route if you want to flash straight from the phone with Termux instead of a PC. I went with the PC route because it is easier to watch what is happening.

The shape of it is the same as any AOSP build on this phone:

- Unlock the bootloader if you have not already, and accept that it wipes the phone.
- Put your platform tools, the ROM package and the images in one folder so nothing is missing at the wrong moment.
- Boot to fastboot and confirm the PC sees the device before you flash anything.
- Run the installer batch file and let it work through the images in order.
- Boot into recovery when it tells you to, format data, and let the ROM install.
- Flash the certification and integrity fix right after the ROM, before you sign into anything.

Do it as a clean flash. A dirty flash on a base this new is asking for a boot loop you will spend the evening undoing.

## The first ten minutes

Right after first boot, everything feels a little laggy. Resist the urge to judge it. The system is downloading and restoring apps in the background, and it needs roughly ten to fifteen minutes to finish that. Once it does, the glass-style effects on the home screen show up properly and the general smoothness arrives.

If you start swiping around and call the build slow at minute two, you are measuring the setup, not the ROM.

## What works and what is broken

This is the honest section, and it is why you read these things.

- **Open Camera works.** It opens, it shoots, no drama.
- **GCam does not work on this build.** If a Google camera port is the reason you flash ROMs, that is a real dealbreaker and you should wait.
- **Google dialer and messages are in place.** Calls and texts feel like a Pixel.
- **Play Store certification needs the fix.** Flash the integrity and certification patch straight after the ROM, or the Play Store keeps complaining at you.

## Who should install it

Treat a Canary build like a Canary build. The Pixel feel is there and the animations land nicely, but you are on an early base and small things show it.

Install it if you can live without GCam and you are comfortable flashing the certification fix in the same session. Install it if you want to spend a day seeing where Android is heading on this hardware. Do not install it as your only phone if a broken camera app would ruin your week.

For the PC side, the free Rom Flasher tool covers the ADB and fastboot driver setup, so the batch file has a phone it can actually talk to.

::faq
Q: Can I dirty flash the Android 17 Canary build?
A: No. This one needs a clean flash every time. Dirty flashing on a base this new is a fast route to a boot loop, and you will end up formatting data anyway.

Q: Is GCam working on this ROM?
A: Not on this build. Open Camera works fine and is the sensible replacement for now. If GCam is essential to you, wait for a later release before flashing.

Q: Do I need a PC to install it?
A: A PC is the easier and better-tested route, using the installer batch file. There is an Android install option as well if you flash from the phone itself, but the PC path is the one I would follow first.

Q: Why does the phone feel slow after first boot?
A: The system is still installing and restoring apps in the background. Give it around ten to fifteen minutes, then judge the smoothness. The home screen effects also settle in once that background work is done.

Q: Do I have to flash the integrity and certification fix?
A: Yes. It is not optional on this build. Flash it right after the ROM, or the Play Store will keep complaining and some apps will refuse to work properly.
