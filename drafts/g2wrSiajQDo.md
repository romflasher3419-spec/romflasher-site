::summary
Cherish OS on Android 13 runs on the Xiaomi 11T Pro as a GSI, so it installs as one system image over your existing vendor. Only ARM64 AB is published, and there is no vanilla build, so take GApps or slim. The reason to pick it is portability: your vendor stays untouched, so switching ROMs later is a five-minute job instead of an evening.

::body
Cherish OS is a customisation-heavy ROM, and this release is a GSI. So all of that customisation lands on top of your existing vendor instead of replacing it.

That is the whole deal with generic system images. The ROM is one file. The hardware support comes from your phone's own vendor and kernel. And you cannot blame the ROM when the camera mode you like is not in the list.

Device here is the Xiaomi 11T Pro.

## What it does

- Installs Android 13 as a single system image on a Treble-ready device. Only ARM64 AB is published here.
- GApps and slim builds are available. Vanilla is not, so budget for Google apps being present.
- SELinux runs in either mode. Enforcing and permissive are both fine.
- Keeps the Cherish customisation set on the built-in parts, which is what this ROM is known for.
- Nothing is listed as broken inside the ROM itself.

## The best part: it is portable

This is the honest reason to pick a GSI over a device-specific ROM.

Flash it. If you do not like it, flash the next GSI over it. Your vendor stays untouched the whole time, so swapping ROMs is a five-minute job rather than a full evening with a fastboot package.

On the 11T Pro the image booted without complaints. Setup ran, the phone settled, and there was nothing to fight with. If you like trying ROMs, that portability is worth more than any single feature.

## What it does not do

This section is the important one, because GSIs get oversold.

- **It does not fix hardware.** Anything vendor side — camera quality, dual SIM quirks, sensors — follows your vendor and kernel, not the ROM.
- **It does not give you a vanilla build.** If you want a Google-free system, this release will not do it. Take GApps or slim and plan accordingly.
- **It does not ship for every architecture.** Check that ARM64 AB matches your device before you download.

That first point is the one people get wrong. If the camera on your phone takes soft photos after the flash, that is your vendor blob, not Cherish OS. A newer vendor and kernel is the fix. No GSI changes that.

## Who should install it

- Someone who wants heavy customisation on top of clean AOSP.
- Anyone who likes swapping ROMs and wants the quick, non-destructive route.
- People who are comfortable with GApps being present and do not need a Google-free system.
- Anyone on a recent vendor and kernel, which is where a GSI works best.

If you need the camera to be as good as MIUI, or you depend on vendor-specific features, a device-specific ROM will serve you better.

## How to flash it

1. `fastboot reboot fastboot` — move into fastbootd, because the system partition can only be written there.
2. `fastboot --disable-verity --disable-verification flash vbmeta` — both flags, or the GSI will not boot.
3. `fastboot erase system`
4. `fastboot flash system` — give it a couple of minutes and do not unplug.
5. `fastboot reboot recovery`
6. Wipe data in Mi Recovery, then reboot.

## What you need first

- An **unlocked bootloader**. Required, and it wipes the phone the first time.
- The **Cherish OS Android 13 GSI**, ARM64 AB.
- The **vbmeta** file, since you flash it with both flags.
- **Platform tools** on the PC.
- A **custom recovery** for the final data wipe.
- A **full backup**, because the data wipe is not optional.

## Where people get stuck

- **Skipping the vbmeta flags.** Without both `--disable-verity` and `--disable-verification`, the image is rejected at boot.
- **Skipping the data wipe.** New system plus old userdata equals a bootloop, every time.
- **Flashing system in plain bootloader.** It has to be fastbootd.
- **Blaming the ROM for vendor behaviour.** Camera, calls and sensors are your vendor's side of the fence.

If the driver side of this is the annoying part, the free Rom Flasher tool on GitHub handles the ADB and fastboot driver install in a couple of clicks. It is free, and the link is in the downloads section.

One last thing. Wipe data, then finish setup on the empty phone before you restore anything. That way nothing hides behind two hours of restored files.

::faq
Q: Is Cherish OS a GSI or a device-specific ROM?
A: It is a GSI for this release, so it installs as a single system image over your existing vendor and kernel. That means your vendor stays untouched and the ROM itself is portable.

Q: Does Cherish OS come in a vanilla build?
A: No. GApps and slim are what is available, so expect Google apps to be present. If you want a fully Google-free system, you need a different release.

Q: Which Cherish OS image is right for the Xiaomi 11T Pro?
A: The ARM64 AB image. That is the architecture published for this release, so check it matches your device before you download.

Q: Will the camera be as good as MIUI on a Cherish OS GSI?
A: No, and no GSI can promise that. Camera quality on a generic system image follows your vendor blob, so an older vendor means softer photos. A recent vendor and kernel reduces the gap.

Q: What happens if I do not wipe data after flashing this GSI?
A: You will most likely bootloop. Old userdata is encrypted with keys from the previous system, so a new system partition on old userdata does not start. Wipe data in recovery before the first boot.
