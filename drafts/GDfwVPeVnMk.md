::summary
You can strip the extra apps off any Xiaomi or POCO phone without root and without touching the bootloader. The debloater removes preinstalled MIUI and Google apps over USB debugging, keeps the basics you actually use, and has a reinstall mode that puts everything back if you go too far.

::body
Stock MIUI and HyperOS arrive loaded. You know the feeling — two screens of app icons and you open maybe eight of them. The rest sit there, using space, running in the background and asking for updates.

You can clear that out in one pass. No root, no custom recovery, no bootloader unlock. Just USB debugging and one run of the debloater.

The reason I keep this tool around is not actually the removal. It is the second mode, which puts every single removed app back. That changes the whole thing from a risk into an experiment.

## What it removes and what it keeps

One pass on my phone emptied the drawer down to the things I genuinely use: **File Manager, Calculator, Calendar, Messaging**. Everything else went — the Mi apps, the theme store, the preinstalled Google apps like Google TV, Google One, Meet, YouTube, and the third-party ones that ship on these builds such as LinkedIn, Snapchat and WPS Office.

You do not get to pick every single item by hand in the default flow. The tool works from a list of packages that are safe to remove, which is exactly why it does not break your phone halfway through.

If you want something back, you install it from the Play Store like any other app. That is simpler than trying to restore one specific package.

## What it does not do

- It does not root your phone.
- It never touches the bootloader. This works on a locked phone.
- It only handles packages that can be removed safely. It will not offer to delete something the system needs.
- It will not make a phone that needs a factory reset feel fast again. Removing apps is not a repair.

## What you need

- A PC with the ADB and fastboot tool, or Termux if you do not have a PC.
- The ADB and fastboot driver installed, so the PC can see the phone.
- USB debugging switched on, on the phone.
- The debloat file from the downloads section.

## Step 1 — turn on Developer options

On the phone, go to **Settings**, then **About phone**, and tap the build number repeatedly. After several taps it tells you that you are now a developer. That unlocks the hidden menu.

On HyperOS the wording moves around a little between builds, but it is still About phone and the build number, or the MIUI version entry depending on your version. Keep tapping the same item.

## Step 2 — switch on USB debugging

Go back to Settings, then **Additional settings** or **System**, and open **Developer options**. Find **USB debugging** and turn it on.

Plug the phone into the PC. The phone shows a prompt asking you to allow debugging from this computer. Tick the box that remembers the choice and accept. If you dismiss that prompt by accident, unplug and plug back in to get it again.

## Step 3 — prepare the tool on the PC

Extract the debloat file somewhere you can find it. Keep the ADB and fastboot tool in the same place the script expects, so the commands it runs are found.

The free Rom Flasher tool bundles the ADB and fastboot driver install into a couple of clicks, which saves you hunting through Device Manager for a phone that Windows has decided is an unknown device. It is free, and the link is in the downloads section.

## Step 4 — run it and pick a mode

Open the debloater and choose your mode. **Remove** takes the packages out. **Reinstall** puts back everything a previous run removed.

Let it run to the end. It prints each package as it goes, and the whole thing takes a couple of minutes, not the twenty you might expect.

## Step 5 — check the phone

Reboot the phone when it finishes. Open the app drawer and look at what is left. On my phone it was down to the basics — a much shorter list, and nothing that matters missing.

Open a few things that used to sit next to the removed apps to make sure they still launch. Contacts, Messages, the camera, the settings menus.

## No PC? Use Termux

If you do not have a computer to hand, the same job runs from Termux on the phone itself, and there is a Termux flash file in the downloads section for that route.

The steps are the same idea, just run on the device. USB debugging is not involved in that mode because there is no cable, so follow the Termux instructions as written rather than mixing the two sets of steps.

## Where people get stuck

- **The computer prompt was dismissed.** No prompt accepted, no connection. Unplug, plug back in, and accept the debugging prompt properly.
- **USB debugging is on but the driver is missing.** The tool reports no device. Install the driver from the downloads section and try again.
- **Something misbehaves afterwards.** A menu crashes, or a feature that you relied on has quietly stopped working. Run the reinstall mode. Nothing here is permanent.
- **Expecting a speed boost on a tired phone.** If the phone is slow because the storage is full or the system has never been reset, removing apps will not fix that.

## One honest note

This is a genuinely low-risk thing to do, and I say that as someone who flashes ROMs for a living and knows how quickly "low risk" turns into an evening of recovery mode.

The reason it is low risk is the reinstall mode. Every app it takes out, it can put back. So start with the default removal pass, use the phone for a week, and only then decide whether you want to be more selective.

The one thing I would not treat as a toy is a work phone. If your employer's setup depends on a specific app, or a device management profile is installed, leave that phone alone.

::faq
Q: Do I need root to remove bloatware from a Xiaomi phone?
A: No. USB debugging is enough, from a PC or from Termux. The tool never touches the bootloader and does not need the phone unlocked, which means it works on a completely stock device.

Q: Does debloating wipe my data?
A: No. It only removes and reinstalls app packages, so your photos, messages and accounts stay exactly where they are. There is no factory reset involved at any point.

Q: How do I get the removed apps back?
A: Run the reinstall mode on the same file. It puts back everything a previous run removed, from YouTube and Google TV to the theme store and the preinstalled third-party apps.

Q: What if the phone acts strange after debloating?
A: Run the reinstall mode and reboot. Nothing here is permanent, which is the whole point of keeping the second mode around. If a single app matters to you, install it from the Play Store instead.

Q: Can I debloat a HyperOS phone without a PC?
A: Yes. There is a Termux route that runs the same job on the phone itself, with a flash file linked in the downloads section. You skip the cable entirely and follow the Termux steps instead.
