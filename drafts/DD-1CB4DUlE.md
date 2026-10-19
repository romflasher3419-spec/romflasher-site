::summary
SuperiorOS is now running on the Poco X7 Pro on an Android 16 base, and this is the whole clean flash: fastboot, vendor image, the ROM's own recovery, a wipe, and a sideload. It is a clean-flash-only build, so you will lose your data. The two spots that catch people are flashing vendor_boot to only one slot and sideloading before the factory reset.

::body
You want SuperiorOS on the Poco X7 Pro and you want the whole path in one place, not five forum posts stitched together. Here it is. There is nothing complicated about the process — get into fastboot, push the vendor image, boot the recovery that ships with the ROM, wipe, then sideload the ROM zip. If you have flashed any other Poco X7 Pro build, this rhythm will feel familiar and you will move fast.

The one thing to accept up front: clean flash is the only supported path. No dirty flashing, no keeping your data. That is not a scare tactic, it is just how this build is meant to be installed.

## What you need

- The SuperiorOS ROM and its vendor image, both linked below.
- The ADB fastboot tool and the matching driver on your PC.
- A phone that is already unlocked, and a USB cable that holds a connection.
- A backup, IMEI included, because the clean flash wipes everything.

I will say the IMEI part again because it matters. Back it up. I do not make backups and I still tell you to. If something goes sideways and your IMEI is gone, no tutorial will bring it back for you.

## Step 1 — fastboot, and confirm the PC sees the phone

Power the phone off and hold Volume Down and Power until the fastboot screen appears. Plug it in and run:

`fastboot devices`

You need the long serial number and the word `fastboot`. No serial means the driver is missing. Fix that before you go any further, because every step after this depends on it.

## Step 2 — flash the vendor image to both slots

Flash the vendor_boot image that comes with the ROM:

`fastboot flash vendor_boot --slot=all`

The `--slot=all` part is not optional. This phone uses two slots, and if you flash only one, the phone can fall back to the slot you skipped. Recovery then refuses to boot, and you will spend an hour thinking the ROM is broken when it is just the other slot sitting empty.

If your model's instructions say boot instead of vendor_boot, follow the ROM's own guide. The idea is the same: the recovery image goes to both slots.

## Step 3 — reboot into the Superior recovery

Now reboot into the recovery that comes with the ROM. You can do it from fastboot:

`fastboot reboot recovery`

Give it a moment. If it boots to recovery, you are exactly where you should be. If it drops you into the system instead, go back and check Step 2 — that is the one-slot problem showing itself.

## Step 4 — factory reset first

This is the step people reverse, and it is the one that causes bootloops. Do a factory reset inside recovery and wipe the data. Do it now, before the sideload.

Sideloading the ROM onto old data is how you get a bootloop that looks like the ROM's fault. It is not. It is order of operations.

## Step 5 — sideload the ROM zip

In recovery, choose **Apply update**, then **Apply from ADB**. On your PC, run:

`adb sideload <the ROM zip>`

The progress bar will look stuck near the end. That is normal — sideload finishes quietly. Let it run all the way through and do not touch the cable.

## Step 6 — reboot and set it up

When the sideload is done, reboot to the system. First boot takes a while, so give it time. Finish the setup wizard before you restore anything, so any problem shows up on a clean phone.

## Where people get stuck

- **Flashing only one slot.** Recovery refuses to boot because the other slot is empty. Use `--slot=all`.
- **Sideloading before the factory reset.** This usually ends in a bootloop. Wipe first, sideload second.
- **USB debugging off.** The device never shows up in the tool, so nothing you type will land anywhere.

## Notes on this build

This is a Gapps build, signed, with SELinux enforcing. That means Google apps are in from the start and the security model is intact, which is a good sign on a custom ROM. The changelog is basically the initial build plus a gaming-focused tweak pass.

On known issues: the maintainer's list is mostly "you tell me, bring logs with your report." There is an Aperture fix shown in the video. And FP jiiov is likely still not working, so test your fingerprint yourself before you rely on it.

If the driver and fastboot side is the annoying part, the free Rom Flasher tool on GitHub bundles the driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Do I have to wipe to install SuperiorOS on the Poco X7 Pro?
A: Yes. Clean flash is mandatory for this build, and it is the only supported path. Back up everything first, IMEI included, and expect a fresh setup wizard on first boot.

Q: Which slot do I flash vendor_boot to?
A: Both. Use `--slot=all` when you flash the vendor image. Flashing only one slot is the most common reason recovery refuses to boot on this phone.

Q: Is root required for this ROM?
A: No. The ROM boots without root, so you can leave it stock and add root later if you want it. Nothing in the install depends on being rooted.

Q: Does this build include Google apps?
A: Yes, it is a Gapps build, signed, with SELinux enforcing. Google apps are in from the start, so you do not need a separate Gapps zip.

Q: Can I dirty flash SuperiorOS over another ROM?
A: You can try, but do not expect anyone to call it a good idea. A clean flash is the supported path here, and dirty flashing over another ROM is how you end up in a bootloop with no clear cause.
