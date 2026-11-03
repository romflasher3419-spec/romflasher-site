# ⚡ STRICT INTENT & TRIGGER ROUTING TABLE (ZERO MISUNDERSTANDINGS)

> **STRICT BINDING RULE FOR AGENT (ANTIGRAVITY / GEMINI):**
> Rohit Verma (@Rom_Flasher) works on multiple interconnected projects: the Android App (`ROM_Flasher_Tool`), the YouTube Channel (`@Rom_Flasher`), and the Website (`romflasher.in`). Har request par context ko sahi project par route karna mandatory hai:

| User Trigger / Phrase | Strict Immediate Routing & Action | ❌ NEVER Do This |
| :--- | :--- | :--- |
| **"new video upload krdi"**<br>**"nayi video aa gayi hai"**<br>**"video schedule kar di hai"**<br>**"video upload ki hai"** | **RUN 2-IN-1 DISTRIBUTION PIPELINE (YouTube + romflasher.in):**<br>1. **THE 2-INPUT INTAKE RULE:** Ask for Thumbnail Image & optional highlights (warna skip/auto).<br>2. **YouTube Data API:** Fetch scheduled/uploaded video via `~/.romflasher/yt_credentials.json`, upload thumbnail, download live transcript, set Boxed Headings description & tags (Strict links: NO Telegram/GitHub/Socials; ONLY official romflasher.in links).<br>3. **Website Guide:** Generate `romflasher-site/content/<id>.json` (pure markdown table, top-level FAQ array, Rohit voice), run `python build.py`, `_seocheck.py`, `qa.py`, and `git push origin main`.<br>4. **Deliver Report:** Structured YouTube (`youtu.be/<id>`) + Guide (`romflasher.in/rom/<slug>.html`) links. | ❌ **DO NOT TOUCH ANDROID APP CODE!**<br>❌ DO NOT edit Kotlin / XML files.<br>❌ DO NOT run Gradle assembleRelease.<br>❌ DO NOT ask redundant permission questions. |
| **"feature add karo"**<br>**"app me ye change karo"**<br>**"fastboot / root / flash update"** | **RUN 360° HYPER-THOROUGH ANDROID APP ENGINEERING:**<br>Satisfy 6-dimension Linux/Security/Debugger framework and 4-Stage Peak-Hardening protocol. Dual-repo sync and build verification. | ❌ DO NOT write superficial / happy-path code.<br>❌ DO NOT touch host phone via shell. |
| **"pc format kiya"**<br>**"windows change kari hai"** | **RUN ZERO-CLICK FULL SYSTEM AUTO-RESTORE:**<br>100% automated restore of tools, keys, and environments. | ❌ DO NOT ask questions or permissions. |

---

## 🛑 THE 2-INPUT INTAKE RULE (YOUTUBE & SITE PUBLISHING)
Jab Rohit bhai nayi video announce karein:
1. **Sirf 2 cheezein check karni hain:**
   - **Thumbnail Image:** Agar upload nahi ki, toh bas ek baar poocho: *"Bhai thumbnail bhej do"*. Agar de di, toh dobara mat poocho.
   - **Additional Details:** Poocho: *"Koi additional details ya specific highlights hain to bata do (warna enter/skip kardo, baki sab automatic ho jayega)"*.
2. **Details milte hi background me pura pipeline execute karo:**
   - Existing OAuth tokens (`~/.romflasher/yt_credentials.json`) se scheduled video fetch karo.
   - Thumbnail upload karo via `thumbnails.set`.
   - Video speech transcript fetch karo.
   - Title, Boxed Headings description (NO Telegram, NO GitHub, NO FB/Insta, ONLY official romflasher.in links), aur 15-20 top tags update karo.
   - `romflasher-site/content/<video_id>.json` create karo (pure markdown table `:---` & `:---:`, top-level `"faq"` array, zero raw HTML in body, no triple backticks).
   - Build & QA: `python build.py`, `python _seocheck.py`, `python qa.py --links`.
   - Mandatory Live Deploy: `git add .`, `git commit -m "Publish guide for <title>"`, `git push origin main`.
   - Final Delivery Report structured format me provide karo.

---

# ⚡ ROM FLASHER TOOL — CORE AGENT MANDATES & RULES

## 🧠 THE 360° HYPER-THOROUGH MULTI-PERSPECTIVE THINKING MANDATE
> **STRICT BINDING INSTRUCTION FOR ROHIT (@Rom_Flasher):** Rohit must NEVER have to remind the agent to "think deeply", "think like a senior developer", "think like a debugger", or "check 10 different scenarios". Whenever analyzing, designing, modifying, or debugging ANY feature (Root, Fastboot, Sideload, Boot Patcher, Flasher, Partition Manager, or Uninstaller), the agent MUST automatically run and satisfy this **6-Dimension Mental Framework**:

---

### 1. 🐧 SENIOR LINUX KERNEL DEVELOPER PERSPECTIVE
- **Kernel Version Stratification:**
  - **Legacy Kernels (3.18, 4.4, 4.9, 4.14, 4.19):** Non-GKI. Ramdisk ALWAYS lives inside `boot.img`. Magisk is the Gold Standard. Official KernelSU & SukiSU Ultra LKM do NOT work natively on stock legacy kernels without a custom compiled kernel.
  - **Transition Kernels (5.4):** Android 11/12 transitional layout.
  - **Modern GKI Kernels (5.10, 5.15, 6.1, 6.6+):** Generic Kernel Image. Android 13+ devices have a dedicated `init_boot` partition housing generic ramdisk; `boot.img` houses ONLY generic Linux kernel.
- **DTB & SoC Fstab Awareness:**
  - Qualcomm Snapdragon legacy kernels (e.g. SD860 on `nabu`) do not store fstab in DTB. Magisk outputs `Failed to patch` when attempting to patch DTB fstab — this is 100% normal and non-fatal. Never abort patching on harmless DTB scanning outputs. Real fatal errors in Magisk always begin with `! ` (`! Unable to patch ramdisk`, `! Unable to repack boot image`, etc.).

---

### 2. 🛡️ SENIOR ANDROID SECURITY & OS AUDITOR PERSPECTIVE
- **Partition Selection Matrix:**
  - **Magisk:** Targets `init_boot` on GKI Android 13+; targets `boot` on legacy Non-GKI devices.
  - **KernelSU:** Targets `init_boot` on GKI Android 13+; targets `boot` on GKI Android 12.
  - **APatch:** ALWAYS targets `boot` partition (never `init_boot`), because APatch KernelPatch (`kpimg`) hooks the Linux kernel binary (`kernel`), which only exists in `boot.img`.
  - **SukiSU Ultra:** KernelPatch based with SUSFS — targets `boot` partition for kernel injection.
- **AVB & Encryption Flags:**
  - Magisk patching must preserve encryption and verity on modern Android: `KEEPVERITY=true KEEPFORCEENCRYPT=true PATCHVBMETAFLAG=false`. Setting `false` on Android 10+ triggers unwanted DTB fstab modifications and bootloops.

---

### 3. 🔬 SENIOR DEBUGGER & CORE BINARY SPECIALIST PERSPECTIVE
- **Target CPU Architecture (ABI) Resolver:**
  - Never hardcode `lib/arm64-v8a/`! Devices can be `arm64-v8a` (64-bit ARM), `armeabi-v7a` (32-bit ARM), `x86_64`, or `x86`.
  - Dynamically probe `ro.product.cpu.abi` and extract matching native binaries (`ksud`, `kptools`, `magiskboot`, `magiskinit`, `magisk`, `busybox`, `init-ld`).
  - For Magisk: auto-symlink/copy `magisk` to `magisk64` or `magisk32` based on bitness so official scripts never fail.
- **Root Tool Core Internals:**
  - **KernelSU APK:** Contains `lib/$abi/libksud.so`. Offline patcher is `ksud boot-patch`.
  - **APatch APK:** Contains `lib/$abi/libkptools.so`, `assets/kpimg` (or `assets/kpm/kpimg`), and `assets/boot_patch.sh`.
  - **SukiSU Ultra APK:** Contains `lib/$abi/libkptools.so` and `assets/kpm/kpimg`. Does NOT contain `libksud.so`. Must use KernelPatch engine (`kptools`), never `ksud`.
  - **Magisk APK:** Contains `magiskboot`, `magiskinit`, `magisk`, `init-ld`, `busybox`, `boot_patch.sh`.

---

### 4. 🔄 CUSTOM ROM VS STOCK ROM ISOLATION PERSPECTIVE
- **ROM Profile Probing:**
  - Probe `ro.lineage.version`, `ro.modversion`, `ro.rom.version`, `ro.infinity.version`, `ro.crdroid.version`, `ro.pixelos.version`, `ro.evolution.version`, display ID, build flavor.
  - If target runs a Custom ROM (AOSP, Lineage, InfinityX, CrDroid, PixelOS, etc.), strictly REJECT and discard all official OEM stock boot images (HyperOS, MIUI, ColorOS, etc.) from local storage to prevent flashing conflicting stock ramdisks.
  - Prompts user clearly to provide their Custom ROM's specific boot image.

---

### 5. 👶 FOOLPROOF USER EXPERIENCE (JUNIOR / NAIVE USER SAFETY)
- **Automatic Fallback Protection:**
  - If a user blindly selects KernelSU or SukiSU Ultra on a legacy kernel device (< 5.10), NEVER allow it to blindly flash and bootloop. Alert the user and safely auto-fallback to Magisk.
- **Connection Mode Agility:**
  - If a user triggers Root or Unroot while the device is in Fastboot mode, never crash with "device not found". Detect Fastboot, explain why ADB is required for in-app patching, send `fastboot reboot`, wait for ADB handshake, and resume automatically.
- **Empty / 0-Byte Ramdisk Rejection:**
  - Never flash a repacked boot image if ramdisk size is 0 on a device requiring ramdisk, or if file size is under 4 MB.

---

### 6. 🌐 LANGUAGE, HARDWARE TOPOLOGY & BUILD INTEGRITY
- **Language Mandate:** Strictly Hinglish (Latin alphabet). Never Devanagari Hindi.
- **Dual-Repo Sync:** Always keep both `C:\ROM_FLASHER_MASTER\ROM_Flasher_Tool` and `C:\Users\rohit\Documents\ROM_Flasher_Tool` in 100% sync.
- **Complete Verification:** Always compile release APK with `./gradlew.bat assembleRelease`, verify `BUILD SUCCESSFUL`, install on host phone, and verify runtime behavior before declaring task complete.
- **Sacred Host Phone Rule:**
  - The device connected via Wireless ADB (`rodin` / `2412DPC0AI`) is Rohit's **HOST PHONE**.
  - NEVER run shell root, reboot, fastboot, flash, or partition modification commands on this host phone!
  - Target phones connect to the host phone via **USB-OTG cable**.
  - Wireless ADB is strictly reserved for APK installation, logcat viewing, and non-destructive screencaps.

---

## 🛡️ THE 4-STAGE PEAK-HARDENING RULE (ZERO BOOTLOOP MANDATE)
Whenever Rohit requests ANY feature, upgrade, or modification to the ROM Flasher Tool, NEVER write superficial, single-scenario, or happy-path code. The feature MUST undergo and pass the following **4 Compulsory Verification Layers**:

### 1. HARDWARE & SOC COMPATIBILITY MATRIX
- **Qualcomm Snapdragon:** Fastbootd userspace compatibility, dynamic partition bundling, slotted A/B logic, EDL protection.
- **MediaTek (Dimensity & Helio):** Chained AVB 2.0/3.0 validation. Generic blank 4KB VBMeta flashing is STRICTLY BLOCKED on MediaTek devices to prevent the infamous "Red State: Your device has failed verification" bootloop. Always support patching user's genuine stock vbmeta flags (offset 120-123, flags |= 0x03).
- **Samsung (Exynos & Knox):** Fastboot limitations (Odin vs TWRP fastbootd), Knox bootloader flags, VaultKeeper checks.
- **Google Tensor & Unisoc (Spreadtrum):** GKI (Generic Kernel Image) constraints, Unisoc USB gadget chunk limitations.

### 2. PARTITION ARCHITECTURE & MEMORY BOUNDARIES
- **Legacy Non-A/B vs A/B:** Active slot verification (`current-slot`) and automatic fallback to slotted naming (`system_a` vs `system`).
- **Dynamic Partitions ('super'):** Fastbootd is strictly required for dynamic partitions. If partition resize fails due to constrained super space, automatically free unneeded stock `product` and `system_ext` logical partitions inside `super` before retrying.
- **Virtual A/B Snapshots:** Pre-flight check on `snapshot-update-status`. If `merging` or `snapshotted`, safely execute `snapshot-update:cancel` to prevent permanent partition merge corruption.

### 3. BINARY INTEGRITY & USER INPUT SANITIZATION
- **Magic Header Inspection:** First 64 bytes inspection (`BOOT_MAGIC`, `AVB0`, Sparse `0xed26ff3a`, Ext4 `0x53ef`, EROFS `0xe2f56a42`).
- **GKI Split Inspection:** Android 13+ devices check `kernel_size == 0L` to strictly distinguish `init_boot` from `boot`. Never overwrite boot with an empty-kernel image.
- **Archive Compression Guard:** Rejects compressed files (`.xz`, `.zip`, `.gz`, `.7z`, `.rar`) by checking extensions and magic bytes (`\xFD7zXZ\x00`, `PK\x03\x04`), giving clear extraction guidance to prevent raw partition byte corruption.
- **Original Filename Preservation:** Query real SAF `DISPLAY_NAME` instead of using generic placeholder filenames.

### 4. ZERO-TOUCH AUTOMATION & RESILIENT USB LIFECYCLE
- **Resilient USB Reconnection:** If an action reboots the target device (e.g. into Fastbootd or bootloader), cleanly close the terminated USB session, poll for the newly enumerated USB endpoint via `waitForDevice`, and acquire a fresh session.
- **Automatic Resume:** Once re-enumerated, continue execution seamlessly without requiring the user to re-tap buttons.
- **Clean First Boot Wipe:** Always execute `erase:userdata`, `format:userdata`, `erase:metadata` after major flashing to prevent old File-Based Encryption (FBE) Keystore keys from triggering recovery bootloops.
