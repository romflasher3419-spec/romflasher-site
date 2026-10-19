::summary
ELITE HyperOS runs on the POCO X7 Pro (Rodin) on an Android 16 base, and the
install is short: extract the zip, run the script for your system, confirm the
format, and wait. This is the Lite build, so the feature list is shorter than the
Pro version, and the Play Store shows as not certified out of the box.

::body
The install is the short part on this one. HyperOS-based builds usually are. You
extract the zip, run the script for your operating system, confirm that your data
will be formatted, and let it work. If you would rather not touch a PC at all, the
Termux route on the phone works too.

Then comes the part that actually decides whether you keep it. So here is the
tour, and the honest edges.

## What you get on first boot

The home screen, wallpaper and the Google widget setup all land the way HyperOS
normally does. Nothing feels rushed or half assembled, which is more than you can
say for a lot of modded builds.

One small detail that says a lot: the calculator works after first boot. On a lot
of modded ROMs it is the first thing that breaks, so seeing it behave here is a
good sign about how carefully the build was put together. The Mi camera app is
still in place too, so you are not stuck with a half-finished replacement camera.

## What was tested

- Install and first boot on the Android 16 base.
- Home screen, wallpaper and the Google widget setup.
- Mi camera, calculator and the usual system apps. The calculator works.
- Play Store certification state out of the box.
- The Lite customisation menu, which has more in it than the name suggests.
- Whether a PC is needed. It is not, the Termux route works.

## How the install goes

1. Download the ROM zip for the POCO X7 Pro (Rodin).
2. Extract it into a folder you can find again, with 7-Zip or WinRAR rather than
   the built-in Windows extractor.
3. Boot the phone to fastboot, or start the Termux route if you are flashing from
   the phone itself.
4. Run the script for your operating system.
5. Confirm when it tells you your data will be formatted. This is not a warning
   you can decline your way out of.
6. Let it finish, and let the first boot take its time.

That is the whole job. The reason this ROM is popular is that it does not ask you
to babysit a long list of commands.

## Where people get stuck

- **Extracting with the built-in Windows tool**, which sometimes flattens the
  folder structure and leaves the script unable to find its images.
- **Declining the format** because a backup has not been made. Move your photos
  off before you start, not after the prompt appears.
- **Expecting the Pro feature list from a Lite build**. They are different, and
  that is covered next.
- **Assuming the Play Store will be certified** without doing anything.

## Lite versus Pro, said plainly

This is the Lite build. The Pro version of this ROM carries a much longer feature
list, and I am not going to pretend the Lite one has all of it. If you are used to
the Pro build, you will notice what is missing.

What that leaves you is a lighter HyperOS with the core experience intact. For
daily use, everything important is in place, the Mi camera is still there, and the
customisation menu still has more in it than the name suggests.

The one thing to sort yourself is Play Store certification. It shows as not
certified after first boot, so the integrity side is on you. That is a normal
trade for a modded HyperOS build, but do not be surprised when your banking app
looks at you sideways.

## Who should install this

Install it if you want HyperOS with a lighter feature set and you do not mind
sorting certification on your own. Skip it if you want every extra from the Pro
release, because this build simply does not carry them.

If the driver side of flashing is the part that slows you down, the free Rom
Flasher tool on GitHub installs the ADB and fastboot driver in a couple of clicks.
It is free, and the link is in the downloads section.

::faq
Q: Can I flash ELITE HyperOS without a PC?
A: Yes. The Termux route works from the phone itself, so you do not need a PC for
the flash at all.

Q: Does installing ELITE HyperOS wipe my data?
A: Yes. The installer formats data as part of the process. Back up your photos and
files before you run the script.

Q: Is the Play Store certified on this build?
A: Not out of the box. It shows as not certified after first boot, so you need to
sort the integrity side yourself.

Q: Is this the Lite or the Pro version of the ROM?
A: This is the Lite build. The Pro version carries a much longer feature list, so
go Pro if you want every extra rather than the lighter set.

Q: Does the Mi camera app still work?
A: Yes. The Mi camera is still in place on this build, so you are not left with a
half-finished replacement camera app.
