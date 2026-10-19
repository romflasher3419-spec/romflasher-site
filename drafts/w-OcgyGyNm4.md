::summary
RisingOS-Revived 8.1.1 is booting on the Poco X7 Pro with an Android 16 base. It is a Gapps build, signed, with SELinux enforcing, and the flash goes fastboot to recovery to ADB sideload. The notification panel is the standout, while the Aperture video glitch and the jiiov fingerprint sensor are the two things to know before you commit.

::body
RisingOS-Revived 8.1.1 is up and running on my Poco X7 Pro, on an Android 16 base. This is the full flash plus what I actually found once it came up, including the parts that are not perfect.

Because it is the initial build, the changelog is short and gaming-focused. The ROM reads that way too: fresh, quick, and not yet full of extras. That is not a criticism. It just tells you what you are getting.

## What it looks like

Set up clean, it boots straight into RisingOS. No loops, no drama, and the first setup goes through without a fight.

The notification shade is where this ROM shines. Volume and brightness controls sit right in the panel, which sounds like a small thing until you use a build that puts them somewhere else. The whole panel looks sharp and the layout is the kind of thing you notice immediately and then never think about again, which is the correct outcome.

## What I tested

- **Boot and first setup** — clean install, no loops, straight into RisingOS.
- **Notification shade** — the strong point. Volume and brightness in the panel, sharp throughout.
- **Navigation gestures** — responsive, with no stutter when switching modes.
- **Camera** — Aperture has a video glitch, and the fix is shown on camera.
- **Fingerprint** — for the jiiov sensor it is likely still not working.
- **Play integrity** — worth checking against your own setup, since it depends on what you have installed.

## What you need before you flash

- This is a **Gapps build**, signed, with **SELinux enforcing**. A normal, secure setup rather than a tinkered one.
- **Clean flash is mandatory.** Dirty flashing across an Android base is how you get a paperweight.
- **Back up your IMEI.** I say it every time and I mean it every time.
- **ADB fastboot tool and drivers installed** before the phone is in bootloader mode. Sort the driver out on a working phone, not on one sitting in fastboot.

## How the flash goes

1. Connect the phone and enable USB debugging.
2. Reboot to bootloader from the tool.
3. Flash vendor_boot to both slots.
4. Boot into the Rising recovery.
5. Factory reset, then apply update over ADB.
6. Sideload the ROM zip — skip the extra files unless you want root.
7. Reboot to system.

Both slots on step 3. Not one. That step is where the recovery either comes up or does not.

## What is broken

- **The Aperture in-video recording glitch.** Recording video has a problem, and the fix is covered in the video. It is not something you would stumble onto.
- **FP jiiov.** The fingerprint reader with the jiiov sensor is likely still not working on this build. Check your unit before you get invested.
- Anything else — tell me. Send logs rather than a one-line complaint, and it is much easier to work out what happened.

## The verdict

It is a comfortable daily ride if you can live with the two known issues. The notification panel is the best part of it, the base is clean and properly secured, and it moves well.

If the jiiov fingerprint sensor is what your unit has and you rely on it, think hard before flashing. That is the one issue here that is not a settings tweak.

If the Aperture glitch is your only concern, install it. That one has a fix and the fix is quick.

## Who should install it

Install it if you want a fresh, fast build that has not been loaded up with extras yet, and if your fingerprint reader is not the jiiov one. Install it if a clean flash and an IMEI backup are just part of your routine at this point.

Wait if you have already got a settled daily driver and you do not enjoy being early. There will be more builds of this, and the changelog will get longer.

If the driver side is what puts you off, the free Rom Flasher tool on GitHub installs the ADB and fastboot driver in a couple of clicks. It is free, and the link is in the downloads section.

One note on Play integrity: do not take my result as yours. It depends entirely on what you have installed and how your setup is configured, so check it on your own phone after the flash.

::faq
Q: Does RisingOS-Revived 8.1.1 wipe my data?
A: Yes, and a clean flash is mandatory on this build. Dirty flashing across an Android base is how you end up with a device that will not boot. Back up your data and your IMEI before you start.

Q: Does the fingerprint reader work on this build?
A: It depends on your sensor. For the jiiov sensor it is likely still not working, so check which fingerprint reader your unit uses before flashing. This is not something a settings change will fix.

Q: How do I fix the Aperture video recording glitch?
A: The fix is applied through the steps shown in the video. Aperture has a problem recording video on this build. Once you follow it, video recording works normally.

Q: Is this a Gapps build?
A: Yes. RisingOS-Revived 8.1.1 is a Gapps build, signed, with SELinux enforcing. That means Google services are already in it and you do not need to flash a separate package after the ROM.

Q: Will Play Integrity pass?
A: That depends on your own setup and what you have installed, so check it yourself after flashing rather than going by someone else's result. It is worth testing once the phone is set up the way you want it.
