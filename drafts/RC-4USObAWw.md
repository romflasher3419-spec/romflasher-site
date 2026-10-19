::summary
Robinhood HyperOS 3 is a China-based Android 16 build for the Poco X7 Pro, and you flash it with a fastboot installer instead of recovery. Unpack the ROM on your PC, boot the phone into fastboot, run the installer batch file, answer Y for a clean flash, and pick your root option. It is a short job, and the only real trap is running it from inside the zip.

::body
You have heard about the China-based HyperOS 3 builds and you want to try one on your Poco X7 Pro. Here is the good news first: this one flashes through fastboot, so there is no recovery hopping and no long list of commands to type. You run one script, answer a few prompts, and wait.

Here is the honest part too. Robinhood HyperOS 3 is built on a China base. That means the core system is current and smooth, but the global app lineup is not all there out of the box. You set it up, notice what is missing for your own use, and add the rest yourself. Nothing is broken. It is just a build that assumes you will finish the job.

## What you need before you start

- The Robinhood HyperOS 3 ROM zip, unpacked into a normal folder on your PC.
- The Poco X7 Pro with an unlocked bootloader, ready to enter fastboot.
- Working ADB and fastboot drivers on Windows, so the script can see the phone.
- A full backup, because the installer's clean flash wipes everything.
- A cable you trust and a battery above 50%.

That last point sounds like a joke. It is not. Almost every "the flash ruined my phone" story is really a cable that dropped halfway through.

## Step 1 — unpack the ROM into a folder

Download the ROM from the link below and extract it with 7-Zip or WinRAR. Not the built-in Windows extractor — that one sometimes flattens the structure. You want a real folder with the installer script and the image files sitting side by side inside it.

If you are looking at the contents of the zip file rather than an extracted folder on disk, stop here. Running the installer from inside the archive is the single most common way this goes wrong.

## Step 2 — boot the phone into fastboot and connect it

Power the phone off. Hold Volume Down and Power together until the fastboot screen appears. Plug it into the PC with your good cable.

Now open a command window in your platform tools folder and run:

`fastboot devices`

You should get a long serial number and the word `fastboot`. No serial number means the driver is missing, and the installer will not find the phone no matter how many times you try. Fix the driver first.

## Step 3 — run the installer

Inside the extracted ROM folder, run `Robinhood_os_installer.bat`. Right-click and run it as administrator so nothing gets blocked halfway.

The script walks you through it:

- It asks whether you want a clean flash. Answer **Y**. That is the intended path for this build.
- It then asks how you want root, with options 1, 2 or 3. Pick whichever suits you.
- If you do not want root at all, press **4** and move on.

That is the whole decision list. There is nothing hidden after it.

## Step 4 — let it finish and keep your hands off the cable

The installer starts writing partitions and printing the names as it goes. Some steps take a while and the screen can look frozen. It is not. Do not unplug the cable, do not close the window, and do not tap the phone to check if it is awake.

When it is done, the phone reboots to the system on its own. You can also tap **S** if you want to send it there yourself. Either way, first boot on a China base takes a few minutes.

## Where people get stuck

- **Running the installer from inside the zip.** It has to run from the extracted folder. If the window opens and dies instantly, this is almost always why.
- **Missing fastboot drivers.** No serial number in `fastboot devices` means the script has nothing to talk to. Sort the driver before you blame the ROM.
- **Pulling the cable because it looked stuck.** A long pause is normal. The flash is still running.

## One honest note about the China base

Set the ROM up first, do a full boot, and finish the setup wizard before you start restoring apps and accounts. That way, if something is missing for you, you find it on a clean phone instead of on top of an hour of restored data. Adding a global service or two by hand is normal on China builds. It is the trade-off you accept, and it is worth knowing before you start.

If the driver side feels like the annoying part, the free Rom Flasher tool bundles the ADB and fastboot driver install into a couple of clicks so you are not digging through Device Manager. It is free, and the link is in the downloads section.

## One small thing that saves time

Keep the ROM folder somewhere easy to find, like a folder in the root of your drive. You will come back to it, and hunting through Downloads for a `Robinhood_os_installer.bat` at 1am is its own kind of bad evening.

::faq
Q: The installer window opens and closes straight away. What is wrong?
A: You are almost certainly running it from inside the zip. Extract the ROM into a real folder with 7-Zip or WinRAR first, then run the installer batch file from that folder as administrator.

Q: Does this flash wipe my data?
A: Yes. The installer's clean flash is the intended path, and it resets the phone completely. Move your photos and anything you care about off before you start, and expect a fresh setup wizard on first boot.

Q: Will this build have all the global apps I use?
A: Not straight out of the box. It is a China-based build, so some global services need adding by hand once you are set up. Set it up first, see what is missing for you, and fill in the gaps.

Q: Do I need to be rooted to use this ROM?
A: No. Root is completely optional here. The installer offers a few root options, and pressing 4 skips root entirely. You can also add it later if you change your mind.

Q: The script looks frozen at one step. Should I unplug the cable?
A: No. Long pauses are normal while a partition is being written. Unplugging mid-flash is how phones get soft-bricked. Leave it plugged in until the phone reboots on its own.
