::summary
Rooting MIUI 14 on a Xiaomi phone is a short job: let the Magisk app patch your boot image, flash that patched image in fastboot, boot up, then turn on the DenyList and add your banking apps to it. The root itself takes minutes — almost all the time goes into downloading the right boot image for your exact build.

::body
Root on MIUI 14 is not the hard part. The hard part is the one file you need first, and the one setting you will forget afterwards.

Here is the whole job in one line: Magisk patches your boot image, fastboot writes it back, you boot the phone, install the Magisk app, and then tell Magisk which apps are not allowed to see root. Skip that last part and your bank app will close the moment it opens.

## What you need before you start

- An unlocked bootloader. Root comes after that, never before it.
- The Magisk APK, from the link below.
- Your phone's **boot image**, pulled from the exact MIUI build you are running right now.
- Platform tools and a USB cable that does not drop.
- Ten minutes where you can leave the phone plugged in.

That third bullet is where this goes wrong. "Matching your build" means the same MIUI version, the same region and the same model. A boot image from a different build is the number one cause of a phone that loops on the logo forever.

## Step 1 — get your own boot image

The boot image has to come from your phone's current software, not from a friend's phone and not from a package you found in a random folder. If you already have the fastboot package for your exact build, the boot image is inside it among the other images. If you do not, the safest path is to match the MIUI version shown in Settings, About phone, down to the build number.

Copy that file to the phone. Do not rename it into something you will not recognise later.

## Step 2 — let Magisk patch it

Install the Magisk APK you downloaded. Open it. On the main screen you will see the Magisk version and next to it an Install button.

Tap **Install**, then choose **Select and Patch a File**. Pick the boot image you copied over. Magisk works for a few seconds and writes a new file next to the original, with a name that ends in something like `magisk_patched` plus a random string.

That patched file is what you flash. Not the original. Copy the patched one back to your PC, into the same folder as your platform tools, so the commands are short and you do not mistype a path.

## Step 3 — flash it in fastboot

Power the phone off completely. Hold **Volume Down + Power** until the fastboot screen appears. Plug it in and check that the PC sees it.

Then flash the patched image to the boot partition. The command is the fastboot flash command with `boot` as the partition and your patched file as the target — the exact name depends on what Magisk produced, so copy it from the folder rather than typing it by hand.

A successful flash prints a short confirmation and finishes in about a second. If it hangs, it is almost always the USB connection or a missing driver, not Magisk.

## Step 4 — boot and finish the Magisk setup

Reboot the phone normally. First boot takes longer than usual while the patched image settles, so give it a minute before you panic.

Open the Magisk app again. It should now show root as active. If it still asks you to install, the wrong image went onto the phone — go back and check that you flashed the patched file and not the original.

## Step 5 — the DenyList, which is the real point

On MIUI 14 this is the step that matters more than the root itself.

Open Magisk, go into **Settings**, and turn on **Zygisk** if it is offered, then enable **Enforce DenyList**. Open the DenyList itself and tick every app that has a reason to care whether your phone is rooted: your bank, your payment apps, the wallet, anything government or ID related, and any game with anti-cheat.

Then go check the Play Store. Under Settings, About, Play Store certification should say the device is certified. If it is not, that is the same root-detection problem wearing a different hat, and the DenyList is still where you fix it.

## Where people get stuck

- **Wrong boot image.** If the phone loops on the logo, this is the cause almost every time. Flash the original boot image to get back, then start again with the correct one.
- **Skipping the DenyList.** Root works, everything is fine, and then the banking app closes on launch. That is not a broken root — that is an app that saw root.
- **Forgetting about updates.** Every MIUI OTA replaces the boot image, which means root is gone after the update. You patch and flash again on the new build.

That last one is not a bug, it is just how it works. After any system update, expect to spend the same ten minutes again.

## One honest note

If you have never touched a terminal, the fastboot part is the fiddly bit. The driver has to be installed properly or the command just says it is waiting for a device, and nothing tells you why. Once the connection is right, the flash itself is one command and one second.

The free Rom Flasher tool on GitHub takes care of the ADB and fastboot driver side so you are not stuck in Device Manager guessing. It is free, and the link is in the downloads section.

Do the whole thing on a phone that has finished its setup wizard and is sitting idle. Rooting mid-setup, or with a restore running in the background, just adds variables you do not need.

::faq
Q: Does rooting MIUI 14 wipe my data?
A: The root itself does not. But you need an unlocked bootloader first, and unlocking the bootloader wipes the phone. So if your bootloader is still locked, back everything up before you begin.

Q: Why does my banking app still detect root after I rooted?
A: You skipped the DenyList, or you did not add that specific app to it. Open Magisk, go to Settings, enforce the DenyList, and tick the app. Then clear that app's data once so it starts fresh.

Q: Will I lose root after a MIUI update?
A: Yes. An OTA replaces the boot image, so the patched one is gone. Patch the new build's boot image and flash it again, and your data stays exactly where it is.

Q: Can I root without flashing anything in fastboot?
A: Not on MIUI 14 with Magisk. Magisk needs the patched boot image written to the boot partition, and fastboot is the only reliable way to do that on these phones. Recovery methods exist but they are less predictable.

Q: What happens if I flash the wrong boot image?
A: The phone typically loops on the logo and never reaches the system. Flash your build's original boot image to recover, then start again with the image that matches your exact MIUI version and region.
