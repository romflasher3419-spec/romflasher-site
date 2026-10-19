::summary
Axion OS brings Android 16 to the POCO X7 Pro (rodin) as a signed, vanilla build — no Google apps included, so you supply your own GApps. Flashing is a fastboot and recovery job: flash the matching vendor_boot image to both slots, format data in recovery, then sideload the ROM zip. The one day-one bug is Aperture video, which fails or crashes at random.

::body
Axion OS on the POCO X7 Pro. You have a ROM zip, a vendor_boot image and a PC, and the steps below are the ones that actually get this build onto rodin.

One thing to set expectations before you start. This is an **initial Android 16 release** of Axion. It is signed and SELinux is enforcing, which is more than plenty of first builds manage. But it is early, and there is one bug you will meet on day one.

## The bug you will hit

**Aperture camera video.** Recording video on Aperture either fails outright or crashes at random. It is not something you did wrong, and it is not fixed by reflashing.

The fix is simple: use a third-party camera app for video. Photos and everything else carry on as normal. Once you know it, it stops being a mystery and becomes a small annoyance.

## What you need

- An **unlocked bootloader** on the POCO X7 Pro.
- The **Axion OS ROM zip** and the **matching vendor_boot image**.
- **ADB and Fastboot** on your PC, with the drivers installed.
- **GApps** — NikGapps or MindTheGapps. This is a vanilla build with no Google apps baked in.
- **A backup of your IMEI** before you touch anything.

That last item is not optional. Back up the IMEI first, while the phone still works properly. You will not need it today. You may need it in three months.

## Step 1 — download the ROM and vendor_boot

Get both files from the links on this page. The vendor_boot image has to match the ROM build. Mixing a vendor_boot from one release with a ROM zip from another is asking for trouble.

## Step 2 — fastboot, then flash vendor_boot to both slots

Boot the phone into **fastboot mode** and flash the vendor_boot image to both slots. Both slots matter — this is the step that catches people out, and it is the difference between booting and boot looping.

Use the Fastboot menu for this, and confirm the PC sees the device before you start.

## Step 3 — reboot and catch recovery by hand

Reboot the phone with the fastboot reboot command, then **hold volume up the moment it restarts** so you land in recovery.

Do not use the fastboot reboot-to-recovery command here. That is the one that can leave the phone in a bad state on this device. Hold the buttons yourself.

## Step 4 — format data in recovery

Once you are in recovery, **format data**. This is a vanilla AOSP-based build coming from a different system, so a clean start is what you want. Everything on internal storage goes.

## Step 5 — sideload the ROM

Sideload the ROM with `adb sideload`. If your terminal accepts a dragged file path, you can drag the zip into the window after typing the command — either route works.

Let it run to completion. Do not interrupt it.

## Step 6 — take the recovery reboot

When the ROM finishes, it offers to reboot back into recovery. Say yes. This is normal for this kind of flash and it is not a loop.

## Step 7 — GApps, then root if you want it

From that recovery session, flash **GApps** — NikGapps or MindTheGapps. If you want Magisk, this is the point to add it too. Then reboot to system.

## Step 8 — give the first boot time

Reboot to system and leave it alone. First boot on a fresh vanilla build is slow. Interrupting it is how you end up back at step two.

## Where people get stuck

- **Skipping the vendor_boot step.** Flash the ROM alone on the X7 Pro and you are asking for a boot loop. This is the big one.
- **Using fastboot reboot recovery** instead of holding volume up manually. Take the manual route on this device.
- **Forgetting the IMEI backup.** People only remember they needed it months later, when it is too late to take one.
- **Assuming Google apps are included.** They are not. This is vanilla, and GApps are your job.
- **Blaming the ROM for the Aperture video bug.** It is known. Use another camera app and move on.

## Who should install it

Install Axion OS if you want a clean, signed Android 16 base without a vendor skin, and you are comfortable with fastboot and recovery steps. Skip it if you need a stock camera experience out of the box or you are not comfortable formatting data on a working phone.

If the driver side of fastboot is what usually slows you down, the free Rom Flasher tool bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section with the ROM.

::faq
Q: Does the camera work on Axion OS for the POCO X7 Pro?
A: Photos are fine, but Aperture video either fails or crashes at random. Use a third-party camera app for video and it works normally. This is a known issue on this initial build.

Q: Do I need to flash vendor_boot separately?
A: Yes. Flash the matching vendor_boot image to both slots before the ROM. Skipping this step or flashing only one slot is the most common cause of a boot loop on the X7 Pro.

Q: Does Axion OS include Google apps?
A: No. It is a vanilla build with no Google apps baked in. You flash NikGapps or MindTheGapps yourself after the ROM, from recovery.

Q: Will flashing Axion OS wipe my phone?
A: Yes. You format data in recovery as part of the install, so internal storage is reset. Back up your photos and files first and remember to save a copy of your IMEI.

Q: Why does Axion OS keep rebooting into recovery?
A: That is the ROM asking to return to recovery after a successful sideload, which is expected. Accept it, then flash GApps and reboot to system normally.
