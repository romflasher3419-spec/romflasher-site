::summary
HyperOS 4 on the Indian POCO X7 Pro keeps the Google Play Store working and the integrity checks passing, as long as you flash the official Indian base image before the HyperOS 4 package. Skip the base and Play Store and integrity misbehave. This is the Indian variant, so files from another region are not an option.

::body
You want HyperOS 4 on the Indian POCO X7 Pro, and you want Play Store still opening afterwards. That combination is the whole point of this install. It is not a Chinese build, it is not a stripped-down package, and you should not have to give up Google services to get the new look.

The thing that decides whether you keep Play Store and pass integrity is the order, and specifically one step people skip. Flash the official Indian base first, then the new package on top. Do that and the phone comes up the way it should.

## What you need

- POCO X7 Pro, Indian variant. This matters more than anything else on this list.
- The official Indian ROM or a recent HyperOS 3 build for your device, to use as the base.
- USB debugging switched on in Developer Options.
- A PC or a second Android phone to drive the flash.
- The HyperOS 4 files shown in the video. Nothing pulled from another device.

Read that last line again. This is the Indian variant, and files from another region are exactly how a perfectly good phone ends up bricked beyond what a normal flash can fix.

## Step 1 - back up everything

This wipes the phone. Photos, documents, chat backups, anything tied to your accounts that is not syncing. Do it before you touch Developer Options, because once the flash starts there is no stopping for a minute to copy files across.

## Step 2 - turn on Developer Options and USB debugging

Tap the MIUI version in Settings a handful of times to unlock Developer Options, then go in and switch on USB debugging. Connect the phone and let your PC or the tool push it into fastboot when you are ready.

## Step 3 - flash the official Indian base image first

This is the step that keeps Play Store working and integrity passing. Flash the official Indian base before anything else. People skip this because they assume the new package covers it, and then they wonder why Google services behave strangely or why the phone will not come up properly.

The base gives the device the right starting point. Build on top of something random and you are asking for trouble you will not enjoy cleaning up.

## Step 4 - flash the HyperOS 4 package

With the base on, move on to the HyperOS 4 files and let the flash finish. Do not unplug the cable, do not close the window, and do not hurry the phone. When it is done, you have the new build written.

## Step 5 - first boot and normal setup

This is the slow part. The first boot after a jump like this takes a while. Let it sit and do not decide after a minute that it has gone wrong. When it comes up, set the phone up normally. Play Store and Google services are there from the start, because you flashed the right base.

## Step 6 - turn on Advanced Textures

Once you are in, open Settings and switch on Advanced Textures. That gives you the soft glass and frosted glass look that the new build is known for. It is a small toggle and it changes how the whole interface feels.

## Where people get stuck

- **Skipping the base.** Flash the new package on top of some random build and do not expect Play Store or integrity to behave. The base is the whole trick.
- **Wrong variant.** This is the Indian variant of the POCO X7 Pro. Files from another region are how you turn a working phone into a repair job.
- **Impatience.** The first boot is slow because of how much has changed underneath. Let it finish on its own.

## One honest note

Unofficial previews and finished public releases are not the same thing, so if a feature you saw in a video is not there in your build, that is normal and not something you did wrong. Check where the public update stands for your device before you decide a feature is missing. Nothing about flashing changes that.

If the driver and setup side is the part you dread, the free Rom Flasher tool handles the ADB and fastboot driver install so you can get to the flash without fighting Device Manager. It is free, and the link sits in the downloads section with the HyperOS 4 files.

::faq
Q: Is this a Chinese ROM for the POCO X7 Pro?
A: No, and that is the point of this build. It is the Indian variant, and Play Store stays intact. That is exactly why flashing the official Indian base first matters.

Q: Will Google Play Store work after flashing HyperOS 4?
A: It should, as long as you flash the official Indian base image before the new package. Skipping the base is the usual reason Play Store and integrity checks misbehave afterwards.

Q: Will I lose my data installing HyperOS 4?
A: Yes. This wipes the phone, so back everything up before you start. There is no way to keep internal storage when the base is replaced.

Q: Why is the first boot taking so long after flashing?
A: The first boot after a jump like this is genuinely slow because so much has changed underneath. Let it finish without tapping the screen or pulling the battery.

Q: Can I use files from another region on my Indian POCO X7 Pro?
A: Do not. This guide is for the Indian variant specifically. Files for another region can write partitions your phone cannot boot from, which turns a normal flash into a brick.
