/**
 * MORE THAN GRADES — Client-Side Instant Search Engine (100% English)
 * Real-time fuzzy keyword search across all 8 pages & sections
 */

const siteSearchIndex = [
  // 1. Home
  {
    title: "Homepage | More Than Grades",
    url: "index.html",
    category: "Home",
    keywords: ["home", "grades", "exams", "school", "university", "slogan", "video", "awareness", "student", "wellbeing"],
    description: "The premier student advocacy digital platform: exploring the real student experience beyond report cards and test metrics."
  },
  {
    title: "AI Narrative Video Showcase: Your Grade is Part of You, Not All of You",
    url: "index.html#video-player",
    category: "Media & Video",
    keywords: ["video", "audio", "narrative", "voiceover", "runway", "elevenlabs", "ai generated video", "inspiration", "motivation"],
    description: "A 35-second AI-synthesized narrative video clip with synchronized vocal narration and cinematic visuals on human worth."
  },

  // 2. About Us
  {
    title: "About Us | Platform Mission & Vision",
    url: "about.html",
    category: "About",
    keywords: ["about us", "mission", "vision", "goals", "team", "counselor", "uae", "wellbeing", "values", "compassion"],
    description: "Discover the founding story of More Than Grades, our virtual counseling team, and our dedication to youth mental health."
  },
  {
    title: "Alignment with UAE National Wellbeing Strategy 2031",
    url: "about.html#uae-strategy",
    category: "National Strategy",
    keywords: ["strategy", "uae", "wellbeing 2031", "ministry of education", "national vision", "schools", "youth"],
    description: "How our platform supports UAE national initiatives in fostering positive, resilient, and inclusive academic environments."
  },

  // 3. Feature 1: Your Words Matter (Anti-Bullying)
  {
    title: "Your Words Matter | Anti-Bullying Advocacy & Peer Solidarity",
    url: "feature-anti-bullying.html",
    category: "Feature 1",
    keywords: ["bullying", "cyberbullying", "words matter", "peer support", "solidarity", "upstander", "kindness", "harassment"],
    description: "A comprehensive guide on standing up against verbal and online bullying, and how to become an active upstander for peers."
  },
  {
    title: "Rashid's Story: The Power of One Encouraging Sentence",
    url: "feature-anti-bullying.html#story-rashid",
    category: "Case Scenarios",
    keywords: ["rashid", "story", "scenario", "friendship", "courage", "empathy", "classroom"],
    description: "An AI-illustrated narrative demonstrating how an encouraging word from a classmate broke the cycle of classroom ridicule."
  },

  // 4. Feature 2: First Day Together (New Student Inclusion)
  {
    title: "First Day Together | New Student Adaptation & Friendship Guide",
    url: "feature-new-student.html",
    category: "Feature 2",
    keywords: ["new student", "transfer", "relocation", "friendship", "loneliness", "first day", "inclusion", "social anxiety"],
    description: "Practical strategies to overcome first-day hesitation, break the ice, and build authentic friendships across campuses."
  },
  {
    title: "Mariam's Story: From Quiet Corner to Campus Community",
    url: "feature-new-student.html#story-mariam",
    category: "Case Scenarios",
    keywords: ["mariam", "transfer student", "adaptation", "inclusion", "belonging", "school cafeteria"],
    description: "The journey of a relocated student in Abu Dhabi who found warmth and lifelong friendship through a simple lunch invitation."
  },

  // 5. Feature 3: Exam Season Balance (Stress Management)
  {
    title: "Exam Season Balance | Managing Anxiety & Smart Study Methods",
    url: "feature-exam-stress.html",
    category: "Feature 3",
    keywords: ["exams", "tests", "stress", "anxiety", "pomodoro", "study habits", "sleep hygiene", "active recall", "breathing"],
    description: "Evidence-based study frameworks, Pomodoro focus cycles, and mindfulness exercises to decouple GPA from personal self-worth."
  },
  {
    title: "Smart Study Framework & 4-7-8 Breathing Techniques",
    url: "feature-exam-stress.html#study-methods",
    category: "Tools & Tips",
    keywords: ["pomodoro", "mind maps", "active recall", "relaxation", "cortisol", "panic relief"],
    description: "Techniques for spaced repetition, restorative breaks, and quick physiological breathing to reduce pre-exam test panic."
  },

  // 6. Feature 4: A Space for Your Passion (Extracurricular Talents)
  {
    title: "A Space for Your Passion | Celebrating Student Talents & Innovation",
    url: "feature-student-talents.html",
    category: "Feature 4",
    keywords: ["talents", "passions", "digital art", "robotics", "ai coding", "athletics", "extracurricular", "creativity"],
    description: "A showcase dedicated to appreciating non-academic gifts: algorithmic programming, digital illustration, and athletics."
  },
  {
    title: "Student Talent Exhibition: Coding, Arts & Athletic Leadership",
    url: "feature-student-talents.html#talent-showcase",
    category: "Talent Showcase",
    keywords: ["coding", "hackathon", "fine arts", "track and field", "future skills", "mentorship"],
    description: "Celebrating student creators who apply their innate passions to build impactful community solutions outside curricula."
  },

  // 7. Feature 5: Inspiring Journeys (Bonus Case Studies)
  {
    title: "Inspiring Journeys (Bonus Feature) | Student Triumph Case Studies",
    url: "feature-inspiring-stories.html",
    category: "Bonus Feature",
    keywords: ["inspiring stories", "sultan", "noura", "khaled", "prompt logs", "midjourney", "case studies", "triumph"],
    description: "An exclusive digital anthology of AI-crafted student success stories with transparent prompt engineering comparison logs."
  },

  // 8. Contact & Helplines
  {
    title: "Contact & Support | Safe Confidential Peer Inquiry",
    url: "contact.html",
    category: "Contact",
    keywords: ["contact", "anonymous", "support form", "counseling", "helplines", "inquiry", "feedback"],
    description: "Send an inquiry or experience with complete anonymity, and access official verified crisis hotlines across the UAE."
  },
  {
    title: "Official UAE Child Protection & Mental Health Helplines",
    url: "contact.html#emergency-helplines",
    category: "Emergency Helplines",
    keywords: ["116111", "estijaba", "8001717", "hope", "8004673", "child protection", "crisis support"],
    description: "Toll-free, 24/7 official government hotlines providing immediate psychological and child wellbeing assistance in the UAE."
  }
];

// Search Engine Logic
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("search-modal");
  const openBtns = document.querySelectorAll(".btn-search-trigger");
  const closeBtn = document.getElementById("search-modal-close");
  const searchInput = document.getElementById("search-modal-input");
  const resultsContainer = document.getElementById("search-results-box");

  if (!modal || !searchInput || !resultsContainer) return;

  function openSearchModal() {
    modal.classList.add("open");
    document.body.style.overflow = "hidden";
    setTimeout(() => searchInput.focus(), 100);
    renderResults(siteSearchIndex.slice(0, 4), "Recommended Topics:");
  }

  function closeSearchModal() {
    modal.classList.remove("open");
    document.body.style.overflow = "";
    searchInput.value = "";
  }

  openBtns.forEach(btn => btn.addEventListener("click", openSearchModal));
  if (closeBtn) closeBtn.addEventListener("click", closeSearchModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeSearchModal();
  });

  // Keyboard shortcut (Ctrl + K or Cmd + K or /)
  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      modal.classList.contains("open") ? closeSearchModal() : openSearchModal();
    } else if (e.key === "Escape" && modal.classList.contains("open")) {
      closeSearchModal();
    }
  });

  // Real-time query execution
  searchInput.addEventListener("input", (e) => {
    const query = e.target.value.trim().toLowerCase();
    if (!query) {
      renderResults(siteSearchIndex.slice(0, 4), "Recommended Topics:");
      return;
    }

    const filtered = siteSearchIndex.filter(item => {
      const matchTitle = item.title.toLowerCase().includes(query);
      const matchDesc = item.description.toLowerCase().includes(query);
      const matchKeywords = item.keywords.some(k => k.toLowerCase().includes(query));
      return matchTitle || matchDesc || matchKeywords;
    });

    renderResults(filtered, `Search Results for “${e.target.value}” (${filtered.length} matches):`);
  });

  function renderResults(items, headerText) {
    if (items.length === 0) {
      resultsContainer.innerHTML = `
        <div style="text-align: center; padding: 2.5rem 1rem; color: #94a3b8;">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
          <p style="font-size: 1.1rem; font-weight: 700; color: #f8fafc;">No matching results found!</p>
          <p style="font-size: 0.9rem; margin-top: 0.35rem;">Try searching for keywords like: bullying, exams, stress, talents, story, or new student.</p>
        </div>
      `;
      return;
    }

    let html = `<div style="font-size: 0.85rem; font-weight: 700; color: #34d399; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;">${headerText}</div>`;
    items.forEach(item => {
      html += `
        <a href="${item.url}" class="search-result-item">
          <div class="search-result-category">${item.category}</div>
          <div class="search-result-title">${item.title}</div>
          <div class="search-result-desc">${item.description}</div>
        </a>
      `;
    });
    resultsContainer.innerHTML = html;
  }
});
