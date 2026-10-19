::summary
MURI UI is a Realme UI 7 port on an Android 16 base for the POCO X7 Pro, flashed from Fastboot with the installer inside the package. It is a beta with real bugs: NFC, fingerprint, face unlock, double-tap to wake and the performance manager HAL are all affected. Install it for the different interface, not as a daily driver.

::body
MURI UI on the POCO X7 Pro. It is Realme UI 7 ported onto an Android 16 base, and it is a beta. I want the bugs in front of you before the install steps, not buried under them, because that ordering is the honest one.

If you lean on NFC for payments, or you unlock your phone with your fingerprint dozens of times a day, this build is not for you right now. That is not a knock. It is a port, and ports carry the list below.

## What it looks like

MURI UI is a Realme interface running on POCO hardware, ported from a Realme device. That is the whole appeal. The layout, the animations, the way the settings are organised — none of it is HyperOS. If you have used a Realme phone and missed it, this is why you would flash this.

It is genuinely different, and it is running on hardware it was not built for. That is the trade.

## What is broken

Straight from the build's own known-bugs list:

- **NFC**
- **Fingerprint**
- **Face Unlock**
- **Double-tap to wake**
- **Performance Manager HAL**

Read that list once more and decide if any of them is something you use every day. Fingerprint and NFC are the two that catch most people.

## What you need

- The **POCO X7 Pro (Rodin)** with an **unlocked bootloader**.
- The **MURI UI ROM package for Rodin**, from the links on this page.
- A **PC with working ADB and Fastboot**.
- A **full backup**, because the installer wipes data.
- The extras ready: the Kaorios module fix, an AOSP camera and a recommended GCam.

That last point matters. The camera situation on a port is not the same as stock, so have the extra camera app downloaded before you flash, not after.

## Step 1 — reboot to Fastboot

Power off the phone and boot it into **Fastboot** mode. Connect it to the PC.

## Step 2 — confirm the PC sees it

Check the device is detected before you run anything. If the PC cannot see it, the driver is the problem, and the installer will fail on line one.

## Step 3 — extract the package and run the installer

Extract the MURI UI ROM package on the PC. There is an installer inside it — run that from within the extracted folder so it can find the images it needs.

## Step 4 — decide on root

The package brings **KernelSU Next** support. During setup you get the option. Take it if you want root, skip it if you do not. Either way, the flash proceeds.

## Step 5 — wait for the flash, then the first boot

Let the installer finish and wait for the first boot. First boot on a port is slow. Do not start tapping things to wake it up.

## Step 6 — add the extras

Once you are booted, bring in the extras from the links below:

- The **Kaorios module fix**, which handles the integrity side.
- An **AOSP camera** and a **recommended GCam**, since the stock camera experience does not carry over cleanly on a port.

Sort the integrity fix before you install banking apps. They will not open otherwise, and that is not a bug you can chase your way out of.

## Who should install it

Install MURI UI if you are curious, you have a backup phone, and you want to see a Realme interface on POCO hardware. You will enjoy it.

Do not install it if NFC payments or fingerprint unlock are part of your day, or if this is the only phone you have. Wait for a build that clears those bugs.

## Where people get stuck

- **Chasing NFC or fingerprint problems.** They are known bugs on this build. Reporting them as new does not move anything forward.
- **Expecting banking apps to work immediately.** Only basic integrity passes here, so the module fix is what gets you further.
- **Forgetting it is a beta** and treating normal port behaviour as a fresh discovery.

## The honest bit

This is a beta port with bugs, and the developer is credited on the build. If something is broken, check the known list before assuming you did the flash wrong. The install is quick — Fastboot, detect, extract, run the installer — and the interesting part is the interface you get on the other side.

If the driver setup is what usually stalls you, the free Rom Flasher tool puts the ADB and fastboot driver install into a couple of clicks. It is free, and the link sits in the downloads section.

::faq
Q: Does fingerprint work on MURI UI?
A: No. Fingerprint is on the known-bugs list for this beta, along with face unlock, NFC, double-tap to wake and the performance manager HAL. If you rely on fingerprint unlock daily, this is not your daily driver yet.

Q: Is MURI UI stable enough for everyday use?
A: It is a beta port, so treat it that way. The interface works and it is genuinely different, but the listed bugs are real. Use a spare phone or accept the missing features if you flash it.

Q: Will flashing MURI UI wipe my data?
A: Yes. The installer wipes data, so back up everything you care about before you begin and expect the setup wizard on first boot.

Q: Why do my banking apps not open after flashing MURI UI?
A: Only basic integrity passes on this build, so apps that check certification will refuse to run until you apply the module fix. Install the integrity fix before you set up banking apps.

Q: Do I need root to install MURI UI?
A: No. The package includes KernelSU Next support and offers the choice during setup. You can take the root option or skip it, and the flash continues either way.
