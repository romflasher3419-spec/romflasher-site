::summary
You do not flash TWRP on the Xiaomi 11T Pro and hope — you boot the recovery with one fastboot command, then use TWRP's own option to install itself permanently. That way the write happens from inside a working recovery, which is a lot less nerve-racking than a blind flash.

::body
Here is the trick most people miss. The usual advice is to flash the recovery image straight to the phone and hope it comes up. On the 11T Pro there is a better way. You boot the recovery first with fastboot, let it come up on screen, and then use TWRP's own option to install itself onto the phone for good.

The difference matters. When you flash blind, you find out whether the image works only after the reboot, and by then the stock recovery may already be back. When you boot first, you are looking at TWRP on the screen before anything is written. Then you do the permanent install from inside a recovery that is already running.

The whole job is: phone in fastboot, cable in, one command, then a couple of taps. No long wait.

## What you need

- **Xiaomi 11T Pro with an unlocked bootloader.** TWRP cannot go on a locked one. Full stop.
- **A PC** with the recovery image and platform-tools ready
- **A working data cable.** Not a charge-only one. Those are the reason a command appears to do nothing.
- **The image file for the 11T Pro** — link below. Take the one built for this phone, not a generic image.

## Step 1 — reboot to fastboot

Power the phone off, then hold **Volume Down + Power** until you see the fastboot screen. Plug it into the PC.

Run:

`fastboot devices`

You want a serial number back with the word `fastboot`. If the command just sits there waiting for a device, that is the cable or the driver, not TWRP. Fix it now.

## Step 2 — boot the recovery with one command

This is the one command the whole guide is named after:

`fastboot boot file.img`

Replace `file.img` with the actual image filename you downloaded. `fastboot boot` sends the recovery to the phone and runs it without writing it to storage. That is the key distinction — it is a temporary boot, not a flash. Wait until the recovery screen appears.

## Step 3 — wait for recovery to load

Give it a moment. TWRP will come up, and this is your sign that the image works on this phone. If it drops back to fastboot or to a black screen, the image is wrong for the 11T Pro. Stop and get the right one.

## Step 4 — go to Advanced

In TWRP, open the **Advanced** menu. The option you want is in there.

## Step 5 — select Flash current TWRP

Choose **Flash current TWRP**. This is the step that writes the recovery to the phone permanently, and it does the write from inside a running TWRP rather than from a blind fastboot flash. It takes a moment.

After this one step, the recovery is on the phone for good. A normal reboot lands you back in TWRP.

## Where people get stuck

- **Rebooting before Step 5.** This is the big one. `fastboot boot` only runs the recovery for now. If you restart the phone before you tap Flash current TWRP, it is gone and you start over from Step 1.
- **A charge-only cable or a missing driver.** The command sits there waiting for a device and looks frozen. It is not frozen.
- **A locked bootloader.** Nothing here works until it is unlocked.
- **OTA updates.** Taking a system update later can put the stock recovery back. Keep the image file handy so you can repeat this, which takes about two minutes.

## One small reassurance

If you get to TWRP on the screen, you have already done the hard part. The permanent install is a menu tap, and at that point you are watching it happen rather than trusting it. That is the whole reason this method is worth using over a straight flash.

The driver side is the fiddly part. If Device Manager is showing an unknown device, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Does fastboot boot install TWRP permanently on the Xiaomi 11T Pro?
A: No. `fastboot boot` only runs the recovery for that session. To make it stick you open Advanced in TWRP and choose Flash current TWRP. After that, a reboot lands you in TWRP.

Q: What happens if I reboot before flashing current TWRP?
A: The temporary recovery is gone and the phone boots normally. You have not broken anything — just start again from fastboot and re-run the boot command.

Q: The fastboot command just hangs. What is wrong?
A: It is almost always the cable or the driver. A charge-only cable cannot carry data, and a missing driver means the PC never sees the phone. Swap the cable and check Device Manager.

Q: Does this work with a locked bootloader?
A: No. The 11T Pro's bootloader has to be unlocked first. TWRP cannot boot or install on a locked one.

Q: Why did TWRP disappear after a system update?
A: An OTA can restore the stock recovery over TWRP. Keep the image file so you can repeat the one-command boot and the permanent install, which takes a couple of minutes.

Q: Is this safer than flashing the recovery image directly?
A: It is less nerve-racking in one specific way. You see TWRP running before anything is written, and the permanent install happens from inside a working recovery rather than from a blind flash.
