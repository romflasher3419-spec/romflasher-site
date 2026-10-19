::summary
Stag OS Android 12.1 on the Redmi K50i is a generic system image, phh-treble based, ARM64 AB, with both GApps and vanilla flavours. A GSI is only half the story — the ROM side is Stag OS and the hardware side is your vendor and kernel, so camera, signal and sensors depend on what is already on your phone. You flash it over fastboot with vbmeta, and you need the right vbmeta with verity and verification disabled.

::body
You want something clean on the K50i. No MIUI, no Xiaomi services, just Android. Stag OS arrives here as a generic system image, Android 12.1, phh-treble based, and that last detail is the one that decides whether you enjoy this or spend the evening confused.

A GSI is a system image that is not built for your phone specifically. It is built to fit the standard Android system layout, and your phone supplies everything else. Two people can flash the same file and get two different experiences. That is normal, not a broken build.

Here is what you get, what you do not, and the order to do it in.

## What the build is

- **Android 12.1** base.
- **Generic system image**, phh-treble based.
- **Architectures:** ARM64 AB.
- **GApps flavour** available for a Google setup.
- **Vanilla flavour** available if you would rather add your own package and keep it Google-free.
- **Slim:** not available for this one.
- **SELinux:** both enforcing and permissive work.
- **Bugs inside the ROM:** none reported.
- **Device-side issues:** depend on your vendor and kernel.
- **Maintainer:** @TheAtt1la.

## GApps or vanilla — pick before you download

This is the first real decision, and it is worth making calmly rather than grabbing whichever link is at the top.

Take **GApps** if you want the Play Store and Google apps working straight after the first boot, without extra steps. Take **vanilla** if you would rather add your own package afterwards and control exactly what lands on the phone. Both are legitimate; they just change how much work the setup is.

## What you need

- An unlocked bootloader. This wipes the phone, so do it first and get it out of the way.
- Platform tools on the PC, with the fastboot driver installed so Windows sees the phone.
- The Stag OS GSI zip for ARM64 AB, in the flavour you chose.
- The vbmeta file. You need version with **verity and verification disabled** — this is not optional on this setup.
- A backup on the PC. A GSI flash replaces the system, so plan for a wipe.

## Step 1 — sort the vbmeta before anything else

Get your vbmeta file in place first. You need it flashed with verity and verification disabled, and skipping this is the most common reason a GSI refuses to boot on the K50i. Do the vbmeta step in the same session as the flash, not as an afterthought, so you are not rebooting into a device that will not come up.

## Step 2 — boot the phone to fastboot

Power the phone off, then hold the fastboot key combination for the K50i until the fastboot screen appears. Plug it into the PC and confirm the device is recognised before you issue a single command.

## Step 3 — flash the system image

Flash the Stag OS GSI onto the system partition with fastboot. This is the part that takes the longest — the image is large, and the transfer runs over USB, so do not expect it to finish in a few seconds. Leave the cable in and let it run.

If fastboot errors out partway, do not reboot. A half-written system partition will not boot. Re-run the flash instead.

## Step 4 — reboot and let it settle

Reboot to system. The first boot on a GSI takes a while, and sometimes a second reboot is needed before everything settles. If an app or a sensor misbehaves right after the first boot, restart the phone once before you start blaming the build.

## What a GSI does and does not cover

This is the part worth internalising. Stag OS supplies the ROM side — the system, the interface, the framework. Your phone supplies the hardware side — the vendor image, the kernel, the camera drivers, the modem behaviour.

So camera quality is not something the GSI sets. Signal strength is not something the GSI sets. Sensor behaviour comes from what is already on your phone. If those are poor, the fix is on the vendor and kernel side, not in Stag OS.

That also explains why two people flash the same file and get different results. You are not comparing your phone to their phone — you are comparing your vendor and kernel to theirs.

## Where people get stuck

- **Skipping the vbmeta step, or flashing one without verity and verification disabled.** The device will not boot, and it looks like the GSI is at fault when it is not.
- **Flash errors, then a reboot.** A partial system write is an unbootable phone. Re-run the flash rather than rebooting to find out.
- **Blaming the ROM for hardware behaviour.** Camera, signal and sensors come from your vendor and kernel. A GSI cannot fix what it does not control.

## About updates

Updates and changelogs come from the official groups rather than from the phone, and the maintainer group is noted as unknown here. So keep an eye on the official channels if you want to know when something moves. Treat the build you flash as the build you have.

If the driver and platform tools side is where you get held up, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Do I need vbmeta to flash Stag OS on the Redmi K50i?
A: Yes. Flash a vbmeta file with verity and verification disabled before the GSI, otherwise the device will fail to boot and it will look like the ROM is broken.

Q: What is the difference between the GApps and vanilla Stag OS builds?
A: The GApps flavour comes with Google apps ready to use after the first boot. The vanilla flavour ships without them, so you add your own package afterwards. Both are supported, and the choice is about how much setup you want.

Q: Will the camera and signal be as good as on MIUI?
A: That depends on your vendor and kernel, not on Stag OS. A GSI supplies the system, while camera, modem and sensor behaviour come from the hardware side of your phone. Two people can get different results from the same image.

Q: Is Stag OS Android 12.1 a proper ROM for the K50i?
A: It is a generic system image, phh-treble based, built for ARM64 AB. That means it runs on the K50i, but it is not a device-specific build, so parts of the experience depend on what is already on your phone.

Q: How do I get updates for this Stag OS GSI?
A: Updates and changelogs come from the official groups rather than over the air. Watch the official channels, and treat the version you flashed as the version you are running until something newer appears.
