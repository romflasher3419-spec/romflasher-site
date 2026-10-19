::summary
MistOS v4.3 on the Poco X7 Pro is an Android 16 build that needs one step most ROMs skip: flashing the vendor_boot image in fastboot before recovery. Miss that and recovery will not mount anything. Here is the exact order, plus the recovery timing trick that catches people out.

::body
MistOS is the sort of build that sits close to AOSP but keeps a bit of its own personality, so it does not feel like a carbon copy of every other stock Android ROM. On Android 16 the base is fresh and the first boot is quick, provided you get the vendor step right.

That proviso is the whole article. MistOS on the Poco X7 Pro is a two-stage flash. First the vendor_boot image goes on in fastboot. Then you boot recovery, format data, and sideload the ROM. Do it in that order and the job is boring in the best way. Do it out of order and you will be staring at a recovery that refuses to mount anything and wondering if you broke the phone.

You did not break the phone. You just skipped a step.

## What you need

- The MistOS v4.3 ROM zip for the Poco X7 Pro.
- The matching vendor_boot image from the vendor link. Not a vendor image for another build, and not one you had lying around from a previous ROM.
- adb and fastboot on a PC. If you would rather not use a PC, a terminal app on the phone works, and the commands are the same, just typed on the device.
- A data USB cable that stays connected. Charge-only cables are a real thing and they will waste your evening.
- Enough battery, and a backup you would not cry over.
- Your IMEI written down. Clean flash, so have it somewhere off the phone.

## Step 1 - flash the vendor_boot image

Put the phone in fastboot and flash the vendor image to both slots:

`fastboot flash vendor_boot --slot=all vendor_boot.img`

The `--slot=all` part matters on devices with A/B slots. Flashing one slot and leaving the other behind is a classic source of a phone that boots into the wrong half of the system.

If fastboot says it is waiting for a device, your driver is not installed properly. Fix that now, not halfway through.

## Step 2 - catch the recovery window

This is the step that catches people. Type the reboot command, then watch the screen. The moment it goes dark, hold volume up and keep holding until recovery appears.

You get one short window here. Miss it and the phone boots to system with a vendor image on it and no ROM flashed, which then looks like a broken build. It is not. Power off and try again, a little quicker on the volume key this time.

## Step 3 - format data

Once you are in recovery, format data. Not a wipe, format. This build needs a clean flash, so a dirty flash over another ROM will either bootloop or come up with services crashing. If you came here from a different ROM, do not skip this because you are in a hurry.

## Step 4 - sideload the ROM

Choose the sideload option in recovery and push the zip from your PC with `adb sideload`. Alternatively, many recoveries will let you drag the zip straight into the terminal window, which is the same thing with fewer keystrokes.

It will print progress and then something that looks like it stalled near the end. Leave it. Sideloading always looks like that.

## Step 5 - extras, then first boot

When it asks whether you want to continue, say yes. This is the point where you can flash GApps or Magisk if you want them. Then reboot to system.

First boot takes a while, longer than stock, and the logo may sit there long enough to make you nervous. Give it several minutes before you conclude anything is wrong.

## Where people get stuck

- **Booting to system with no vendor image.** Recovery mounts nothing, and it looks like a dead build. Flash the vendor_boot image first, every time.
- **Missing the recovery window.** Not holding volume up fast enough sends you straight to system. Watch for the screen going dark and be ready.
- **Dirty flashing over another ROM.** Different ROM, clean flash. Then blame nothing.
- **Using a vendor image from the wrong build.** It flashes happily and then behaves strangely. Match it to MistOS v4.3.

## One honest note

The vendor step is genuinely annoying. It is an extra flash, an extra reboot, and a timing window you can miss. It is the price of running Android 16 on this device with this method, and once you know the order it takes about two minutes. But if you are coming from a ROM that flashed in one clean sideload, expect to relearn the rhythm.

If the driver side of this is where you always get stuck, the free Rom Flasher tool on GitHub bundles the ADB and fastboot driver install so you are not hunting through Device Manager at midnight.

::faq
Q: Do I need to flash vendor_boot before MistOS v4.3?
A: Yes, flash the vendor_boot image in fastboot first, with `--slot=all`, then boot recovery and sideload the ROM. Skip it and recovery will not mount anything, which looks like a broken build.

Q: Can I flash MistOS from my phone without a PC?
A: Yes. A terminal app on the phone can run the same fastboot and sideload commands. It is the same process, just typed on the device instead of your PC.

Q: Why did my phone boot to system instead of recovery?
A: You missed the recovery window. After the reboot command, hold volume up the moment the screen goes dark and keep holding. If you are late, the phone boots to system and you need to power off and try again.

Q: Can I dirty flash MistOS over my current ROM?
A: No. Clean flash is mandatory on this build, so format data in recovery before sideloading. Dirty flashing over another ROM usually ends in a bootloop.

Q: Will flashing MistOS wipe my data?
A: Yes. Formatting data in recovery erases internal storage, and the flash brings the phone back to the setup wizard. Back up your files and note your IMEI before you start.
