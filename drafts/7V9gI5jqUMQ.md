::summary
A new build landed after a long gap on the channel, and this clip is the short
version of it. There is no install walkthrough here, just what changed since the
last build and the free tools that get used for every flash. The hardbrick guide
and the tool links all sit in the downloads.

::body
I have been quiet on the build side for a while. Not gone, just making things.
Then this one finally came together, and it deserved a marker rather than a
full walkthrough.

So this clip is short on purpose. It shows the update, says what changed, and
points at the files I keep pinned for every install. If you have followed this
channel for any length of time, none of the tools will be new to you. They get
used on every flash I do, and they have not changed.

## What is in this clip

- A fresh build arriving after a long break
- A quick look at what moved since the last one
- The tools I keep pinned, unchanged and free
- No install steps, no long setup, no file-by-file walkthrough

If you came here wanting to flash something today, this is the wrong video to
follow. It is the update, not the tutorial.

## The tools, since they come up every time

Two things do the actual work here. There is the Android side, which runs from
the phone itself, and the Windows side, which handles fastboot and recovery jobs
with a cable. Both are free and both are in the downloads listed with this video.
I run the same files on my own POCO X7 Pro.

Alongside those sit the standard pieces anyone flashing needs:

- **ADB and Fastboot platform files** for the PC. Without these, fastboot does
  not exist on your machine and every command fails with a version of "not
  recognized".
- **The ADB and fastboot driver**, so Windows stops showing your phone as an
  unknown device the moment you plug it in.
- **The hardbrick guide**, which I keep linked for a reason.

That last one is the most important link on this page. Nobody opens a hardbrick
guide on a good day. You open it when the phone is sitting there dead, the
screen will not wake, and you are searching at an hour when you should be
asleep. Having it saved before that happens is the whole point.

## Why the gap was long

Custom ROM work is not a straight line. Builds come together slowly, things get
rebuilt, features get pulled back out because they were not ready, and the parts
that survive are the parts worth filming. I would rather show you something that
works than something that will break on your device two days after you install
it.

## If you are flashing something soon

Two pieces of advice, and I mean both of them.

Slow down. Read the steps twice before you touch anything. Most messages I get
about dead phones trace back to a wrong file or a skipped format, not to the ROM
itself. The ROM rarely does the damage. The hurry does.

And back up before you start. Unlocking the bootloader wipes the phone, and so
does a clean flash. Move your photos and anything else you care about onto a PC
or into the cloud first, and do it the day before, not while you are waiting for
a download to finish.

::faq
Q: Where are the tools you use for flashing?
A: Everything is in the downloads listed with this video. The free Rom Flasher
tool, the ADB and fastboot files, the driver pack and the hardbrick guide are all
there, and none of them cost anything.

Q: Does this video show a full install?
A: No. This clip is an update after a long gap. It shows the new build and the
tools, but the step-by-step installs are in the longer videos.

Q: Should I flash a build as soon as it comes out?
A: Not necessarily. Read the notes that come with it, check it matches your exact
model, and back up first. A little patience saves a lot of recovery work.

Q: Why do I need the driver if I already have the platform files?
A: The platform files give your PC the fastboot command, and the driver is what
lets Windows recognise the phone when it is connected in fastboot mode. Without
the driver, you get an empty device list.

Q: Can I keep using the same files for later flashes?
A: Yes. Grab them once and keep them somewhere you can find again. They do not
change between builds, and having them saved means you are not downloading
drivers while your phone sits in fastboot mode.
