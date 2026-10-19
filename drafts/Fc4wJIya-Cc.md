::summary
STAG OS on the Redmi Note 5 Pro is a clean AOSP build running an Android 10 base, which is about as light as this 2018 phone gets. Here is how the flash goes on whyred, and an honest look at what the ROM actually delivers day to day.

::body
Android 10 on a Redmi Note 5 Pro sounds odd until you use it. The phone came with something much older, and here you are running gesture navigation and the newer notification handling on hardware from 2018. That is the appeal. If you want the cleanest software this phone can run, STAG OS is one of the builds people keep coming back to.

The MIUI skin is gone. There is no account nagging, no folder of preinstalled apps, no extra layer between you and the system. On a phone with limited memory, that is not a small thing.

## What you need before you start

- An unlocked bootloader on whyred. Unlocking wipes the phone, so do it before you set anything up.
- A custom recovery running on the phone. Get it working properly before anything else.
- The STAG OS zip built for whyred, on an Android 10 base.
- The firmware base the release post recommends. This matters on this device — flash the one it asks for.
- A full backup of internal storage and a battery above 60%.

## Step 1 — unlock the bootloader and get recovery working

Nothing else on this list happens before that. Unlock first, accept the wipe, then install a recovery for whyred. Test that recovery boots and can see your internal storage before you move on. If it cannot read storage now, it will not flash a zip later.

## Step 2 — take a full backup of system and data

Back up both. System, so you have something to roll back to, and data, so your files and app data survive. Copy the backup off the phone if you can. A backup that lives on the phone you are about to wipe is not a backup.

## Step 3 — wipe system, data, cache and Dalvik

Note the extra one here. This flash wipes system too, not just data. With an AOSP build on old hardware, a clean slate is the difference between a phone that settles down and one that misbehaves for days.

## Step 4 — flash the STAG OS zip

Flash the zip and wait. Do not interrupt it. If the release post for your build mentions a separate GApps package, decide now whether you want Google services at all — on a phone this old, skipping them leaves more memory free.

## Step 5 — wipe cache and Dalvik, then reboot

After the flash, wipe cache and Dalvik and reboot. Then leave the phone alone for the first boot. On this chipset it is not quick. Ten minutes of black screen before the setup wizard appears is within normal range, so don't panic.

## What it looks like once it boots

STAG OS stays close to stock Android, which is exactly what a phone this old needs. Extra features cost memory you do not have. So you get:

- A stock-style launcher with a normal app drawer and no skin on top.
- Android 10's gesture navigation, which on a small screen actually helps — you get the navigation bar space back.
- The Android 10 notification handling, including the focus mode and better per-app control.
- A settings app that looks like Android rather than like MIUI.

## What the honest bits are

- **The camera depends on the build.** Always test it before trusting it. Take a few shots in daylight and indoors, check the video recording works, and check that the camera App opens quickly. On whyred, camera stability is the point where builds separate from each other.
- **Heavy apps will feel the limits of this hardware.** No ROM fixes three gigabytes of RAM and an older chip. Social media apps, browsers with many tabs, anything that keeps a lot in memory — those are the ones that will stutter.
- **Firmware base matters.** Flash the recommended one if the release post says so. Skipping that step is where the strange bugs come from.

## Where people get stuck

- **Forgetting to wipe system.** Data only is not enough for a base change on this device.
- **A recovery that cannot read internal storage.** Fix it before flashing, not during.
- **Ignoring the firmware note.** It looks optional. It is not, and the symptoms show up later as random crashes and a warm phone.

## Who should install this

Flash STAG OS if you want the cleanest thing your Redmi Note 5 Pro can run and you accept that it will not become a fast phone. It will become a tidy one. Calls, messages, browsing, music, a few photos — all of that works, and it works without MIUI loading on top of everything.

If you are chasing performance for games, no ROM on this hardware is going to give it to you. If you want the Xiaomi camera processing back, remember what you are giving up.

One practical note before you start. If the bootloader unlock and driver side is what usually stops you, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks so Windows recognises the phone without a Device Manager hunt. It is free, and the link is in the downloads section.

::faq
Q: Is Android 10 too old to use on the Redmi Note 5 Pro?
A: For security patches, yes, it is well behind. For daily use it still runs fine — calls, messaging, browsing and music all work. Just go in knowing you are not getting current security updates.

Q: Do I need to flash GApps with STAG OS?
A: Flash it exactly the way the release post for your build describes. If it includes Google apps already, do not add a package on top. If it is a bare AOSP base, you can choose to skip GApps entirely and keep more memory free.

Q: Can I go back to MIUI after flashing STAG OS?
A: Yes. Download the fastboot package for your exact model and flash it from your PC. That resets the phone again, so move your photos and files off first.

Q: Why does the first boot take so long?
A: This is old hardware and a clean install with an empty cache, so the system needs time to build everything fresh. Ten minutes before the setup wizard appears is normal. Plug it in and leave it alone.

Q: Will the camera work properly on this ROM?
A: Test it before you rely on it. Camera behaviour on whyred depends on the build you flash and the firmware base underneath it, so take a few photos and try the video recording before making it your daily phone.
