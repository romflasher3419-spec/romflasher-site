::summary
Project Infinity X 3.6 is the first Android 16 QPR1 build for the POCO X7 Pro, and
it is a signed GApps release with haptics back on the QTI vibrator and fingerprint
calibration for jiiov sensors. Flash vendor_boot to both slots, reboot into
recovery with Volume Up, format data and sideload the zip.

::body
Project Infinity X 3.6 is the QPR1 drop the maintainer was aiming for, and it
landed earlier than the version name suggests. If you have been waiting for an
Android 16 build on the POCO X7 Pro that does not feel like a science project,
this is the one to start with. It is signed, it is a GApps build, and two of the
old annoyances on AOSP for this phone are finally gone.

## What is new in 3.6

- Initial Android 16 QPR1 release, synced with the latest upstream source
- Back on the QTI vibrator, with haptic strength control instead of one fixed
  level
- Fingerprint calibration included for jiiov sensors, which used to be the
  irritating part of AOSP on this hardware
- Shipped eng-preloader
- A fingerprint calibration test ships with the build
- 2.4GHz and 5GHz hotspot settings split apart
- Basic call recording added
- MiuiCamera is dropped, so do not go looking for it
- Minor changes underneath

That vibrator change is small and you notice it immediately. One fixed buzz
setting is worse than it sounds once you have lived with it for a week.

## What you need

- The Project Infinity X 3.6 zip for the POCO X7 Pro
- vendor_boot.img from the same download page
- A PC with ADB and fastboot and the driver installed, or Termux on a second
  Android phone if you have no PC
- A full backup
- Your fingerprint and lockscreen PIN removed before you start

That last point is not optional. Clear the lockscreen settings and delete the
fingerprint first. Carrying them into the flash is a common cause of trouble at
first boot.

## Step 1 - remove the lockscreen security and boot to fastboot

Delete your fingerprint, then remove the PIN or pattern, then power the phone off.
Hold Volume Down and Power until the fastboot screen appears. Confirm the PC sees
it:

`fastboot devices`

## Step 2 - flash vendor_boot to both slots

`fastboot flash vendor_boot --slot=all vendor_boot.img`

Both slots. The `--slot=all` flag is there for a reason, and doing one slot only
leaves you with a phone that boots correctly once and then acts strange after the
next update.

## Step 3 - reboot and catch recovery with Volume Up

`fastboot reboot`

Hold Volume Up the instant it restarts. You are aiming for recovery, not for the
old system. If you are late, you will boot into what was already there, and you
start again from step 2.

And to say it plainly: do not use `fastboot reboot recovery` on this phone. It
can brick the device. The Volume Up hold is the way.

## Step 4 - factory reset and format data

Factory reset first, then format data. Both. This is a clean flash, and it is the
right call whether you are coming from another ROM or from another Android
version. Skipping it is the classic route to a bootloop.

## Step 5 - sideload the ROM zip

Pick Apply update, then Apply from ADB. On the PC, type `adb sideload` and drag
the zip into the terminal window so the path fills in by itself. Press enter and
watch it run to the end.

When it asks, choose yes and reboot to system. Do not flash a GApps package on
top of this build. It already is one, and stacking another one is how people
break a working install.

## Step 6 - first boot

Long first boot. Let it sit. QPR1 builds take their time on the very first start,
and pulling the cable during setup is the worst thing you can do at this stage.

## Flashing without a PC

If you do not have a Windows machine, Termux on a second Android phone handles
the same flash. The steps are the same, the commands are the same, and the phone
doing the flashing is simply standing in for the PC. It is a neat trick and it
works, though I would still take a PC if one is available, purely because the
screen makes errors readable.

## Where people get stuck

- **Using `fastboot reboot recovery`.** It can brick the phone. Volume Up hold
  after a normal reboot is the safe route.
- **Keeping the old fingerprint.** Clear the lockscreen settings and fingerprint
  before you flash, or you will fight the phone at first boot.
- **Flashing GApps on top of the build.** It is already a GApps build. Adding
  another package breaks things rather than adding anything.
- **Dirty flashing from another ROM or Android version.** Do the factory reset
  and the data format even when it feels like extra work.

## One honest note

The camera story on 3.6 takes a second to explain. MiuiCamera is dropped, but
there is still a camera app in the build, so you are not left without one. If you
were specifically attached to MiuiCamera, this is the build where that stops
being an option.

Termux is the other thing worth knowing about before you decide you cannot flash
this. A lot of people assume a PC is mandatory. It is not here, and the flash
file for that route is in the downloads.

If the driver install is the part that usually stops you, the free Rom Flasher
tool puts the ADB and fastboot driver in with a couple of clicks instead of a trip
through Device Manager. It is free, and the link is in the downloads section.

::faq
Q: Is Project Infinity X 3.6 the first Android 16 QPR1 build for the POCO X7 Pro?
A: Yes, it is the initial QPR1 release for this device, synced with the latest upstream source. It is a signed GApps build.

Q: Can I flash Project Infinity X 3.6 without a PC?
A: Yes. Termux on a second Android phone runs the same commands and handles the flash. A PC is easier to read errors on, but it is not required.

Q: Does this build have MiuiCamera?
A: No. MiuiCamera was dropped in 3.6, so do not go looking for it in the package. The build still ships with a camera app.

Q: Do I need to remove my fingerprint before flashing?
A: Yes. Delete your fingerprint and remove your lockscreen PIN or pattern first. Keeping them is a common reason people run into problems at first boot.

Q: Do I need to flash GApps separately on this build?
A: No. It is already a GApps build, so Play Store is there on the first boot. Flashing another GApps package on top of it can break the install.
