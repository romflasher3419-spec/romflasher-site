::summary
DerpFest OS has landed on the POCO X7 Pro (Rodin) as an Android 16 build, flashed
with vendor_boot, ADB sideload, and Magisk 29 installed in the same recovery
session. GApps are already included, SELinux stays enforcing, and the build is
signed. This is the initial release, so the bug list is still being written.

::body
DerpFest is one of the ROMs people ask about most, and this is its first landing
on the X7 Pro. It follows the now-standard route for this phone: flash vendor_boot
to both slots, reboot, catch recovery with the volume key, format data, sideload,
then root while recovery is still open. I sideloaded Magisk 29 in the same session
because doing it in one pass saves you a second trip into recovery.

What I like is how little drama there is. What I would flag is the honest part:
the maintainer wrote "Initial Build" and nothing else, so the bug list is still
being written by whoever flashes first. That was me. Now it is you.

## What changed

- Initial build for the POCO X7 Pro.
- Signed build with SELinux enforcing.
- GApps included, so there is no separate package to hunt down.
- Root via Magisk 29 during the same recovery session.

That first line is the one to think about. An initial build is not a bad build.
It simply means nobody has hit the strange corner cases yet, so keep a backup of
whatever you are running now.

## What you need

- The DerpFest ROM zip for the POCO X7 Pro (Rodin).
- The `vendor_boot` image for this build.
- A PC with ADB and fastboot, or the Termux route if you want to skip it.
- The ADB and fastboot driver installed.
- Your data moved off the phone, and your IMEI written down somewhere safe.
- Magisk 29, only if you want root.

That IMEI line is not filler. It is the single step people skip and later regret,
and it takes two minutes.

## Step 1 - back up, and write down your IMEI

Move your data off the phone first. Then find your IMEI, usually in Settings, and
write it down or photograph it. If something goes wrong later, having it saved
somewhere other than the phone is worth more than you think.

## Step 2 - fastboot, and check the connection

Boot to fastboot with Volume Down and Power, connect to the PC, and run:

`fastboot devices`

You want a serial number and the word `fastboot`. No serial number is a driver
problem, so fix that before going further.

## Step 3 - flash vendor_boot to both slots

`fastboot flash vendor_boot --slot=all vendor_boot.img`

Both slots. Half-flashing this image is how boot loops start.

## Step 4 - reboot and catch recovery with Volume Up

Run `fastboot reboot`, then hold Volume Up immediately.

Do not use the fastboot command that jumps straight to recovery. On this phone
that is a brick waiting to happen, and I am not exaggerating for effect. Hold the
key yourself.

## Step 5 - factory reset, then format data

Factory reset, then Format data. This build wants a clean start, so do not try to
dirty flash it over an older ROM.

## Step 6 - sideload the ROM

Apply update, then Apply from ADB. From the PC:

`adb sideload` and the DerpFest zip name.

Let it finish to 100 percent before you touch anything.

## Step 7 - say yes, then sideload Magisk 29

When it asks, choose yes. Then, while recovery is still open, sideload Magisk 29
if you want root. Doing it here means one pass instead of two, and it is the tidier
route than patching a boot image after the fact.

Root is optional here. The ROM boots perfectly well without it.

## Step 8 - reboot to system

First boot is slow. Give it minutes, not seconds, before you start worrying. A
clean data partition with a fresh Android 16 install takes its time, and that is
normal.

## Where people get stuck

- **Not writing down the IMEI.** Two minutes now, a lot of regret later.
- **Using the fastboot reboot recovery command.** Hold Volume Up instead.
- **Expecting a bug list.** This is the initial build, so there is not one yet.
- **First boot worry.** It is slow. Give it minutes.

## One known rough edge

The maintainer posted a fix for Aperture video, so if that app misbehaves for you,
check the ROM channel post for it rather than assuming the whole camera stack is
broken.

## Should you flash it

If you want a signed Android 16 build with GApps already inside and you are happy
being an early adopter, this is a clean one. It boots like a phone that shipped
this way, and the whole process is short. If you want a build with a settled bug
list and a few releases of history behind it, wait a while.

If the driver side is the part that slows you down, the free Rom Flasher tool on
GitHub installs the ADB and fastboot driver in a couple of clicks. It is free, and
the link is in the downloads section.

::faq
Q: Do I need Magisk with DerpFest on the POCO X7 Pro?
A: No. Magisk 29 is optional root, and the ROM boots fine without it. If you do
want root, sideload it in the same recovery session as the ROM.

Q: Can I dirty flash DerpFest over an older ROM?
A: No. This build wants a clean start. Factory reset and format data before you
sideload, or you risk the strange behaviour that dirty flashes bring.

Q: Does DerpFest include Google apps?
A: Yes. GApps are baked into the build, so there is no separate package to
sideload and the Play Store works after setup.

Q: Does DerpFest work on other POCO phones?
A: No. This build is for the POCO X7 Pro, codename rodin. A package built for a
different model can leave the phone unable to boot.

Q: Why is the first boot so slow?
A: It is a fresh install on a clean data partition, so it takes minutes rather
than seconds. Let it finish before you start worrying that something is wrong.
