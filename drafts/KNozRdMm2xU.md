::summary
If Play Store says your device is not certified, you can usually get the integrity verdicts passing again with root and a small set of modules, then a reboot and one action per module. You need KernelSU or Magisk already working. Most first failures come from a skipped reboot or from running the module actions in the wrong order.

::body
You rooted your phone, everything was fine for a while, and then one morning Play Store decides your device is not certified. Or an app refuses to open and tells you it needs a verified device. That is Play Integrity doing its job, and it is exactly what you would expect once the bootloader is unlocked and the system stops looking factory-fresh to Google.

The fix is not mysterious. It is a small number of modules plus a careful order of operations. The order is the part people get wrong, so slow down and follow it properly.

One thing up front: this needs root. KernelSU or Magisk, installed and actually working. Without root nothing can hook into the system, and no module will do anything useful.

## What you need

- Root, already installed. KernelSU or Magisk, whichever your setup uses.
- The module files from the all-files link. There are four of them.
- A reboot's worth of patience, twice.
- A way to check the result, like the integrity checker the modules provide or a Play Integrity API checker app.

## Step 1 - confirm root is really working

Before you touch modules, open KernelSU or Magisk and make sure it granted root to something. If you have not rooted yet, stop here. Modules are the next job, not this one.

Also check that Zygisk is enabled if you are on Magisk. That is the piece that lets modules reach into apps, and with it off half of this will silently do nothing.

## Step 2 - install the four modules, one at a time

Install them in sequence, not all at once. Flash the first, let it finish, then the second, and so on. The four are Integrity Box, Tricky Store, a Zygisk module, and Play Integrity Fix. The exact files are in the all-files link, so use those rather than a version someone posted in a thread from two years ago.

One at a time matters. If you install everything in a single go and something misbehaves, you have no idea which module caused it.

## Step 3 - reboot

Actually reboot. Not "close the app and reopen it". The modules need the system to come up fresh so they can load into the right places. This is the single most common reason a first attempt fails, and it is the easiest thing in the world to skip.

## Step 4 - run each module's action

After the reboot, open KernelSU or Magisk and go to the modules section. Several of these modules have an action button next to them, and that action is not decorative. It runs a command that sets things up.

- In Integrity Box, run the integrity command from the action.
- For Play Integrity Fix, run its action too.
- Confirm the Zygisk module is actually active, not just installed.

Skipping the actions is the second most common reason this fails. A module that is installed but never told to run has done half its job at best.

## Step 5 - check the verdicts

Re-run your integrity checker. You are looking for all three verdicts to come back positive: basic, device and strong. If you are on the checker the modules provide, run the check from inside the app so it reads the same values the modules set.

If one verdict still fails, the usual cause is a missed reboot or an action you did not run. Go back to step 3.

## Step 6 - open Play Store

Open Play Store and give it a moment. It can throw an error on the first launch after all this. If it does, back out of it completely and reopen it, then check the certification status again. In most cases it settles and shows certified.

At this point you can also look at the bootloader state with a key attestation check, which tells you what an app can see about your device's security state.

## Where it goes wrong

- **No root.** Nothing hooks in, nothing changes. Check that first.
- **Skipped reboot.** Module installed, action run, no reboot, no effect.
- **Module actions never run.** Installed is not the same as active.
- **Module versions out of date.** Google changes how integrity is checked, so a fix that worked last year may not work today. Keep the modules current.

## One honest note

This is not a permanent fix. It is a moving target. Google changes the checks, the modules get updated, and you apply the updates. Anyone telling you there is a one-time set-and-forget solution is selling you something that will break in a few months.

That is not a reason to avoid it. It is a reason to know what you are signing up for when you unlock the bootloader and root in the first place. And it works on Android 15 and Android 16 setups, so you are not stuck on an old version to keep it going.

::faq
Q: Do I need root to pass Play Integrity?
A: Yes. The modules need KernelSU or Magisk to hook into the system, so root has to be installed and working first. Without it, installing modules changes nothing.

Q: Which modules do I need for Play Integrity?
A: Four: Integrity Box, Tricky Store, a Zygisk module, and Play Integrity Fix. Install them from the all-files link, one at a time, rather than grabbing versions from random threads.

Q: Why did Play Integrity fail the first time I tried?
A: Usually a skipped reboot between installing the modules and running their actions, or the module actions never being run at all. A module that is installed but not activated does not do its job.

Q: Does this fix survive Android updates?
A: Not permanently. Google changes how integrity is checked, so the modules need updating over time. Treat this as something you maintain, not a one-time fix.

Q: Will this make my device certified on both Android 15 and 16?
A: Yes, the same module set covers both Android 15 and Android 16 setups. The steps are identical, and the only difference is which root manager you are using.
