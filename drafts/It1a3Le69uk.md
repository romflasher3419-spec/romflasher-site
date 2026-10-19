::summary
KaleidoscopeOS Edition on Android 13 for the Redmi K50i brings the November security patch, parallel space and a fix for the auto-brightness that never behaved. It wants a clean flash, not a dirty one — format data before you install. Dirty flashing over an older base is where the bugs come from.

::body
KaleidoscopeOS keeps its AOSP base close to stock and then adds the parts you actually notice: a second space for work apps, smoother display handling, and a brightness curve that is not fighting you. If auto-brightness has been annoying you on this phone, that last one is the reason to pay attention.

There is one rule with this build. It wants a clean flash. If you dirty flash it over an older base, you get the strange little bugs, and then you blame the ROM for something you did. Format data, install fresh, set the phone up again. It is a longer evening and a shorter week of troubleshooting.

## What is in this build

- November security patch merged.
- Parallel space added, for keeping work and personal apps apart.
- Smooth display added, which handles the refresh rate more sensibly.
- Auto-brightness fixed. After a clean flash, the screen stops jumping around.
- Other fixes and improvements rolled in alongside those.

## What it looks like once it boots

The base is close to stock Android, so the launcher, the settings app and the notification shade are AOSP. Not MIUI. If you are coming from stock firmware, that is the part to brace for, because the layout is different and the MIUI camera app is gone.

The additions are the interesting bit. Parallel space gives you a second, separate environment for apps, which is genuinely useful if you carry work apps and personal apps on the same phone. Smooth display changes how the screen handles its refresh rate, and once you have used it, going back feels coarse.

Auto-brightness is the one that quietly matters. On this phone the screen used to fight you — dimming when you needed it bright, jumping while you read. After a clean flash of this build, that behavior settles down.

## What is broken or rough

- **SELinux is permissive here.** That keeps the build flexible, but some banking and payment apps do not like it and may refuse to run or behave oddly. Test the apps you depend on before you commit.
- **A clean flash is not optional.** The build asks for it, and skipping it is the top source of weird bugs.
- **The MIUI camera is gone.** The replacement is a different animal, and if you shoot a lot you will notice.
- **Support moves build to build.** This is a community build on MediaTek hardware, so support varies. Keep a way back to stock.

## What you need

- Redmi K50i with an unlocked bootloader.
- A recovery for this device — TWRP or OrangeFox, running and readable.
- Platform tools on a PC, in case you need to push files after formatting.
- The KaleidoscopeOS Edition zip, plus vbmeta. AOSP builds usually need it.
- A full backup, because you are formatting data.
- 50% battery or better.

## Step 1 - back up everything first

Do this before anything else. A clean flash means format data, and format data means internal storage is emptied. Move your photos, downloads and documents off the phone entirely — not into another folder on the phone.

## Step 2 - boot into recovery and check it

Power off, boot your recovery, and confirm touch works and internal storage reads properly. If storage shows zero or touch is dead, the recovery does not match this device. Stop and fix it. A recovery that half works is how people end up with a phone that will not boot.

## Step 3 - format data, no shortcuts

This is the step the build asks for, and it is the one people skip.

- Wipe data, cache and dalvik.
- Then format data. That is the option that clears encryption, and it is different from a plain wipe.
- Accept that internal storage is now empty. Your ROM zip is gone from the phone.

## Step 4 - get the files back on the phone

After formatting data, you need the ROM zip and vbmeta back on the device. Either keep them on a USB drive you can read from recovery, or push them over from a PC with the platform tools you have set up.

This is the moment where the no-PC fantasy ends for most people. Have your files reachable before you format, not after.

## Step 5 - flash and reboot

Flash vbmeta the way your build instructions describe, then flash the ROM package and let it run to the end. Wipe cache and dalvik, then reboot to system.

The first boot is slow. Leave the phone alone, and let the setup wizard come up when it comes up. Do not interrupt it because the screen sat still for a minute.

## Who should install it

Install KaleidoscopeOS if you want a recent Android 13 base, you like the idea of a second space for apps, and the auto-brightness fix is worth a clean flash to you. You should be comfortable with recovery and with setting a phone up from scratch.

Skip it if you rely on banking apps that are strict about custom ROMs, or if a dirty flash is all the time you have. This build does not do shortcuts.

Keep your stock firmware and know the way back before you start. That is what makes a clean flash a choice instead of a gamble.

If the driver and platform tools side is where you normally stall, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Can I dirty flash KaleidoscopeOS over an older build?
A: No, and doing it is where the strange little bugs come from. This build asks for a clean flash. Format data before installing rather than after, and set the phone up again from scratch.

Q: What is the auto-brightness fix in this build?
A: Earlier builds had a brightness curve that behaved badly, dimming and jumping when it should not. The November patch build settles that down, but only if you clean flash. Dirty flashing can leave the old behavior in place.

Q: Does KaleidoscopeOS on the K50i include Google apps?
A: Treat Google apps as a separate step unless your build states otherwise. Many AOSP-based builds ship without them, so have a matching Gapps package ready to flash in the same recovery session as the ROM.

Q: Why do my banking apps refuse to work on this ROM?
A: This build runs with SELinux permissive, and some banking and payment apps do not accept that. They may refuse to open or behave strangely. Test the apps you rely on before you make this your daily phone.

Q: Do I need a PC to flash this?
A: You need one if you format data, because the ROM zip and vbmeta are erased from internal storage and have to be pushed back. Keep them on a USB drive you can read in recovery, or have platform tools ready on a PC.
