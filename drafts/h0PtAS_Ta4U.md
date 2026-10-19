::summary
Arrow OS on the Redmi K50i is an unofficial Android 12L AOSP build on an OSS vendor, and this release fixed haptics and the VoLTE drop after reboot and added the MIUI Camera. Auto brightness is still not working. You flash the ROM, then Gapps right after it, before the first boot.

::body
This is the unofficial Arrow OS build for the K50i, running Android 12L on an OSS vendor. It is a clean AOSP ROM — no MIUI skin, no extra junk — and the build I am flashing here brought a few real fixes with it. That is why it is worth a fresh install instead of a dirty one.

Before you touch anything, two jobs have to be done. Your bootloader has to be unlocked and a custom recovery has to be on the phone. Both are separate from this and both come first.

## What you need

- A Redmi K50i with an unlocked bootloader.
- A custom recovery already flashed.
- The Arrow OS build for the K50i, from the link in the downloads section.
- A Gapps package. The ones recommended for this build are Flame Gapps and Nik Gapps.
- A charged phone and a good cable for the first boot.

Get the Gapps package before you start. Doing the flash and then hunting for Gapps from the setup screen is a self-inflicted problem.

## Step 1 - reboot into recovery

Power off, then hold Volume Up and Power until recovery appears. Check it can read internal storage. If recovery asks for a password or shows empty folders, your data partition is encrypted and you need to format it before going further.

## Step 2 - wipe and format

Wipe data and format before flashing, especially if you are coming from another ROM. A dirty flash from a different base is where bootloops start, and Arrow OS on an OSS vendor is a different base from MIUI.

If you are on the same Arrow OS line and just moving to this build, a dirty flash may be fine. If you are unsure, format. It costs you data either way.

## Step 3 - flash Arrow OS

Install the Arrow OS zip and let it run to the end. Do not tap the screen while it writes.

## Step 4 - flash Gapps right after, before first boot

This is the part people get wrong. Flash your Gapps package immediately after the ROM, in the same recovery session, before you boot the system for the first time. Boot the ROM first and you will be setting it up again to add Google apps properly.

## Step 5 - reboot and let it sit

The first start takes a while, so let it sit. Setup wizard, then set the phone up and test calls, data, Wi-Fi and the camera before you rely on it.

## What changed in this build

- **Gapps are flashable now.** Flame Gapps and Nik Gapps both work, which means you can add Google apps properly instead of fighting the system.
- **Haptics fixed.** Vibration works again, so the keyboard and gestures feel right.
- **VoLTE issue after reboot fixed.** This was the annoyance of losing VoLTE every time you restarted. If it still drops, turn off video calling as a fallback.
- **MIUI Camera added.** You get the camera app you already know instead of a plainer AOSP one.
- **OSS vendor, SELinux permissive.** That is what this build runs on.
- **Miscellaneous improvements.** Smaller fixes through the build.

## What is broken

- **Auto brightness is not working yet.** Expect to drag the brightness slider yourself. It is a small thing that you notice twenty times a day.
- **Safety Net needs a module.** It will not pass out of the box, so banking and payment apps may refuse to run until you sort that.
- **4K video needs a player that can handle it.** Just Player does the job if the stock player chokes.

## Who should install it

- **Install it if** you want clean AOSP with the MIUI Camera and you can live with a manual brightness slider for now.
- **Skip it if** auto brightness is something you rely on, or if you need banking apps to work without extra steps on day one.

## Where people get stuck

- **Flashing Gapps after the first boot.** Do it in the same recovery session as the ROM, before the phone ever boots.
- **VoLTE dropping after a reboot.** The fix is in this build, but if it still misbehaves, disable video calling as the workaround.
- **Expecting Safety Net to pass.** It needs a module. Plan for that if you use payment apps.

If the driver side of your PC setup keeps failing, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. The link is in the downloads section.

::faq
Q: Is auto brightness fixed in Arrow OS on the Redmi K50i?
A: No, not in this build. Auto brightness does not work yet, so you adjust the slider yourself. It is on the list of things still to be fixed rather than a setting you are missing.

Q: Do I need to flash Gapps with Arrow OS on the K50i?
A: Yes, if you want Google apps. Flash the Gapps package right after the ROM in the same recovery session, before the first boot. Flame Gapps and Nik Gapps both work with this build.

Q: Why does VoLTE stop working after a reboot?
A: That was a known issue and this build carries a fix for it. If it still drops on your phone, turn off video calling, which is the workaround that keeps VoLTE alive for most people.

Q: Which Gapps package works with Arrow OS Android 12L on the K50i?
A: Flame Gapps and Nik Gapps are the ones recommended for this build. Either works, and the important part is flashing it straight after the ROM rather than after the first boot.

Q: Does Arrow OS on the Redmi K50i pass Safety Net?
A: Not out of the box. Safety Net needs a module, so expect banking and payment apps to complain until you sort that out. Plan for it before you move your daily apps across.
