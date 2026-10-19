::summary
SuperiorOS Phoenix on the Redmi Note 5 Pro is a clean AOSP build for whyred, and it runs lighter than MIUI ever did on this phone. Here is the flash walkthrough, plus what actually works and what the camera does when you push it.

::body
There is a point in an old phone's life where the best thing you can do is strip it back. SuperiorOS Phoenix is that move on the Redmi Note 5 Pro. It brings a clean AOSP build to whyred, and it runs better than you would expect from a 2018 handset.

This is a mix of the flash steps and the test results, because both matter here. The install is short. The interesting part is what the ROM does on a daily basis, and specifically whether the camera holds up, since that is the usual weak spot on whyred.

## What you need before you start

- An unlocked bootloader on whyred. This wipes the phone as part of the unlock, so do it first.
- A custom recovery installed and working. Test that it sees your storage.
- The SuperiorOS Phoenix zip built for whyred.
- The firmware base the release post recommends, if it names one.
- A full backup of system and data, copied off the phone where possible.

## Step 1 — unlock the bootloader

Nothing on this page happens before that. Unlock, accept the data wipe, and set the phone up again only after the ROM is flashed.

## Step 2 — install a recovery and verify it

Install recovery for whyred, then boot into it and check that it can read internal storage. If it cannot, that is a recovery problem, and flashing a zip now will only fail in a confusing way.

## Step 3 — back up system and data

Back up both. System gives you a way back, data gives you your files. Move the backup off the phone if you have somewhere to put it.

## Step 4 — wipe system, data, cache and Dalvik

System too, not just data. On this device, a base change with old system partitions left in place is how you get strange bugs that are hard to trace afterwards.

## Step 5 — flash the SuperiorOS Phoenix zip

Flash it and let it complete. If the release post for your build asks for a separate GApps package, decide now whether you want Google services at all — on a phone with limited memory, skipping them frees up a useful amount.

## Step 6 — wipe cache and Dalvik and reboot

Wipe cache and Dalvik, then reboot. The first boot takes a while on this chipset. Several minutes before the setup wizard appears is normal, so leave it alone and let it finish.

## What I checked

- Boot time and how smooth the system feels on old hardware.
- Whether the camera app actually works, including basic photo and video.
- Battery drain across a normal day of use.
- Fingerprint unlock and the usual sensors.
- How warm the phone gets when you push it with games.
- The extra settings SuperiorOS adds on top of AOSP.

## What the results look like

The system is light and it shows. Scrolling through the launcher, opening settings, moving between apps — all of it is more responsive than MIUI was at the end of its life. That is mostly because there is far less running in the background.

Fingerprint unlock and the standard sensors work normally. Nothing surprising there, and that is a good sign on a build this old.

Battery drain over a normal day is reasonable for this phone. It is not a transformation, but a lighter system means less work in the background, and you feel that at the end of the day.

Thermals are the one to watch when gaming. Push it and the phone gets warm, and then it slows down. That is the hardware limit showing through, not the ROM.

## What is broken or rough

- **The camera is the point where builds separate.** On whyred, the lineage of camera fixes in the build matters more than the version number printed on it. Test it properly: daylight, indoors, and a short video clip. If it opens slowly or crashes, that build is not for you.
- **Some apps want more memory than this phone comfortably has.** You will notice it with heavy social and browser use. Keep what you install to the apps you actually use.
- **VoLTE is not guaranteed.** Test it on your carrier before you make this your daily phone, because if your carrier needs it and it does not work, you will find out at the worst time.
- **Leaving MIUI means leaving its camera processing behind.** That is a real trade, not a minor one, and it is worth deciding about before you wipe.

## Who should install this

Flash SuperiorOS Phoenix if you want a clean AOSP build on an old phone that still has some life in it. It is lighter, tidier, and it does not nag you about accounts or push services you never asked for.

Keep a known-good zip and a recent backup so you can roll back. On a device this old, being able to undo a bad flash in twenty minutes is the whole difference between a fun evening and a lost one.

If you want the Xiaomi camera back, or you need VoLTE and yours does not hold up, go back to MIUI and stop worrying about it. There is no prize for running a custom ROM on a phone this old.

For the unlock and driver side, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks so Windows recognises the phone without you hunting through Device Manager. It is free, and the link is in the downloads section.

::faq
Q: Is SuperiorOS Phoenix official for the Redmi Note 5 Pro?
A: Check the release post for the exact build you download. Builds for this device move between official and community-made over time, and the post will tell you which one you are looking at.

Q: Does VoLTE work on this ROM?
A: Test it on your own carrier before you rely on the phone. VoLTE support varies between builds on whyred, and finding out it does not work after you have made it your daily phone is a bad way to learn.

Q: Is it better than MIUI on this phone?
A: Lighter, yes. Cleaner, yes. The camera processing from MIUI is not something you get back though, so if you depend on the Xiaomi camera look, that is the trade you are making.

Q: Why does the first boot take so long?
A: Old hardware plus a clean install means the system builds everything fresh on that first start. Several minutes before the setup wizard appears is normal. Plug the phone in and let it finish.

Q: Will games run well on it?
A: Light games are fine. Demanding ones will heat the phone and slow it down, because that is the limit of this hardware rather than the ROM. A lighter system helps a little, but it does not turn this into a gaming phone.
