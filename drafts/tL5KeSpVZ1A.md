::summary
OxygenOS 16 runs on the POCO X7 Pro through a community port built from the
OnePlus Nord CE 5. Setup is clean, Google restore works, and the OnePlus look is
all there. Fingerprint and face unlock do not work yet, so read the gaps before
you wipe your phone for this one.

::body
OxygenOS on a Poco is the interesting part of this whole thing. It is a community
port pulled from the OnePlus Nord CE 5, running on the X7 Pro (rodin), and I
flashed it clean to find out what actually works instead of what the feature list
claims. This is the Hotfix V2 build, updated at the end of November, credited to
MS.ACHRAF.

Here is the honest version, section by section.

## What it looks like once it boots

The OnePlus feel is real and it does not need a description half as long as the
one I could write. You get the Oxygen launcher, the settings layout, the
notification shade and the animations that go with them. Nothing about it looks
half finished on the surface.

The bigger surprise is setup. It is genuinely clean. You pick your language,
English or the regional options a global build usually carries, and you get
through the wizard without a fight. Google account restore worked for me, app data
included, so you are not starting from an empty phone. That alone puts this port
above a lot of community builds.

## What works

- First boot and the whole setup wizard.
- Regional language support, the way you would expect from a global build.
- Google account restore, with app data coming back.
- The OxygenOS settings layout and notification shade.
- The launcher, quick toggles and animations.
- Daily feel. Scrolling, app switching, and the general rhythm of the phone.

For a port, that is a solid list. It is the stuff you touch every day, and it
holds up.

## What is broken, and be honest about this part

- Fingerprint unlock does not work yet.
- Face unlock does not work yet.
- Some of the smaller edge features you would get on a real OnePlus are missing
  or rough, which is normal for a port of this age.

Those first two are the ones that matter. A phone without a fingerprint reader is
a different phone. You will be typing your PIN every single time, at the lock
screen, in banking apps, in password managers. That sounds like a small thing on
paper and it is a constant annoyance in real life.

I am flagging it plainly because finding out after you have wiped your phone is
the worst possible way to learn it.

## How the flash goes

This one is fastboot based with a `.bat` installer, which makes it one of the
easier builds to get onto the device. You boot to fastboot, run the script for
your operating system, and let it work. Read the menu carefully when it asks about
root, and pick the option you actually want instead of clicking through it.

As always, this wipes the phone. Back your data up first.

## Who should install this

Install it if you want the OnePlus look on a Poco and you can live without
biometrics for now. The port boots, the setup is clean, and Google restore means
you are up and running quickly.

Skip it if you rely on fingerprint or face unlock. That is not a small gap on a
phone you use every day, and no amount of nice animations makes up for typing a
PIN forty times a day.

## The honest verdict

The port boots and runs. Setup is genuinely clean and Google restore works, so you
are not starting from zero. Fingerprint and face unlock are the big missing pieces
right now, and that is the trade you are making. It is a good choice for someone
curious about the OnePlus experience on their Poco. It is not yet a daily driver
for everyone, so know the gaps before you flash.

If the driver side of the flash is the part that slows you down, the free Rom
Flasher tool on GitHub installs the ADB and fastboot driver for you in a couple of
clicks. It is free, and the link is in the downloads section.

::faq
Q: Does fingerprint unlock work on the OxygenOS 16 port for the POCO X7 Pro?
A: No, not yet. Fingerprint and face unlock are both missing in this build, so you
will be unlocking with a PIN or pattern for now.

Q: Is this port safe to use as a daily driver?
A: That depends on you. The ROM boots and runs well and Google restore works, but
without biometrics many people will find it hard to live with every day.

Q: Which phone is this port based on?
A: It is ported from the OnePlus Nord CE 5, credited to MS.ACHRAF, and running on
the POCO X7 Pro with codename rodin.

Q: How do I install OxygenOS 16 on the POCO X7 Pro?
A: It is fastboot based with a .bat installer. Boot the phone to fastboot, run the
script for your operating system, and read the menu when it asks about root.

Q: Does flashing this wipe my data?
A: Yes. A port flashed this way formats the phone, so copy your photos and files
off first and expect the setup wizard on the first boot.
