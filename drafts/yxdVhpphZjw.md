::summary
Nothing OS 4.0 beta 1 has been ported to the POCO X7 Pro, running Android 16. Fast charging, the camera, Dolby Atmos, Play Store, 5G and face unlock all work. Vibration, fingerprint, double tap to unlock and Always On Display are still missing, so it is not ready to be your only phone yet.

::body
This is one of those videos where the honest list matters more than the good news, so let me put both on the page.

Nothing OS 4.0 beta 1 has been ported to the POCO X7 Pro, codename Rodin, by @th.achraf. It is Android 16, released 17/12/2025, and for a first port it is surprisingly usable. Ports usually collapse somewhere in the basics, and this one mostly does not.

## What works

- 90W fast charging, which is the one most ports get wrong
- Face unlock
- The camera, including blur effects
- Auto brightness that behaves
- 5G, Wi-Fi, Bluetooth, NFC
- MTP and OTG
- The setup wizard, Google login, Play Store and SMS
- Dolby Atmos
- Deep sleep, so it is not quietly eating the battery
- RAM Plus and game mode
- MEET_BASIC_INTEGRITY, plus game and Google Photos spoofing

That is a longer "working" list than most first ports manage. Fast charging and the camera in the same build is the part that surprised me.

## What is not there yet

- Vibration, listed as coming
- Fingerprint, listed as coming
- Double tap to unlock, listed as coming
- Status bar alignment, listed as coming
- Always On Display, missing
- Storage only reports 128GB, which is a known bug, so do not trust that screen

Read that second list again before you decide. Fingerprint and vibration are not small conveniences. Between them they change how the phone feels in your hand every single time you pick it up.

## The verdict, short version

As a beta it holds up, and the basics work. I would not move my SIM and my banking apps over yet though. Unlocking with a PIN every time gets old within a day, and no vibration means you will miss things you used to feel.

If you need a daily driver right now, keep your current setup and wait one or two builds. If you have a second phone and want to see Android 16 running on this hardware, this is a fun one to try.

## How to install it

The steps are short, so follow them in order.

1. Boot the phone to fastboot and flash vendor_boot. The video shows the exact command on screen.
2. Reboot straight to recovery. Do not stop in the system.
3. Format data, then sideload the ROM.
4. Skip root, finish setup, and restore your data after the phone is running.
5. Optional: flash the camera mod from the links if you want the extra camera work.

The order matters here. Flashing vendor_boot and then rebooting to recovery without passing through the system is what keeps the recovery side working, and skipping the format data step is how people end up back in a boot loop.

## Things to do before you start

- Move your photos and files off the phone. Format data wipes internal storage.
- Note your IMEI somewhere you can find it. You hope you never need it.
- Make sure the bootloader is unlocked before you begin. If it is not, unlocking wipes the phone anyway, so do that first and then take your backup.
- Keep the camera mod link handy if you plan to use it, so you are not hunting for it mid-setup.

## Who should install it

Install it if you have a spare phone, you like the Nothing interface, and you want to see how it behaves on this hardware before deciding anything permanent.

Skip it for now if fingerprint unlock, vibration or Always On Display are part of your normal day, or if your banking apps need to keep working without questions. The storage reading being wrong is also worth remembering, because it will worry you at exactly the wrong moment.

If the fastboot part is what usually stops you, the free Rom Flasher tool bundles the ADB and fastboot driver setup so the PC sees the phone first time. It is free, and the link is with the others below.

::faq
Q: Is Nothing OS 4.0 on the POCO X7 Pro ready for daily use?
A: Not quite. Fast charging, the camera, 5G, Play Store and Dolby Atmos all work, but fingerprint, vibration and Always On Display are still missing. Wait one or two builds if you need a single phone that does everything.

Q: Does the fingerprint sensor work on this port?
A: No, it is listed as coming, along with vibration and double tap to unlock. You unlock with a PIN in the meantime, which is the main reason people should not move their SIM over yet.

Q: Will my storage show the wrong size?
A: Yes, it reports only 128GB, and that is a known bug in this build. Your files are not being lost, the number on that screen is just wrong, so do not panic when you see it.

Q: Does the camera work, or should I flash the mod?
A: The camera works, including blur effects, and auto brightness behaves too. There is an optional camera mod in the links if you want more out of it, but it is not required to get a usable camera.

Q: How do I install Nothing OS 4.0 on the POCO X7 Pro?
A: Boot to fastboot and flash vendor_boot, reboot straight to recovery, format data, then sideload the ROM. Skip root, finish setup, and restore your data afterwards.
