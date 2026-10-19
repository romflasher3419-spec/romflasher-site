::summary
Project Infinity X 3.3 is a GApps Android 16 build for the POCO X7 Pro, and it is
stable enough to use daily. You flash vendor_boot to both slots, reboot into
recovery by holding Volume Up, format data and sideload the zip. Two quirks will
trip you up if nobody warns you, so read those first.

::body
You have decided to move the POCO X7 Pro onto Project Infinity X 3.3, and now you
are staring at a procedure that starts with flashing something called
vendor_boot and ends with typing a sideload command. It sounds worse than it is.
The whole job is maybe fifteen minutes, and the only two parts that genuinely
catch people are in the warning list below.

## Read this before you touch anything

Two things on this build are worth knowing in advance, because both are miserable
to find on your own:

- **Do not switch the display colour setting to X-Reality.** Leave it alone. On
  this build it leaves you staring at a blank white screen.
- **If quick settings and the main settings app feel laggy,** toggle the
  window-level blur option off and then back on. It sounds like nonsense. It
  fixes it.

Neither of these is a reason to skip the ROM. They are just the price of going
first.

## What is in this build

- Project Infinity X 3.3, built on Android 16
- GApps included, so Google services are there from the first boot
- Signed userdebug build with SELinux enforcing
- Changelog is short: source synced upstream, some minor changes underneath,
  and USB tethering fixed
- A separate fix handles the Aperture video issue

The GApps plus enforcing SELinux combination is why I would happily run this as a
daily phone rather than a weekend experiment.

## What you need

- A backup of your IMEI, and your photos, chats and files copied off the phone
- The vendor_boot image built for this exact ROM version
- The Project Infinity X 3.3 zip
- ADB and Fastboot driver on your PC, plus Platform Tools
- A charged phone and a cable you trust

Do the backup first. Not while the flash is running. Now.

## Step 1 - flash vendor_boot to both slots

Boot the phone to fastboot and confirm your PC sees it before anything else.

Then flash the vendor_boot image to both slots in one command:

`fastboot flash vendor_boot --slot=all vendor_boot.img`

Wait for both slots to report finished. Doing it to one slot only is how people
end up with a phone that boots into the wrong thing.

## Step 2 - reboot and catch the recovery key window

Run:

`fastboot reboot`

The moment it reboots, hold Volume Up. Hold it early rather than exactly on time.
If you are late, the phone boots the old system, and you start over from step 1.

One warning that deserves its own line: **never use `fastboot reboot recovery` on
this device.** The notes are blunt about it and say it can brick the phone. Do it
the Volume Up way.

## Step 3 - format data

In recovery, format data first. This is a clean flash and a mandatory one. Do not
stack this ROM on top of another. Formatting is what stops the bootloop you would
otherwise spend an hour chasing.

Then go back out to the main recovery menu.

## Step 4 - sideload the ROM

Choose Apply update, then Apply from ADB. On your PC, type:

`adb sideload`

and drag the ROM zip into the command window so it fills in the path for you.
Press enter and watch the percentage climb.

When it reaches the end, it will ask whether you want to reboot to recovery. Say
yes if you want to add GApps or Magisk, since that is when you would do it. Then
reboot to system.

## Step 5 - first boot

It will sit on the boot logo for a while. That is normal. Do not pull the cable,
do not force a restart. Just let it come up.

## Where people get stuck

- **Using `fastboot reboot recovery`.** Just do not. Volume Up after a normal
  reboot is the safe path on this phone.
- **Missing the recovery key window.** If the phone boots into the old system,
  nothing is broken. Start again from the vendor_boot step.
- **Dirty flashing.** Format data. Every time you come from another ROM or
  another Android version.
- **Changing the display colour profile.** X-Reality on this build gives you a
  white screen. Stay away from it.

## One honest note

The laggy settings quirk annoyed me until I knew the fix, and then it stopped
existing. That is the trade with a build this fresh, and both of these are known
issues written down rather than mysteries you have to solve. Expect the next
version to tidy them up.

If the ADB side of this is the part you keep redoing, the free Rom Flasher tool
installs the ADB and fastboot driver for you in a couple of clicks. It is free,
and the link is in the downloads section.

::faq
Q: Is a clean flash needed for Project Infinity X 3.3?
A: Yes. Format data before sideloading, especially if you are coming from another ROM or another Android version. A dirty flash here is asking for a bootloop.

Q: Does this ROM include Google apps?
A: Yes, it is a GApps build, so Play Store and Google services are there on the first boot. You do not need to sideload a separate GApps package.

Q: Why does the settings app feel laggy on this build?
A: It is a known quirk. Turn window-level blurs off and then back on in the settings, and the lag goes away. It is a small toggle, not a broken build.

Q: Can I set the display colour to X-Reality?
A: No. Leave the display colour setting alone on this build. Switching to X-Reality has been reported to leave you with a blank white screen.

Q: How do I enter recovery after flashing vendor_boot?
A: Run a normal fastboot reboot and hold Volume Up immediately. Never use the fastboot reboot recovery command on this device, because it can brick the phone.
