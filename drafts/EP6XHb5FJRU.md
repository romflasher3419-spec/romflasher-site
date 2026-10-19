::summary
MiTool is a Termux tool that flashes a fastboot ROM to a Xiaomi or POCO phone from a second Android device, so no PC and no Mi Flash are needed. One phone runs Termux and MiTool, the other is the phone being flashed, and an OTG cable links them.

::body
Sometimes there is no laptop. You are on a trip, or at a friend's place, or your only machine is an old one that will not run the flashing software. That is the situation this exists for.

MiTool runs inside Termux on one Android phone. The other phone — the Xiaomi or POCO you want to flash — sits at the end of an OTG cable. The phone running Termux does the work that a PC would normally do.

It is command-line. If you have never opened Termux, that is the part to be honest with yourself about. Follow the steps slowly and it works.

## What MiTool can and cannot do

It handles a real set of jobs: unlocking the bootloader, flashing fastboot ROMs, flashing recovery ROMs, and a few bypass-type tasks that show up in the menu.

It cannot do one important thing. **It cannot skip Xiaomi's bootloader unlock wait.** If your phone has never been unlocked, you still go through the Mi Community request and the account aging period. Nothing on the command line shortens that.

It also needs a second Android device. There is no single-phone rescue here, because the phone you are flashing cannot run the tool that is flashing it.

## What you need

- A second Android phone to run Termux on. It needs decent free storage, because ROM packages are large.
- Termux installed, plus the Termux API package.
- An OTG cable that fits both phones.
- USB debugging switched on, on the phone that will be flashed.
- The ROM files downloaded onto the phone that runs MiTool, not the target.

## Step 1 — install Termux and give it storage access

Install Termux from the link in the downloads section, then the Termux API package next to it. Both are needed — the scripts call into the API for parts of their work.

Open Termux and run the storage setup command once. It asks for permission and creates the shortcuts into your phone's storage. Without it the tool cannot see the ROM you downloaded, and you will spend a while wondering why it says the file is missing.

## Step 2 — run the install script

MiTool installs with a single command that pulls the script directly from its repository and runs it. It is listed in the downloads section below. Paste it into Termux and let it run to the end.

This is the part that keeps itself current. The script fetches the latest package when it runs, so you are not chasing an APK that stopped being updated months ago.

When it finishes, type `mitool` and the menu opens.

## Step 3 — set up the cable and the connection

This is where people lose twenty minutes, so read it before you plug anything in.

Turn on **USB debugging** on the target phone first. Go to Settings, About phone, tap the build number until Developer options unlocks, then find USB debugging inside Developer options and switch it on.

Now use the OTG cable to connect the phone running Termux to the target phone. The Termux phone is the host, the target is the device. The tool needs to see the target as a connected device before any flashing starts.

If the tool reports nothing connected, the order is usually to blame: unplug, check USB debugging is really on, and reconnect.

## Step 4 — flash from the menu

Open the menu with `mitool` and pick the job you want. For a fastboot flash you select the ROM package you already downloaded onto the Termux phone and let the tool push the images across to the target.

Watch the output. A full fastboot flash writes a long list of partitions and some of them take a while. Do not unplug the cable, and do not touch the target phone. When it is done the phone reboots on its own.

## Where people get stuck

- **Termux cannot see the ROM file.** The storage setup command never ran, so Termux has no access to your folders. Run it once and it stays fixed.
- **Nothing is detected on the cable.** USB debugging is off on the target, or the OTG cable is the wrong direction. Check both before blaming the tool.
- **The ROM is on the wrong phone.** The package lives on the device running MiTool. Download it there, not on the phone being flashed.
- **Expecting the unlock wait to disappear.** It does not. A locked bootloader still goes through the normal request and waiting period.

## One honest paragraph

Two phones, a cable, and a command line is genuinely more fiddly than sitting at a PC with a mouse. If you have a working computer, use it — this is for the times you do not.

What it buys you is real, though. A phone with a broken screen that still boots to fastboot, or a rescue when you are nowhere near your own machine, is exactly the case this solves. The install staying on the latest version by itself is the part I appreciate most.

Keep the target phone charged before you start. A flash that dies at seventy percent because the battery ran out is a much longer evening than anything the tool itself will do to you.

::faq
Q: Do I really not need a PC to flash a fastboot ROM?
A: Correct, with MiTool you do not. A second Android phone running Termux replaces the PC, and the two phones talk over an OTG cable. You still need that second device though.

Q: What cable do I need for MiTool?
A: An OTG cable between the two phones. The Termux phone is the host and the phone being flashed is the device, so the connection has to be the host-to-device kind.

Q: Does MiTool work on any Xiaomi or POCO phone?
A: It is built as a general Xiaomi and POCO tool, so most models are covered. Check the menu after install for the options that apply to your exact model before you start flashing.

Q: Can MiTool skip the 7 day bootloader unlock wait?
A: No. It can walk you through unlocking, but Xiaomi's waiting period still applies and nothing shortens it. If your bootloader is already unlocked you skip that part entirely.

Q: Where should the ROM file be stored?
A: On the phone running Termux and MiTool, not on the phone you are flashing. The tool reads the package from its own storage and pushes the images across the cable.
