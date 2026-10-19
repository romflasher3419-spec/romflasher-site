::summary
Pixel Experience X on the Redmi Note 5 Pro gives you the clean Pixel look on whyred, with the extras people kept asking for. The interface side feels light and stays smooth. The hardware side will not change, so flash it for the experience rather than for speed.

::body
You want the Pixel feel without buying a Pixel, and you have an old Redmi Note 5 Pro sitting in a drawer. That is a reasonable combination. Pixel Experience X keeps the clean Pixel look and adds the extras people kept asking for, and on whyred the difference from MIUI is bigger than the difference between most ROMs.

Here is the install, in the order that works on this device, followed by an honest look at what a normal day on it feels like.

## What you need before you start

- An unlocked bootloader on whyred. This wipes the phone, so unlock before you set anything up.
- A custom recovery running properly. Test that it can read internal storage before you try to flash anything.
- The Pixel Experience X zip built for whyred.
- Firmware that matches what the build expects. If the release post names a base, use that one.
- A full backup of internal storage and a battery above 60%.

## Step 1 — unlock and get recovery working

Unlock the bootloader, accept the wipe, then flash a recovery for whyred. Do not rush this part. A recovery that boots but cannot see your storage is worse than no recovery, because you will only find out when you try to flash.

## Step 2 — back up system and data

Back up both, then copy the backup off the phone. Data so your files survive, system so you have something to roll back to if the ROM is not for you. A backup stored on the phone you are about to wipe is not a backup.

## Step 3 — wipe data, cache and Dalvik

Clean flash. If you are moving onto a new base, wipe system too. Coming from MIUI, a clean slate is the only way this settles down properly.

## Step 4 — flash the ROM zip

Pixel Experience X already includes the Google apps, so there is no GApps package to add. Flash the zip, watch the progress, and let the recovery go quiet at the end without tapping anything.

## Step 5 — wipe cache and Dalvik, then reboot

Wipe cache and Dalvik after the flash, then reboot. The first boot on this chipset is slow. Give it time and leave the phone on the charger while it works.

## Step 6 — finish setup and use it normally

Sign in, let your apps restore, and use the phone for a day before you decide anything. Battery numbers from the first few hours are meaningless while the system is still building caches.

## What it looks like once it boots

It looks like a Pixel. The launcher, the app drawer, the settings app, the quick settings tiles — all of it follows the Pixel design language rather than the MIUI one. There is no Xiaomi folder of preinstalled apps, no account prompts, and no skin sitting on top of Android.

The Pixel Experience X part adds a few extras on top of the standard clean Pixel experience, which is what separates it from the plain Pixel Experience builds.

## What was tested

- First boot, the setup wizard and the Pixel-style launcher.
- The notification shade and the quick settings layout.
- The camera app — opening it, framing, taking a shot.
- Installing apps from the Play Store and signing in.
- Battery across a normal day of use.
- How warm the phone gets during ordinary tasks.

## What is honest about it

- **The interface moves fine.** At this age, keeping the software light is the only way to keep it usable. A clean Pixel build does that better than MIUI did.
- **The camera is limited by the sensor, not the app.** The Pixel camera app is well built, but it cannot create detail the sensor never captured. Test it before you trust it.
- **Heavy games still push the phone.** No ROM turns this hardware into something else. Light games are fine, demanding ones are not.
- **Battery life is what it is.** A tired battery in an old phone stays tired. If yours has been in use for years, replacement is a better use of money than any ROM.

## Where people get stuck

- **Adding a GApps package.** This ROM already includes the Google apps. A second package on top causes crashes instead of adding features.
- **Skipping the system wipe coming from MIUI.** Data only is not enough when the base changes.
- **Flashing from a recovery that cannot read storage.** Sort the recovery first.
- **Judging the ROM in the first hour.** It is still settling. Give it a full day.

## Who should install this

Flash Pixel Experience X if you like the Pixel look and you accept that your Redmi Note 5 Pro will feel tidier rather than faster. Used as a light daily driver, it does the basics without drama. Calls, messages, browsing, music, the Play Store — all normal.

If you need performance, look elsewhere, because nothing on this hardware will give it to you. If the Xiaomi camera processing is what you like about MIUI, remember what you are giving up before you wipe.

One practical thing. Keep your installed app list small on a phone this old. That is not a ROM limitation, it is the hardware, and it is the single easiest way to keep the experience smooth. Whatever you do not use, uninstall.

And if the driver side of the unlock and flash is what usually slows you down, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks so Windows sees the phone first try. It is free, and the link is in the downloads section.

::faq
Q: Does Pixel Experience X need a separate GApps package?
A: No. The Google apps are already included in the ROM. Flashing a separate package on top of it causes crashes rather than adding anything useful.

Q: Is Pixel Experience X good as a daily driver on the Redmi Note 5 Pro?
A: For light use, yes. Calls, messages, browsing, music and the Play Store all work normally. Heavy games and memory-hungry apps will still push this old hardware, and no ROM changes that.

Q: Is a bootloader unlock necessary for this ROM?
A: Yes, the same as with every other custom ROM. Unlocking wipes the phone, so do it first and set the phone up again afterwards.

Q: Will it stay smooth over time?
A: Keep your installed app list small and it behaves much better. The hardware has limited memory, and every app running in the background takes some of it. Uninstalling what you do not use helps more than any setting.

Q: Can I return to stock MIUI if I do not like it?
A: Yes. Download the fastboot package for your exact model and flash it from your PC. That wipes the phone again, so move your files off before you start.
