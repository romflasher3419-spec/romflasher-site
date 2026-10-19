::summary
Evolution X 12.1 on Android 17 is now running on the POCO X7 Pro (rodin), and you can install it with no PC and no Termux. You back up your data and your IMEI first, connect the phone to the tool, let it push the phone into fastboot, pick the ROM and the required files, and let it flash. MiCam, Dolby and Yuki Kernel 6.6.142 are all part of this build.

::body
You have probably flashed a ROM from a laptop before and remember the ugly part: drivers, a platform tools folder, a command that fails at 1 AM. This install skips that. It is Evolution X 12.1 on Android 17, built for the POCO X7 Pro, codename rodin, and the whole thing runs from the phone.

It is marked unofficial, the developer is @orubensgoncalves, the build is dated 05/09/2026 with the August 2026 security patch, and the base is HyperOS 3.0.301.0.

## What this build actually gives you

- Android 17 with a fresh device tree, not a patched-up older one
- MiCam back on board, which matters on an AOSP-style base
- Dolby included, so you keep that part of the sound
- Yuki Kernel 6.6.142 underneath
- Updated firmware and minor power improvements
- SELinux Enforcing, and a user build rather than a test build
- GApps and Vanilla variants, so you can pick whether Google is in the box

SELinux being enforcing is the detail I would look at first. It is the difference between a build that can pass as a daily driver and one that spends its life in permissive mode.

## What you need

- A POCO X7 Pro (rodin). Another device's package is the fastest route to a brick.
- The Evolution X 12.1 package plus the required files for rodin from the link.
- The Android tool for the no-PC route, or the PC tool if you would rather flash from a computer.
- A full backup, and a separate backup of your IMEI and NVRAM.
- The hard-brick fix guide saved somewhere on the phone or PC, just in case.
- Battery above half and a cable you trust.

## Step 1 - back up your data, then your IMEI

Do the normal backup first: photos, chats, downloads, whatever you cannot lose. Then do the one people skip, which is the IMEI and NVRAM backup. That second file is the difference between a bad flash and a very bad day, because a phone without IMEI data is a phone without a working network.

If you take one thing from this page, take that. It costs a few minutes and it has saved a lot of people.

## Step 2 - connect the phone and open the tool

Connect the phone and open the free Rom Flasher tool. It should detect the device by itself. At this stage the phone is just in normal Android mode, so you can check the connection is steady before anything is written.

## Step 3 - let the tool push the phone into fastboot

Let the tool put the phone into fastboot and confirm on the device screen. That confirmation is the safety catch. If you are not sure which screen you are looking at, put the phone down and read it before you agree.

## Step 4 - pick the ROM and the required files

Open the Flash section and select the Evolution X package plus the required files for rodin. Slow down on this screen. This is the one place where the wrong file turns a fifteen-minute job into an evening of recovery.

## Step 5 - let the flash run to the end

Start the flash and then leave the cable alone. Do not unplug it to check progress. Do not open another app. Do not let the phone go to sleep somewhere it should not. When it finishes, it reboots into the first boot on its own.

## Step 6 - first boot and the tour

First boot takes a few minutes, and the setup wizard comes after that. Then walk through what you actually got: the interface and customization options, MiCam, Dolby, performance, and how it behaves in a normal day. That last part is what decides whether the build stays on your phone.

## Where people get stuck

- No IMEI backup. This is the one that turns a bad flash into a very bad day.
- Flashing a package for another device. rodin only, always.
- Skipping the base requirement. Follow the ROM developer's notes instead of improvising, because the required files list is not decoration.

## Who should install this

Install it if you want the newest Android on this hardware and you are comfortable with the no-PC method. It also suits you if MiCam and Dolby are things you do not want to give up when you leave the stock software.

Wait if you cannot sit still through a first boot, or if you have never backed up IMEI and NVRAM before. Do that backup once on this phone and the next flash feels completely different.

The flash itself is the easy part. If the driver side is what stopped you last time, the free Rom Flasher tool handles that setup in a couple of clicks. It is free, and the link is in the downloads section.

::faq
Q: Can I install Evolution X 12.1 on the POCO X7 Pro without a PC?
A: Yes. That is the whole point of the no-PC route. The tool runs from the phone, pushes your phone into fastboot itself, and handles the required files for you, so there is no Termux and no command line.

Q: Do I really need an IMEI and NVRAM backup before flashing?
A: Yes, do it before you flash, not after. A bad flash that damages the IMEI data leaves you without a working network, and that backup is the only practical way back. It takes a few minutes.

Q: Does Evolution X 12.1 wipe my data?
A: Yes. Moving to a custom ROM means a clean start, so back up your photos and chats first. You get the setup wizard on first boot once the flash finishes.

Q: Is this Evolution X build official?
A: No, it is marked unofficial, built for rodin by @orubensgoncalves. Unofficial means the developer maintains it directly, so read their notes before you start.

Q: What does the ROM run on underneath?
A: It is Android 17 on the HyperOS 3.0.301.0 base, with Yuki Kernel 6.6.142. SELinux is enforcing and it is a user build, with MiCam and Dolby both included.
