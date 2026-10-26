/**
 * Rom Flasher — Motion Graphics & Interactive Hardware Deck Engine
 * Pure vanilla JavaScript: 60 FPS Canvas Constellation, 3D Perspective Tilt,
 * Live Fastboot Terminal Simulator, and Cyberpunk Web Audio Feedback.
 * (C) Rohit Verma (@Rom_Flasher) — romflasher.in
 */

(function () {
  'use strict';

  /* ==========================================================================
     1. Cyberpunk Canvas Constellation Physics (#hero-matrix-canvas)
     ========================================================================== */
  function initHeroCanvas() {
    var canvas = document.getElementById('global-matrix-canvas') || document.getElementById('hero-matrix-canvas');
    if (!canvas) return;

    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var width = (canvas.width = window.innerWidth);
    var height = (canvas.height = window.innerHeight);

    var particles = [];
    var isMobile = window.innerWidth < 768;
    var count = isMobile ? 32 : 68;
    var maxDist = isMobile ? 85 : 120;
    var mouse = { x: -9999, y: -9999, radius: 150 };

    function Particle() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.65;
      this.vy = (Math.random() - 0.5) * 0.65;
      this.radius = Math.random() * 1.6 + 1.1;
      this.color = Math.random() > 0.6 ? '#5ac8fa' : (Math.random() > 0.5 ? '#bf5af2' : '#ff2d9b');
      this.alpha = Math.random() * 0.45 + 0.35;
    }

    Particle.prototype.update = function () {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > width) this.vx = -this.vx;
      if (this.y < 0 || this.y > height) this.vy = -this.vy;

      // Mouse gentle repulsion
      var dx = mouse.x - this.x;
      var dy = mouse.y - this.y;
      var dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < mouse.radius) {
        var angle = Math.atan2(dy, dx);
        var force = (mouse.radius - dist) / mouse.radius;
        this.x -= Math.cos(angle) * force * 2.2;
        this.y -= Math.sin(angle) * force * 2.2;
      }
    };

    Particle.prototype.draw = function () {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.globalAlpha = this.alpha;
      ctx.shadowBlur = 6;
      ctx.shadowColor = this.color;
      ctx.fill();
      ctx.shadowBlur = 0;
    };

    for (var i = 0; i < count; i++) {
      particles.push(new Particle());
    }

    function onResize() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', onResize, { passive: true });

    // Track mouse & touch on entire viewport for all pages
    window.addEventListener('mousemove', function (e) {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    }, { passive: true });

    window.addEventListener('touchmove', function (e) {
      if (e.touches && e.touches[0]) {
        mouse.x = e.touches[0].clientX;
        mouse.y = e.touches[0].clientY;
      }
    }, { passive: true });

    window.addEventListener('mouseleave', function () {
      mouse.x = -9999;
      mouse.y = -9999;
    });

    var animId = null;
    function render() {
      if (document.hidden) {
        animId = requestAnimationFrame(render);
        return;
      }
      ctx.clearRect(0, 0, width, height);

      // Connect particles
      for (var i = 0; i < particles.length; i++) {
        var p1 = particles[i];
        p1.update();
        p1.draw();

        for (var j = i + 1; j < particles.length; j++) {
          var p2 = particles[j];
          var dx = p1.x - p2.x;
          var dy = p1.y - p2.y;
          var dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < maxDist) {
            var alpha = (1 - dist / maxDist) * 0.22;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = '#6c63ff';
            ctx.globalAlpha = alpha;
            ctx.lineWidth = 0.85;
            ctx.stroke();
          }
        }

        // Draw laser connector to mouse across the whole page
        var mdx = mouse.x - p1.x;
        var mdy = mouse.y - p1.y;
        var mDist = Math.sqrt(mdx * mdx + mdy * mdy);
        if (mDist < mouse.radius) {
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = '#5ac8fa';
          ctx.globalAlpha = (1 - mDist / mouse.radius) * 0.45;
          ctx.lineWidth = 1.0;
          ctx.stroke();
        }
      }
      ctx.globalAlpha = 1;
      animId = requestAnimationFrame(render);
    }
    render();
  }

  /* ==========================================================================
     2. Cyberpunk Web Audio FX (Synthesized, Zero MP3 Dependency)
     ========================================================================== */
  var audioCtx = null;
  var soundEnabled = false;

  function initAudio() {
    try {
      soundEnabled = localStorage.getItem('rf_sound') === '1';
    } catch (e) {
      soundEnabled = false;
    }
    updateAudioBtn();
  }

  function getAudioCtx() {
    if (!audioCtx) {
      var AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function playUiClick(freq, type) {
    if (!soundEnabled) return;
    var ctx = getAudioCtx();
    if (!ctx) return;
    try {
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.type = type || 'sine';
      osc.frequency.setValueAtTime(freq || 880, ctx.currentTime);
      gain.gain.setValueAtTime(0.04, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.05);
    } catch (e) {}
  }

  function playSuccessChord() {
    if (!soundEnabled) return;
    var ctx = getAudioCtx();
    if (!ctx) return;
    try {
      var freqs = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
      freqs.forEach(function (f, i) {
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(f, ctx.currentTime + i * 0.04);
        gain.gain.setValueAtTime(0.05, ctx.currentTime + i * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + i * 0.04 + 0.35);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + i * 0.04);
        osc.stop(ctx.currentTime + i * 0.04 + 0.35);
      });
    } catch (e) {}
  }

  function toggleAudio() {
    soundEnabled = !soundEnabled;
    try {
      localStorage.setItem('rf_sound', soundEnabled ? '1' : '0');
    } catch (e) {}
    updateAudioBtn();
    if (soundEnabled) {
      playUiClick(1046, 'sine');
    }
  }

  function updateAudioBtn() {
    var btns = document.querySelectorAll('.sound-toggle-btn');
    btns.forEach(function (btn) {
      if (soundEnabled) {
        btn.classList.add('sound-on');
        btn.setAttribute('aria-label', 'Sound FX: ON (Click to mute)');
        btn.innerHTML = '<span class="s-icon">🔊</span><span class="s-text">SFX: ON</span>';
      } else {
        btn.classList.remove('sound-on');
        btn.setAttribute('aria-label', 'Sound FX: OFF (Click to unmute)');
        btn.innerHTML = '<span class="s-icon">🔇</span><span class="s-text">SFX: OFF</span>';
      }
    });
  }

  /* ==========================================================================
     3. Live Interactive Flashing Terminal Simulator
     ========================================================================== */
  var terminalPresets = {
    'auto-flasher': {
      title: '⚡ 1-Click Auto Flasher (OTG Protocol)',
      badge: 'ACTIVE FLASHING',
      targetDevice: 'POCO X7 Pro (komodo)',
      bootloader: 'UNLOCKED (Tamper: 0)',
      bridge: 'USB 3.2 OTG Direct Bridge',
      keybox: '3/3 TEE Hardware Keybox Active',
      speed: '482.4 MB/s',
      eta: '14.2s',
      progressMax: 100,
      logs: [
        { tag: 'FASTBOOT', cls: 't-cyan', text: 'Handshake accepted with target device [komodo:18d1:4ee0]' },
        { tag: 'PROTOCOL', cls: 't-violet', text: 'Direct Phone-to-Phone OTG streaming initialized (Zero PC / Zero Termux)' },
        { tag: 'SECURITY', cls: 't-green', text: 'Bootloader verified: UNLOCKED | AVB2.0 State: ORANGE' },
        { tag: 'PARSER', cls: 't-yellow', text: 'Payload unpacked: Super.img [4,294,967,296 bytes]' },
        { tag: 'CHUNKER', cls: 't-pink', text: 'Splitting dynamic sparse payload into 512MB chunks for memory safety' },
        { tag: 'FLASH', cls: 't-cyan', text: 'Streaming super_chunk_01.img -> /dev/block/by-name/super [OK 1.2s]' },
        { tag: 'FLASH', cls: 't-cyan', text: 'Streaming super_chunk_02.img -> /dev/block/by-name/super [OK 1.1s]' },
        { tag: 'PATCH', cls: 't-violet', text: 'Injecting dynamic slot-switch payload: target_slot -> slot_b' },
        { tag: 'SUCCESS', cls: 't-green', text: '100% COMPLETE! ROM Flashed in 14.2s without PC. Rebooting target...' }
      ]
    },
    'play-integrity': {
      title: '🛡️ Play Integrity 3/3 Strong Pass (TEE Keybox)',
      badge: 'TEE HARDWARE VALIDATED',
      targetDevice: 'Xiaomi 14 Ultra (aurora)',
      bootloader: 'UNLOCKED | TrickyStore OSS',
      bridge: 'Direct OTG Injection',
      keybox: 'CN=Key Attestation CA1 (UNBANNED TEE)',
      speed: 'Direct Keystore Patch',
      eta: '4.8s',
      progressMax: 100,
      logs: [
        { tag: 'TEE_CHECK', cls: 't-yellow', text: 'Scanning Google Hardware Keystore CRL revocation feed...' },
        { tag: 'KEYBOX', cls: 't-green', text: 'Loaded unbanned TEE Hardware Keybox: Subject: CN=Key Attestation CA1' },
        { tag: 'STATUS', cls: 't-cyan', text: 'Google CRL Check: 4/4 Certificates UNREVOKED & ACTIVE' },
        { tag: 'TRICKY', cls: 't-violet', text: 'Configuring target.txt spoof profile -> Pixel 9 Pro XL (komodo/2026-10-05)' },
        { tag: 'INJECT', cls: 't-pink', text: 'Injecting keybox.xml into /data/adb/tricky_store/ with chmod 600' },
        { tag: 'VERIFY', cls: 't-green', text: 'Running DroidGuard attestation test...' },
        { tag: 'RESULT', cls: 't-green', text: 'BASIC_INTEGRITY: PASS [✓]' },
        { tag: 'RESULT', cls: 't-green', text: 'DEVICE_INTEGRITY: PASS [✓]' },
        { tag: 'SUCCESS', cls: 't-green', text: 'STRONG_INTEGRITY: PASS [✓] (Full Banking & UPI Active)' }
      ]
    },
    'hyperos': {
      title: '🔥 HyperOS Fastboot & Unbrick Recovery',
      badge: 'RECOVERY BYPASS',
      targetDevice: 'Redmi Note 13 Pro+ (zircon)',
      bootloader: 'UNLOCKED (HyperOS 2.0)',
      bridge: 'Fastbootd Over USB-OTG',
      keybox: 'Pre-Root Magisk/KSU Ready',
      speed: '430.8 MB/s',
      eta: '18.6s',
      progressMax: 100,
      logs: [
        { tag: 'BOOT_STATE', cls: 't-yellow', text: 'Target detected in FASTBOOTD mode [Dimensity 7200 Ultra]' },
        { tag: 'ANTI_RB', cls: 't-violet', text: 'Checking anti-rollback version: Index 1 matched' },
        { tag: 'WIPE_MET', cls: 't-pink', text: 'fastboot erase metadata -> SUCCESS' },
        { tag: 'FLASH_BOOT', cls: 't-cyan', text: 'Flashing boot.img [GKI 5.10 with KernelSU Next hooks] -> [OK]' },
        { tag: 'FLASH_VEND', cls: 't-cyan', text: 'Flashing vendor_boot.img -> [OK 2.1s]' },
        { tag: 'SPARSE', cls: 't-violet', text: 'Auto-flashing multi-part product, system and cust images...' },
        { tag: 'POST_HOOK', cls: 't-yellow', text: 'Executing auto-disable dm-verity and verification flags' },
        { tag: 'SUCCESS', cls: 't-green', text: 'Unbrick payload verified! HyperOS 2.0 cleanly installed.' }
      ]
    },
    'otg-direct': {
      title: '📱 Phone-to-Phone OTG Protocol',
      badge: 'STANDALONE WIRELESS/OTG',
      targetDevice: 'OnePlus 12 (waffle)',
      bootloader: 'UNLOCKED',
      bridge: 'Host Controller Direct IO',
      keybox: 'Hardware Keystore Pass',
      speed: '512.0 MB/s',
      eta: '8.4s',
      progressMax: 100,
      logs: [
        { tag: 'USB_HOST', cls: 't-cyan', text: 'Android Host mode engaged: VID=0x18d1, PID=0x4ee0' },
        { tag: 'PERMISSION', cls: 't-green', text: 'Direct USB endpoint access granted by Android OS' },
        { tag: 'NO_PC', cls: 't-yellow', text: 'Running 100% on-device native C++ libusb binaries' },
        { tag: 'ZERO_TERM', cls: 't-pink', text: 'No Termux scripts, no manual command typing required' },
        { tag: 'STREAM', cls: 't-violet', text: 'Direct memory buffer streaming at zero copy overhead' },
        { tag: 'SUCCESS', cls: 't-green', text: 'Host <-> Target handshake fully synced. Ready for 1-Tap Flash!' }
      ]
    }
  };

  function initTerminalSimulator() {
    var deck = document.getElementById('flasher-cockpit');
    if (!deck) return;

    var logContainer = deck.querySelector('.cockpit-logs');
    var progressBar = deck.querySelector('.cockpit-progress-fill');
    var progressText = deck.querySelector('.cockpit-progress-text');
    var speedText = deck.querySelector('.cockpit-speed-val');
    var tabs = deck.querySelectorAll('.cockpit-tab');
    var runBtn = deck.querySelector('.cockpit-run-btn');

    // Telemetry display fields
    var devField = deck.querySelector('.telemetry-dev');
    var blField = deck.querySelector('.telemetry-bl');
    var bridgeField = deck.querySelector('.telemetry-bridge');
    var keyboxField = deck.querySelector('.telemetry-keybox');

    var currentPreset = 'auto-flasher';
    var isSimulating = false;
    var timerId = null;

    function renderPreset(presetKey, animate) {
      var preset = terminalPresets[presetKey];
      if (!preset) return;
      currentPreset = presetKey;

      tabs.forEach(function (t) {
        t.classList.toggle('active', t.getAttribute('data-preset') === presetKey);
      });

      if (devField) devField.textContent = preset.targetDevice;
      if (blField) blField.textContent = preset.bootloader;
      if (bridgeField) bridgeField.textContent = preset.bridge;
      if (keyboxField) keyboxField.textContent = preset.keybox;
      if (speedText) speedText.textContent = preset.speed;

      if (timerId) clearTimeout(timerId);

      if (!animate) {
        // Quick static render
        logContainer.innerHTML = '';
        preset.logs.forEach(function (item) {
          var line = document.createElement('div');
          line.className = 'log-line';
          line.innerHTML = '<span class="log-time">' + getTimestamp() + '</span> ' +
            '<span class="log-tag ' + item.cls + '">[' + item.tag + ']</span> ' +
            '<span class="log-text">' + item.text + '</span>';
          logContainer.appendChild(line);
        });
        if (progressBar) progressBar.style.width = '100%';
        if (progressText) progressText.textContent = '100% COMPLETED';
        return;
      }

      // Animated live simulation
      isSimulating = true;
      if (runBtn) runBtn.disabled = true;
      logContainer.innerHTML = '';
      if (progressBar) progressBar.style.width = '0%';
      if (progressText) progressText.textContent = '0% INITIALIZING...';

      var index = 0;
      function nextLine() {
        if (index >= preset.logs.length) {
          isSimulating = false;
          if (runBtn) runBtn.disabled = false;
          if (progressBar) progressBar.style.width = '100%';
          if (progressText) progressText.textContent = '100% COMPLETE (' + preset.eta + ')';
          playSuccessChord();
          return;
        }

        var item = preset.logs[index];
        var line = document.createElement('div');
        line.className = 'log-line log-enter';
        line.innerHTML = '<span class="log-time">' + getTimestamp() + '</span> ' +
          '<span class="log-tag ' + item.cls + '">[' + item.tag + ']</span> ' +
          '<span class="log-text">' + item.text + '</span>';
        logContainer.appendChild(line);
        logContainer.scrollTop = logContainer.scrollHeight;

        playUiClick(700 + index * 60, 'sine');

        var pct = Math.min(100, Math.round(((index + 1) / preset.logs.length) * 100));
        if (progressBar) progressBar.style.width = pct + '%';
        if (progressText) progressText.textContent = pct + '% STREAMING...';

        index++;
        var delay = 220 + Math.random() * 260;
        timerId = setTimeout(nextLine, delay);
      }
      nextLine();
    }

    function getTimestamp() {
      var d = new Date();
      var pad = function (n) { return (n < 10 ? '0' : '') + n; };
      return pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
    }

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var p = this.getAttribute('data-preset');
        playUiClick(950, 'triangle');
        renderPreset(p, true);
      });
    });

    if (runBtn) {
      runBtn.addEventListener('click', function () {
        playUiClick(1100, 'triangle');
        renderPreset(currentPreset, true);
      });
    }

    // Initial render
    renderPreset('auto-flasher', false);
  }

  /* ==========================================================================
     4. 3D Perspective Physics Tilt + Dynamic Cursor Spotlight (Linear/Raycast)
     ========================================================================== */
  function init3DTilt() {
    try {
      if (window.matchMedia('(hover:none)').matches ||
          window.matchMedia('(pointer:coarse)').matches) return;
    } catch (e) {}

    var cards = document.querySelectorAll('.bento-card, .card, .deck-card, .creator-card');

    cards.forEach(function (card) {
      // Add spotlight element inside card if missing
      if (!card.querySelector('.card-spotlight')) {
        var spot = document.createElement('div');
        spot.className = 'card-spotlight';
        card.appendChild(spot);
      }

      var rect = null;
      var rafId = null;

      card.addEventListener('mouseenter', function () {
        rect = card.getBoundingClientRect();
      });

      card.addEventListener('mousemove', function (e) {
        if (!rect) rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;

        // Position spotlight
        var spot = card.querySelector('.card-spotlight');
        if (spot) {
          spot.style.opacity = '1';
          spot.style.left = x + 'px';
          spot.style.top = y + 'px';
        }

        if (rafId) cancelAnimationFrame(rafId);
        rafId = requestAnimationFrame(function () {
          var halfW = rect.width / 2;
          var halfH = rect.height / 2;
          var rotateY = ((x - halfW) / halfW) * 7.5;
          var rotateX = -((y - halfH) / halfH) * 7.5;

          card.style.transform = 'perspective(900px) rotateX(' + rotateX.toFixed(2) + 'deg) rotateY(' + rotateY.toFixed(2) + 'deg) translateZ(6px)';
        });
      });

      card.addEventListener('mouseleave', function () {
        if (rafId) cancelAnimationFrame(rafId);
        card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        var spot = card.querySelector('.card-spotlight');
        if (spot) spot.style.opacity = '0';
        rect = null;
      });
    });
  }

  /* ==========================================================================
     5. Scroll Reveal Micro-Animations (IntersectionObserver)
     ========================================================================== */
  function initScrollReveal() {
    if (!('IntersectionObserver' in window)) return;

    var elements = document.querySelectorAll('.reveal-on-scroll, .bento-card, .card, .creator-deck');
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    elements.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ==========================================================================
     6. DOM Ready Orchestrator
     ========================================================================== */
  function boot() {
    initAudio();
    initHeroCanvas();
    initTerminalSimulator();
    init3DTilt();
    initScrollReveal();

    // Bind audio toggle buttons
    document.querySelectorAll('.sound-toggle-btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        toggleAudio();
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
