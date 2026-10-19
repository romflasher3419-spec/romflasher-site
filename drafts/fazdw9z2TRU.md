::summary
CrDroid v12.2 is on the Poco X7 Pro with an Android 16 base, and it is my favourite ROM family for a reason. The flash is a fastboot-then-sideload job: flash vendor_boot to both slots, boot the CrDroid recovery, factory reset, then sideload the ROM zip. A clean flash is mandatory, and you should back up your IMEI before you start.

::body
CrDroid keeps earning the top spot for me. This is the build I reach for first, and v12.2 on the Poco X7 Pro with an Android 16 base is a good example of why.

So this one is the install, done properly, followed by being straight about the small annoyances. Because there are some. There always are.

## What you get

A Vanilla build, signed, with SELinux enforcing. That combination matters. You get a clean base with nothing pushed on top, and you decide what goes onto it afterwards.

- Vanilla — no bundled extras deciding things for you.
- Signed — the build is properly signed, not a loose unsigned package.
- SELinux enforcing — the normal, secure configuration rather than a tinkered one.
- Android 16 base under CrDroid's own layer of customisation.

## What you need before you start

- **ADB fastboot tool** and the **ADB fastboot driver** installed on your PC, working, before the phone ever goes into bootloader mode.
- An unlocked bootloader.
- The CrDroid v12.2 ROM zip on your PC, ready to sideload.
- A backup of your data and **a backup of your IMEI**. Clean flash is mandatory here, and that is not a formality.
- A cable that is not falling apart.

## Step 1 - enable USB debugging and connect

Connect the phone, enable USB debugging, and confirm your PC can see it. If the driver is not installed yet, do that now. Trying to sort out drivers while the phone is sitting in bootloader mode is a worse evening.

## Step 2 - reboot to bootloader

Reboot the phone into bootloader from the tool. Run `fastboot devices` to confirm. You want a serial number back, not an empty line.

## Step 3 - flash vendor_boot to both slots

This is the step that decides whether the recovery comes up. Flash vendor_boot to both slots, exactly as the instructions say. Flashing one slot and hoping is how people end up staring at a boot logo.

## Step 4 - boot the CrDroid recovery

Boot into the CrDroid recovery. This is the recovery that comes with the build, not a separate one you went and found.

## Step 5 - factory reset

Do the factory reset in recovery before you sideload. Not after. Sideloading before the wipe is the classic route to a phone stuck on the logo, and it is a completely avoidable one.

## Step 6 - sideload the ROM zip

Apply the update over ADB and sideload the ROM zip. Let it finish without touching anything. Skip any extra files unless you specifically want root — they are not needed for a working install.

## Step 7 - reboot to system

First boot takes a while. Let it. Then you are on CrDroid with a clean base and your own choices ahead of you.

## What is broken or fiddly

Two things, both fixable in seconds once you know them.

- **The Aperture video-recording glitch.** Aperture has a problem recording video, and the fix is shown in the video. It is quick, but it is not something you would guess.
- **The blur in recents.** Recents looks wrong because of a blur. Go into the launcher settings and set image transparency to 0 and it clears up.
- **FP jiiov.** The fingerprint reader using the jiiov sensor is likely still not working. Check which sensor your unit has before you commit, because this one is not a settings fix.

## Who should install it

Install it if you want a clean, signed, properly secured base that you then build on. Install it if you have flashed before and you accept a mandatory clean flash and an IMEI backup as the cost of entry.

Skip it for now if your fingerprint reader matters more to you than the ROM does and your unit uses the jiiov sensor. Skip it if a dirty flash is what you were hoping for — that is not on offer here.

The recents blur and the Aperture fixes are both quick once someone tells you what they are. That is most of what makes the first day with a new build annoying, and it is the part the video covers.

If the driver side of this is the bit you dread, the free Rom Flasher tool on GitHub installs the ADB and fastboot driver in a couple of clicks so you are not hunting through Device Manager while a phone sits in fastboot. It is free, and the link is in the downloads section.

## Before you commit

Back up your IMEI. I will keep saying it. A clean flash is mandatory, and a backup costs you five minutes now and a weekend if you did not take it.

::faq
Q: Do I need a clean flash for CrDroid v12.2 on the Poco X7 Pro?
A: Yes, clean flash is mandatory here. This build is on an Android 16 base, and dirty flashing across an Android base is how you end up with a phone that will not boot. Wipe before you sideload, not after.

Q: What is the Aperture video recording bug?
A: Aperture has a glitch when recording video. It does not fix itself with a settings change you would find on your own, and the fix is shown in the video. Once applied, video recording works normally.

Q: How do I fix the blur in recents?
A: Go into the launcher settings and set image transparency to 0. That clears the blur in the recents view. It is a settings change, not a build problem.

Q: Will the fingerprint reader work?
A: It depends on your sensor. FP jiiov is likely still not working on this build, so check which fingerprint sensor your unit has before you flash. Other configurations may behave differently.

Q: Do I need to back up my IMEI before flashing?
A: Yes. It is worth doing every time, and especially here since a clean flash is required. Losing IMEI data is a much bigger problem than losing your photos, and a backup takes only a few minutes.
