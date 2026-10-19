::summary
You can root the POCO X7 Pro with Termux and KernelSU without a PC anywhere in
the chain. You patch your own init_boot file inside the KernelSU app, move it to a
second Android device, and flash it from Termux over USB. The init_boot has to
match your exact firmware build, or you are heading into a boot loop.

::body
Rooting without a PC sounds like a party trick. It is not. It is the same flash
you would do from a laptop, just moved onto hardware you already carry. Two
Android devices, one cable, one file transfer, and no driver hunting on Windows.

I picked KernelSU over Magisk for a boring reason. It keeps root in the kernel,
stays quieter about it, and apps that sniff around for the usual root leftovers
tend to miss it. Magisk still works fine if that is your habit, and nothing below
changes much if you prefer it.

The part that actually matters is the init_boot file, and it has to match your
firmware build exactly. Mismatch it and you are heading straight into a boot loop.

## What you need

- The KernelSU app. Use the patched build linked below, because plain store
  versions will not patch cleanly.
- `init_boot.img` from your own firmware. In this video the build is
  `20.202.0.VOJINX`, and yours has to match your phone.
- Termux set up with the recovery tool on a second Android device, with USB
  debugging switched on.
- Quick Share, Telegram or WhatsApp to move files between the two phones.
- Your data backed up, because you are rooting, not lucky.

## How the flow works, in plain words

This is the part that feels strange the first time. You are not flashing from the
laptop. You are pulling the boot image off your own firmware, sending it to the
phone, letting the KernelSU app patch it, sending the patched copy back to the
device that runs Termux, and flashing it from there with the phone plugged in over
USB. Two Android devices, one cable.

Once you have done it once, it is a ten minute job.

## Step 1 - install KernelSU and open it once

Install the patched KernelSU build and open it one time so it sets itself up.
Do not skip that first launch.

## Step 2 - get your own init_boot.img

Take `init_boot.img` out of your own fastboot ROM or recovery package. Not someone
else's upload, not a file from a guide about a different build. Yours.

Check the firmware version while you are in there. If it does not match what is on
the phone, stop and download the right package, because flashing a mismatched
boot image is the classic boot loop.

## Step 2b - a quick sanity note before you commit

If you are unsure which firmware you are on, check it in Settings and compare it
against the package name before you extract anything. Two minutes here saves an
evening later.

## Step 3 - patch init_boot in KernelSU

Send `init_boot.img` to the phone, open KernelSU, choose Install, pick the file,
and hit Start. It writes a patched copy. Leave it in the Download folder so you
know exactly where it is.

## Step 4 - send the patched file to the Termux device

Move the patched image back to the second Android device with Quick Share,
Telegram or whatever you already use. Drop it in the Download folder there too,
because the Termux command you paste expects to find it there.

## Step 5 - run the flash tool from Termux

Open Termux, paste the `cd` command from the video, then run the flash tool. It
walks the flashing for you, which is the whole reason this works without a laptop.

## Step 6 - connect the phone and confirm it is seen

Connect the phone over USB with USB debugging on. The tool should list the device
before it flashes anything. If it reports nothing, that is almost always a
charge-only cable or debugging left off, not a broken tool.

## Step 7 - flash, reboot, confirm root

Flash the patched `init_boot`, reboot, and open KernelSU. It should show root as
live. If it does not, the patched file and the firmware build do not match, so go
back to Step 2 with the correct `init_boot.img`.

## Where people get stuck

- **Flashing an init_boot from a different firmware build.** The version has to
  match yours, no exceptions. This is the single most common failure here.
- **USB debugging switched off**, so the tool reports no device and people blame
  the cable.
- **A charge-only cable.** Same dead end, just with extra frustration and a
  longer troubleshooting session.
- **Using the plain store KernelSU build**, which will not patch cleanly.

## KernelSU or Magisk

Both give you root. KernelSU keeps it in the kernel, which is why I picked it
here: apps that sniff around for the usual root leftovers tend to miss it, and it
stays quieter. Magisk still works fine and has the bigger ecosystem of modules. If
you already know Magisk, there is no reason to change. If you are starting fresh
on this phone, KernelSU is the tidier choice.

One honest note: rooting breaks Play Integrity on most setups, and banking apps
often care. That is not a bug in this method, it is what root does. If your bank
app is non-negotiable, think about that before you flash.

If the driver or tooling side is what puts you off, the free Rom Flasher tool on
GitHub handles the ADB and fastboot driver install in a couple of clicks. It is
free, and the link is in the downloads section.

::faq
Q: Can you really root Android without a PC?
A: Yes. Termux on a second Android device does the flashing, and the phone you are
rooting just needs USB debugging on and a working cable.

Q: Do I need an unlocked bootloader to root with KernelSU?
A: Yes. Rooting needs an unlocked bootloader, and unlocking wipes your data, so
back everything up before you begin.

Q: Which init_boot file should I patch?
A: The one from your own firmware, with a matching build number. In this video it
is 20.202.0.VOJINX, but yours must match whatever build your phone is running.

Q: KernelSU or Magisk for the POCO X7 Pro?
A: Both work. KernelSU keeps root in the kernel and tends to stay quieter around
apps that look for root, while Magisk has the larger module ecosystem.

Q: Does rooting break banking apps?
A: Often, yes. Root usually fails Play Integrity, and many banking apps check for
that. Plan for it before you root rather than after.
