::summary
You can install an AOSP ROM on a Xiaomi or POCO phone without a PC and without Termux, using two Android phones and the free Rom Flasher tool. The helper phone flashes the vendor_boot or boot image, the target phone boots recovery, you format data, and then you sideload the ROM zip. It works on any build that ships a recovery image, like Pixel Infinity, crDroid, LineageOS or Evolution X.

::body
You do not have a laptop handy, or you do not want to wrestle with drivers on Windows tonight. Fair enough. If the ROM you want ships a recovery-based build, you can do the whole install from a second Android phone. Two phones, one cable, one tool, and a sideload at the end.

I ran this with Pixel Infinity, but the flow is not tied to one ROM. Pixel Infinity, crDroid, LineageOS, Evolution X, PixelOS and most other AOSP builds that come with a recovery image all follow the same path.

One honest note before you start. In my own run, the ROM zip I had was corrupt, so there is a gap in the footage where I re-downloaded it. That is exactly the mistake to dodge. Check the file before you start, not after the sideload dies at 60 percent.

## What you need

- Two Android phones: the one being flashed, plus a helper phone.
- A USB cable that actually holds a connection. This is not the place for the cable from the drawer.
- The vendor_boot or boot image that matches your ROM and your model.
- The ROM zip built for your exact device.
- The free Rom Flasher tool installed on the helper phone.

## Step 1 — connect both phones and let the tool detect the device

Plug the helper phone into the target phone with your good cable. Open the tool on the helper and let it detect the target device. If it does not show up, stop here and sort the connection and the USB debugging permission first. Nothing later in these steps will work if this one does not.

## Step 2 — flash the vendor_boot or boot image

This is the one step where the model matters. Some devices need the vendor_boot image, some need the plain boot image. Check which one your device tree and your ROM's release post call for, and use the image that matches your exact model.

Flash that image from the helper phone. When it finishes, do not pull the cable yet.

## Step 3 — reboot into recovery

Use the advanced reboot menu on the target phone to boot into recovery. You should land in the recovery that came with the ROM, not the phone's stock one. If it boots back to the system instead, the image did not take — go back to Step 2 and check you used the right image for your model.

## Step 4 — format data, then go back

Format data in recovery. Yes, this erases everything on the phone. It is not optional here, and skipping it is the fastest route to a bootloop.

Once the format is done, go back to the main recovery menu. Do not reboot yet.

## Step 5 — apply the update over ADB

Choose **Apply update**, then **Apply from ADB**. This puts the phone into sideload mode and waits for the ROM file.

## Step 6 — sideload the ROM zip

Send the ROM zip across and let it run all the way to the end. Watch the progress on the target phone. If it stops early, the file is probably bad — that is the corrupt-zip failure I hit myself.

## Step 7 — decline extras and reboot

When the sideload finishes, recovery may offer to install additional packages. Answer **No**. Then reboot to the system and give the first boot its time.

## Where people get stuck

- **The wrong image.** Using boot when your device wants vendor_boot, or the other way round, means recovery never appears. Match your model exactly.
- **A corrupt ROM zip.** Sideload stalls or fails on a broken file. Check the file before you start so you are not re-downloading at midnight.
- **Skipping the data format.** It ends in a bootloop almost every time. Format data, then sideload.

## The honest catch

This method needs one thing you cannot fake: a recovery-based build for your exact device. If your phone only has fastboot builds, this route does not apply, and you will need a PC after all. Check that first, before you download anything else.

Also, your bootloader must already be unlocked. Flashing a custom recovery on a locked bootloader is not something this method gets around. Unlocking wipes the phone, so if you have not done it yet, that is your real first step.

If you want the driver side handled for you when you do have a PC, the free Rom Flasher tool on GitHub also bundles the ADB and fastboot driver install. It is free, and the link is in the downloads section.

::faq
Q: Do I really not need a PC to install an AOSP ROM?
A: Not on this route. The whole flash runs from a helper Android phone, so you do not need a laptop or Termux. The catch is that your ROM has to be a recovery-based build for your exact device.

Q: Which phones can I use as the helper?
A: Any working Android phone that can run the free Rom Flasher tool and hold a stable USB connection. The helper does the flashing; your target phone is the one that gets wiped.

Q: Do I need an unlocked bootloader for this?
A: Yes. Flashing a custom recovery needs an unlocked bootloader, and this method does not change that. Unlocking also wipes your data, so do it before you plan the install.

Q: Can I keep my data this way?
A: No. Formatting data is a required part of the process, so move anything you care about off the phone first. Expect a fresh setup wizard after the reboot.

Q: The sideload stopped partway through. What went wrong?
A: Most often the ROM zip is corrupt or incomplete. Re-download it and check the file before trying again. Sideload stops or fails on a broken file.
