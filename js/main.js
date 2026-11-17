/**
 * MORE THAN GRADES — Main Application Controller (100% English)
 * Handles Navigation, Video Player, Audio Synthesis, and Interactive Modals
 */

document.addEventListener("DOMContentLoaded", () => {
  initMobileMenu();
  initHeaderScroll();
  initInteractiveVideoPlayer();
  initPromptDrawers();
});

/* 1. Mobile Menu */
function initMobileMenu() {
  const toggleBtn = document.getElementById("mobile-menu-toggle");
  const navMenu = document.querySelector(".main-nav");

  if (!toggleBtn || !navMenu) return;

  toggleBtn.addEventListener("click", () => {
    const isExpanded = navMenu.classList.toggle("mobile-open");
    toggleBtn.setAttribute("aria-expanded", isExpanded);
    toggleBtn.innerHTML = isExpanded ? "✕" : "☰";
    if (isExpanded) {
      navMenu.style.display = "flex";
      navMenu.style.flexDirection = "column";
      navMenu.style.position = "absolute";
      navMenu.style.top = "80px";
      navMenu.style.right = "0";
      navMenu.style.left = "0";
      navMenu.style.background = "#090e1a";
      navMenu.style.padding = "1.5rem";
      navMenu.style.borderBottom = "1px solid rgba(148, 163, 184, 0.2)";
      navMenu.style.gap = "0.75rem";
    } else {
      navMenu.style.display = "";
    }
  });
}

/* 2. Header Scroll Effect */
function initHeaderScroll() {
  const header = document.querySelector(".site-header");
  if (!header) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 40) {
      header.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.6)";
      header.style.background = "rgba(9, 14, 26, 0.96)";
    } else {
      header.style.boxShadow = "none";
      header.style.background = "rgba(9, 14, 26, 0.9)";
    }
  });
}

/* 3. Interactive AI Video Player with Cinematic Canvas & Real Audio */
function initInteractiveVideoPlayer() {
  const canvas = document.getElementById("ai-video-canvas");
  const overlayPlay = document.getElementById("video-overlay-play");
  const playBtn = document.getElementById("btn-video-play");
  const playIcon = document.getElementById("play-icon");
  const progressBar = document.getElementById("video-progress-fill");
  const progressContainer = document.getElementById("video-progress-container");
  const timeDisplay = document.getElementById("video-time-display");
  const subtitleBox = document.getElementById("video-subtitles-text");
  const muteBtn = document.getElementById("btn-video-mute");
  const fullscreenBtn = document.getElementById("btn-video-fullscreen");

  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const totalDuration = 35; // 35 seconds requirement
  let currentTime = 0;
  let isPlaying = false;
  let isMuted = false;
  let animId = null;
  let audioCtx = null;
  let speechSynth = window.speechSynthesis;
  let speechUtterance = null;

  // Cinematic Scenes Data (100% English)
  const scenes = [
    {
      start: 0,
      end: 8,
      title: "Silence of Examination Halls",
      sub: "In schools and universities, we are conditioned to equate our human self-worth with exam numbers...",
      colorA: "#0f172a",
      colorB: "#1e293b",
      particles: "#38bdf8"
    },
    {
      start: 8,
      end: 16,
      title: "Moments No Transcript Measures",
      sub: "A peer reaching out to comfort a struggling friend; a newcomer finding a warm welcoming smile...",
      colorA: "#064e3b",
      colorB: "#022c22",
      particles: "#34d399"
    },
    {
      start: 16,
      end: 25,
      title: "Limitless Creative Passions",
      sub: "From AI coding and robotics to digital illustration and athletics, youth talent shapes the future...",
      colorA: "#7c2d12",
      colorB: "#431407",
      particles: "#fb923c"
    },
    {
      start: 25,
      end: 35,
      title: "Your Grade is Part of You, Not All of You",
      sub: "You are a human being with empathy, dreams, and potential no exam can measure. Be proud of who you are!",
      colorA: "#0f172a",
      colorB: "#047857",
      particles: "#f59e0b"
    }
  ];

  function resizeCanvas() {
    canvas.width = canvas.parentElement.clientWidth || 960;
    canvas.height = Math.round(canvas.width * (9 / 16));
  }
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);

  function initAudioEngine() {
    if (audioCtx) return;
    try {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    } catch (e) {
      console.warn("AudioContext not supported", e);
    }
  }

  function playSoundChord(freq, type = "sine") {
    if (!audioCtx || isMuted) return;
    try {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 3);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 3);
    } catch (e) {}
  }

  // English Vocal Narration
  function startEnglishVoiceover() {
    if (!speechSynth || isMuted) return;
    speechSynth.cancel();

    const fullScript = "Welcome to More Than Grades. In schools and universities, we are often told that test percentages are the only measure of our worth. But the truth is far greater than an exam paper. Behind the desks are courageous acts of kindness, peer solidarity, and creative passions that no GPA can calculate. Always remember: Your grade is part of your journey, not the measure of your worth.";
    speechUtterance = new SpeechSynthesisUtterance(fullScript);
    speechUtterance.lang = "en-US";
    speechUtterance.rate = 0.95;
    speechUtterance.pitch = 1.0;

    const voices = speechSynth.getVoices();
    const enVoice = voices.find(v => v.lang.startsWith("en"));
    if (enVoice) speechUtterance.voice = enVoice;

    speechSynth.speak(speechUtterance);
  }

  function stopEnglishVoiceover() {
    if (speechSynth) speechSynth.cancel();
  }

  // Draw Frame on Canvas
  let particleArray = [];
  for (let i = 0; i < 40; i++) {
    particleArray.push({
      x: Math.random() * 800,
      y: Math.random() * 450,
      r: Math.random() * 3 + 1,
      vx: (Math.random() - 0.5) * 0.8,
      vy: (Math.random() - 0.5) * 0.8
    });
  }

  function drawScene(time) {
    const w = canvas.width;
    const h = canvas.height;
    const curScene = scenes.find(s => time >= s.start && time < s.end) || scenes[scenes.length - 1];

    // Background Gradient
    const bgGrad = ctx.createLinearGradient(0, 0, w, h);
    bgGrad.addColorStop(0, curScene.colorA);
    bgGrad.addColorStop(1, curScene.colorB);
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // Glowing Ambient Orb
    const orbGrad = ctx.createRadialGradient(w / 2, h / 2, 20, w / 2, h / 2, w / 2);
    orbGrad.addColorStop(0, "rgba(52, 211, 153, 0.18)");
    orbGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = orbGrad;
    ctx.fillRect(0, 0, w, h);

    // Dynamic Floating Light Particles
    ctx.fillStyle = curScene.particles;
    particleArray.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;
      ctx.beginPath();
      ctx.arc((p.x / 800) * w, (p.y / 450) * h, p.r, 0, Math.PI * 2);
      ctx.fill();
    });

    // Central Emblem
    ctx.save();
    ctx.translate(w / 2, h * 0.42);

    ctx.beginPath();
    ctx.arc(0, 0, h * 0.22, 0, Math.PI * 2);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.rotate(time * 0.25);
    ctx.beginPath();
    ctx.arc(0, 0, h * 0.24, 0, Math.PI * 0.7);
    ctx.strokeStyle = curScene.particles;
    ctx.lineWidth = 4;
    ctx.stroke();
    ctx.restore();

    // Scene Title
    ctx.fillStyle = "#ffffff";
    ctx.font = `bold ${Math.round(w * 0.034)}px 'Outfit', sans-serif`;
    ctx.textAlign = "center";
    ctx.fillText(curScene.title, w / 2, h * 0.44);

    // AI Badge indicator
    ctx.fillStyle = "rgba(16, 185, 129, 0.9)";
    ctx.font = `600 ${Math.round(w * 0.016)}px 'Inter', sans-serif`;
    ctx.fillText("✦ AI SYNTHESIZED MEDIA • DMD 1203 ✦", w / 2, h * 0.32);

    // Subtitle Text on screen
    if (subtitleBox) {
      subtitleBox.innerText = curScene.sub;
    }
  }

  let lastTimestamp = null;
  function videoLoop(timestamp) {
    if (!lastTimestamp) lastTimestamp = timestamp;
    const delta = (timestamp - lastTimestamp) / 1000;
    lastTimestamp = timestamp;

    if (isPlaying) {
      currentTime += delta;

      if (Math.floor(currentTime) % 8 === 0 && Math.floor(currentTime) !== Math.floor(currentTime - delta)) {
        playSoundChord(220 + (currentTime * 8), "sine");
      }

      if (currentTime >= totalDuration) {
        pauseVideo();
        currentTime = 0;
      }
      updateUI();
    }

    drawScene(currentTime);
    animId = requestAnimationFrame(videoLoop);
  }

  function playVideo() {
    initAudioEngine();
    if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
    isPlaying = true;
    lastTimestamp = performance.now();
    if (overlayPlay) overlayPlay.style.display = "none";
    if (playIcon) playIcon.innerText = "❚❚";
    startEnglishVoiceover();
    playSoundChord(440);
  }

  function pauseVideo() {
    isPlaying = false;
    if (overlayPlay) overlayPlay.style.display = "flex";
    if (playIcon) playIcon.innerText = "▶";
    stopEnglishVoiceover();
  }

  function togglePlay() {
    isPlaying ? pauseVideo() : playVideo();
  }

  function updateUI() {
    const pct = (currentTime / totalDuration) * 100;
    if (progressBar) progressBar.style.width = `${pct}%`;

    if (timeDisplay) {
      const curM = Math.floor(currentTime / 60);
      const curS = Math.floor(currentTime % 60).toString().padStart(2, "0");
      const totM = Math.floor(totalDuration / 60);
      const totS = Math.floor(totalDuration % 60).toString().padStart(2, "0");
      timeDisplay.innerText = `${curM}:${curS} / ${totM}:${totS}`;
    }
  }

  if (overlayPlay) overlayPlay.addEventListener("click", playVideo);
  if (playBtn) playBtn.addEventListener("click", togglePlay);

  if (progressContainer) {
    progressContainer.addEventListener("click", (e) => {
      const rect = progressContainer.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const ratio = Math.max(0, Math.min(1, clickX / rect.width));
      currentTime = ratio * totalDuration;
      updateUI();
      drawScene(currentTime);
    });
  }

  if (muteBtn) {
    muteBtn.addEventListener("click", () => {
      isMuted = !isMuted;
      muteBtn.innerText = isMuted ? "🔇" : "🔊";
      if (isMuted) stopEnglishVoiceover();
    });
  }

  if (fullscreenBtn) {
    fullscreenBtn.addEventListener("click", () => {
      if (!document.fullscreenElement) {
        canvas.parentElement.requestFullscreen().catch(err => alert(err.message));
      } else {
        document.exitFullscreen();
      }
    });
  }

  drawScene(0);
  updateUI();
  animId = requestAnimationFrame(videoLoop);
}

/* 4. Prompt Engineering Drawer Toggles */
function initPromptDrawers() {
  const promptTriggers = document.querySelectorAll(".prompt-toggle-btn");
  promptTriggers.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const targetBox = document.getElementById(targetId);
      if (targetBox) {
        const isHidden = targetBox.style.display === "none" || !targetBox.style.display;
        targetBox.style.display = isHidden ? "block" : "none";
        btn.innerText = isHidden ? "Hide AI Prompt Details" : "View AI Generation Prompt";
      }
    });
  });
}
