::summary
This was a live session about flashing tools, where each file lives, and the
questions that come up while people set their phones up. The useful part is
seeing the toolkit laid out in one place: the ADB driver, Platform Tools,
recovery images and vbmeta for common Xiaomi and POCO devices. Nothing here is a
magic fix, just the same steps talked through live.

::body
This one ran live, so it moves at its own pace and follows the questions instead
of a script. If you are new to flashing, the part worth your time is seeing the
whole toolkit in one place. Those files are the difference between your first
fastboot command working and the PC staring back at you with no device found.

Nothing in the session is a shortcut. It is the same set of steps you see in the
other videos here, just talked through out loud while people are setting up.

## The toolkit, item by item

- **The ADB and Fastboot driver.** Start here. Without it, Windows sees your
  phone in fastboot mode as an unknown device, and nothing else you do will help.
- **Platform Tools.** The files that give your PC the actual adb and fastboot
  commands. Extract them somewhere permanent instead of opening them from the
  downloads folder.
- **Recovery images.** Device specific. A recovery built for one model does not
  work on another, even when the names look similar.
- **vbmeta.** The piece people forget, and the reason a ROM installs cleanly and
  then refuses to boot.

That last point is where a lot of first attempts end. The install finishes, the
phone reboots, and it drops straight back into recovery or sits on a black
screen. Often enough, the missing piece was vbmeta, or a vbmeta flashed with the
wrong flags for the ROM being installed.

## Where each file is used

The driver and Platform Tools are your PC side. You need them before anything
else, because everything in fastboot runs through them. Set them up once and they
are done forever.

Recovery images matter when you are installing a ROM rather than doing a fastboot
flash of an official package. Take the one built for your exact device.

vbmeta comes into play on AOSP style ROMs, where the build needs verification
disabled to boot properly. Follow the instructions that come with your specific
ROM rather than assuming one setting fits every build.

## The files people forget before their first flash

- The **driver**, because they assume the cable is enough
- **vbmeta**, because the ROM zip does not always shout about it
- A **backup**, because unlocking the bootloader wipes internal storage and so
  does a clean flash
- The **right model**. A file for another variant will flash and then refuse to
  boot, which is a much longer evening

## What fastboot actually does

Fastboot talks to the phone while it is sitting in bootloader mode. It writes
partitions directly: boot, recovery, vbmeta, super and the rest. There is no
operating system in the way and no safety net either. What you write is what the
phone gets.

That is why the model and the file matter so much. In recovery, there is a
package checking what it is installing. In fastboot, you are handing the phone
raw pieces and telling it where to put them.

## Setting up without flashing anything today

You do not have to install a ROM to get value out of this. Install the driver,
extract Platform Tools, run `fastboot devices` with the phone connected in
fastboot mode, and confirm you get a serial number back. That single check tells
you whether your machine is ready, before you are depending on it.

Do that on a quiet evening and you will not be troubleshooting drivers at the
moment you are halfway through an install.

If the driver setup is the part that keeps costing you an evening, the free Rom
Flasher tool on GitHub bundles the ADB and fastboot driver install into a couple
of clicks. It is free, and the link sits in the downloads with everything else.

::faq
Q: Which file do I need first before flashing anything?
A: The ADB and fastboot driver, then Platform Tools. Without the driver, Windows
does not recognise your phone in fastboot mode, and without the platform files
the fastboot command does not exist on your PC.

Q: Will the same recovery file work on every phone?
A: No. Recovery images are built for a specific device. Take the one made for
your exact model, because a recovery for another variant will not work.

Q: Why do I need vbmeta for an AOSP ROM?
A: On AOSP style builds, verification usually needs to be disabled for the ROM to
boot properly, and vbmeta is where that happens. Follow the instructions that
come with your specific ROM instead of copying settings from another build.

Q: My phone installs the ROM and then will not boot. What did I miss?
A: A missing or incorrectly flashed vbmeta is one of the usual causes, along with
a file built for a different model. Recheck the install notes for your exact ROM
and your exact device.

Q: Is the Rom Flasher tool free?
A: Yes, completely free. Download it and use it. The link is in the downloads
along with the platform files and the driver.
