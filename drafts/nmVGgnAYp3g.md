::summary
DerpFest Android 13 is an unofficial build for the Redmi K50i, Redmi Note 11T Pro and POCO X4 GT, and you install it with TWRP rather than a PC. The catch is that TWRP 3.7.0_13 cannot format data on Android 13 — so you wipe data instead, and only format it from the DerpFest recovery that ships with the build. Read the Bluetooth workaround and the known issues before you start.

::body
You want Android 13 on the K50i. Not MIUI with a couple of tweaks — a real AOSP-style build with the DerpFest extras on top. This one exists, it is unofficial, and the install is a recovery job, not a fastboot marathon. That is the good news.

The less good news is the one step almost everyone trips on. TWRP 3.7.0_13 will not format the data partition on an Android 13 base. Not "sometimes". It fails. So the order I use is different from what you have probably read elsewhere, and it is worth following it exactly rather than improvising at 1am.

This build came from yuuki, dated 22 January 2023, and sits on the MIUI V13.2.3.0.TLOCNXM firmware base. Keep that in mind — the base is what the ROM expects underneath.

## What you need before anything else

- An unlocked bootloader. If that is not done yet, do it first, because it wipes the phone on its own.
- The MIUI V13.2.3.0.TLOCNXM base firmware already on the phone. A build flashed over the wrong base is where the strange bugs come from.
- The DerpFest zip for xaga. GApps and vanilla are separate downloads — pick one now, not halfway through.
- TWRP 3.7.0_13, or the DerpFest recovery that ships with the build. You will want the DerpFest one a bit later.
- Platform tools on the PC, and the vbmeta file if you are coming from stock MIUI.
- A full backup on a PC or an SD card. On this ROM that is not a suggestion.

## Step 1 — flash TWRP and boot straight into it

Put TWRP on the phone while you are still on the V13.0.6 base, then boot into recovery. Do not let the phone boot to system in between. Formatting data is not possible from this TWRP on Android 13, so we are using it as the tool that gets the zip in, nothing more.

If the recovery will not stick and MIUI keeps replacing it, that is a firmware-base mismatch, and it is worth going back and checking which base you are actually on rather than flashing TWRP five more times.

## Step 2 — wipe data, do not format data

Here is the part people get wrong. In TWRP 3.7.0_13 you want **Wipe**, then data. Do not touch **Format Data**. It fails on this Android 13 base and leaves you staring at a red error line wondering if you just broke something. You did not. The TWRP is simply not able to do that job here.

A wipe is enough to get the ROM flashed cleanly. Keep the format for later.

## Step 3 — flash the ROM zip

Flash the DerpFest zip you downloaded. GApps build if you want Google apps straight away, vanilla if you would rather add your own package and keep the product partition roomy. Wait until it reports done. Do not reboot in the middle even if the progress bar stalls for a minute.

## Step 4 — reboot, and if it hangs, use the DerpFest recovery

Reboot to system. If it boots, great. If it sits on the boot animation and just keeps going, that is not a brick — it is the data format you were not able to do in TWRP catching up with you. Reboot back to the **DerpFest recovery** that came with the build, format data there properly, and reboot again. That is the whole fix.

The first boot after a format takes a few minutes. Sit on your hands.

## Step 5 — the Bluetooth workaround

If Bluetooth acts up after you get in, open Developer Options and switch on **Disable A2DP offload**. That is the workaround straight from the build notes, and it is the difference between a Bluetooth headset that crackles and one that does not. It is one toggle, and it is the first thing to try before you blame the ROM.

## Known issues worth reading first

- **SELinux is permissive.** That is how the build ships. Do not expect enforcing behaviour.
- **Brightness can drop to minimum after a reboot.** Your screen is not dying. Turn it back up and carry on.
- **FM radio is not included yet.**
- **MIUI Camera has been removed**, because it does not work on Android 13 right now. Plan for using another camera app.
- **The vanilla build reserves 300 MB on the product partition** so you can flash packages like NikGApps later if you change your mind.

## The honest bit

This is an unofficial build, so treat the version you flash as the version you have. There is no guarantee of a next one, and no update channel that you can lean on. That said, if you want Android 13 on the K50i and you are comfortable in recovery, the install is genuinely short once you know not to hit Format Data in the wrong recovery.

Two things I would do differently next time. First, keep the DerpFest recovery zip on the phone before you start, not on the PC — you will want it without hunting for a cable. Second, finish the setup wizard on an empty phone before you restore anything. If something is going to break, better it breaks before two hours of your photos are back on.

If the bootloader unlock or the driver side is the part that stalls you, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install so you are not fighting Device Manager. It is free, and the link sits in the downloads section below.

::faq
Q: Why does TWRP 3.7.0_13 fail to format data on this ROM?
A: TWRP 3.7.0_13 cannot format the data partition on an Android 13 base — it errors out. Use Wipe data in TWRP to get the ROM flashed, then switch to the DerpFest recovery that ships with the build when you actually need a format.

Q: The phone is stuck on the boot animation after flashing. Is it bricked?
A: No. Reboot to the DerpFest recovery, format data there, and reboot to system again. The stuck boot is the result of not being able to format data inside TWRP, and formatting from the DerpFest recovery clears it.

Q: Do I need vbmeta for DerpFest on the Redmi K50i?
A: Yes, if you are coming from stock MIUI. Flash the vbmeta file with verity and verification disabled before you flash the ROM, or the boot can fail on the first attempt.

Q: Bluetooth keeps cutting out after installing. What fixes it?
A: Go into Developer Options and enable Disable A2DP offload. That is the workaround noted for this build, and it fixes the Bluetooth behaviour without needing anything else.

Q: Is FM radio or MIUI Camera working on this build?
A: No. FM radio is not included yet, and MIUI Camera was removed because it does not run on Android 13 right now. Keep a separate camera app ready if the stock MIUI camera is the reason you wanted this phone.
