::summary
Axion OS for the POCO X7 Pro is an Android 16 build that brings the Mi camera and Dolby back to an AOSP ROM, with SELinux left enforcing. The install is short: push vendor_boot to both slots, catch recovery with Volume Up, format data, then sideload the zip. Once it boots, leave the Reality Display Engine setting alone.

::body
Two things usually go missing when you move to an AOSP ROM on this phone. The camera turns into a barebones app, and the speakers lose the tuning you paid for. Axion OS is the build that puts both back. The Mi camera is in there, Dolby is in there, and the rest of the system is a normal Android 16 base.

The other detail worth knowing before you start: SELinux stays enforcing and the build is signed. If you have apps that poke at the system to see whether it has been tampered with, that combo is what keeps them calm.

One warning from the maintainer, and it is not optional. Stay away from the Reality Display Engine setting. It is the one documented issue in this build.

## What you need first

- The **Axion OS zip** for the POCO X7 Pro (rodin). This is not a build for a different phone, and flashing it on one will not end well.
- The **vendor_boot.img** that goes with this release. You will flash this before the ROM, so download it at the same time.
- A **PC with ADB and fastboot** working. The driver matters here. If Windows shows an unknown device when you plug the phone in, fix that before you continue.
- An **unlocked bootloader**, over 50% battery, and a cable you trust.
- A **full backup**. This wipes internal storage, so photos and downloads come off first.

## Step 1 - get into fastboot

Power the phone off, then hold **Volume Down + Power** until the fastboot screen appears. Plug it into the PC and check that it is visible:

`fastboot devices`

If nothing shows up here, stop. No amount of retrying the flash fixes a phone the PC cannot see.

## Step 2 - flash vendor_boot to both slots

This is the one fastboot command that matters:

`fastboot flash vendor_boot --slot=all vendor_boot.img`

The `--slot=all` part is the point. This phone has A/B slots, and the vendor_boot needs to be on both of them, otherwise the recovery you land in depends on which slot the phone happens to boot.

## Step 3 - catch recovery with Volume Up

Run `fastboot reboot` and hold **Volume Up** as soon as you do. Do not type `fastboot reboot recovery` instead. That specific command is a known trap on this device, and the usual result is a phone that boots back into the system while you sit there wondering what happened.

If you miss the window, the phone starts setting up Android. Let it finish, shut it down, and try again. Nothing is broken.

## Step 4 - factory reset, then format data

In recovery, do a factory reset and then **format data**. Both, in that order. Format data is what clears the old encryption, and skipping it is the reason people see the ROM boot and then behave strangely.

## Step 4b - sideload the ROM

Choose **Apply update**, then **Apply from ADB**. On the PC, in the folder where your ROM zip sits:

`adb sideload your-rom.zip`

The progress bar on the phone will stop around the halfway mark. That is normal and not a failure. When recovery asks you to confirm, pick yes.

## Step 5 - first boot

Choose **Reboot system** and then leave the phone alone. First boot on a new Android 16 build takes a few minutes and reboots once on the way. Let it get to the setup wizard before you judge anything.

## Where people get stuck

- **The display engine setting.** Touching it is the known issue. Leave it.
- **`fastboot reboot recovery`.** It does not reliably land you in recovery. Hold Volume Up instead.
- **Flashing GApps on top.** This is already a GApps build. Adding another pack creates a mess you cannot easily untangle.
- **The wrong vendor_boot.** Mismatched files are the reason a flash finishes but the phone will not boot.

## Is the camera really the Mi one?

Yes. It ships inside the build, so you get the modes you were used to rather than a stripped-down camera app. That is the main reason to try this ROM. Everything else is a clean Android 16 experience.

## One honest paragraph

This is a first build, so treat it like one. The camera and Dolby are the wins, and the system is stable enough to use day to day. Do not expect the polish of a ROM that has had a year of releases behind it, and do read the display engine note one more time before you go poking around the display settings.

If the driver side of this is where you usually give up, the free Rom Flasher tool bundles the ADB and fastboot driver install into a couple of clicks so you are not fighting Device Manager at midnight. The link is in the downloads section.

::faq
Q: Does Axion OS for the POCO X7 Pro come with GApps?
A: Yes, this is a GApps build. Play services and the Play Store are included, so you do not need to flash a separate package, and you should not.

Q: What is the Reality Display Engine issue?
A: Changing that setting is the one documented problem with this build. The maintainer's advice is to leave it alone, so open display settings, look at it if you want, and change nothing.

Q: Why does the vendor_boot have to go to both slots?
A: The phone has A/B slots. Flashing vendor_boot with `--slot=all` puts it on both, so whichever slot the phone boots from, the recovery and boot chain match the ROM you are installing.

Q: Can I use `fastboot reboot recovery`?
A: No, hold Volume Up after `fastboot reboot` instead. That command is one of the known ways people miss the recovery window and end up booting into the system by accident.

Q: Does installing this wipe my phone?
A: Yes. Recovery formatting wipes internal storage, so copy your photos and files off first. Set the phone up on the empty system before you restore anything.

Q: Will it bootloop if I use the wrong vendor_boot?
A: It can. Use the vendor_boot that came with this Axion OS release for the POCO X7 Pro rather than one from a different build, and flash it to both slots in the step above.
