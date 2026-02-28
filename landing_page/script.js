/**
 * script.js – Yeonkkachi Landing Page interactions
 */

(function () {
  "use strict";

  // ----- Mobile nav toggle -----
  const hamburger = document.getElementById("hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", function () {
      navLinks.classList.toggle("open");
      const isOpen = navLinks.classList.contains("open");
      hamburger.setAttribute("aria-expanded", String(isOpen));
    });

    // Close menu when a link is clicked.
    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("open");
        hamburger.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ----- Sample tweet feed (placeholder) -----
  // Replace the `sampleTweets` array with a real API call to your backend
  // once you have a proxy / server-side endpoint that returns recent tweets.
  const sampleTweets = [
    {
      text: "[Yeonkkachi] BUY 0.001 BTC/USD @ $65000.0000 ($65.00 USD) | confidence=72% | Momentum indicator crossed above 50-day MA #AITrading #NotFinancialAdvice",
      date: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    },
    {
      text: "[Yeonkkachi] HOLD — no trade signal generated in this cycle. #AITrading #NotFinancialAdvice",
      date: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
    },
    {
      text: "[Yeonkkachi] SELL 0.001 BTC/USD @ $64200.0000 ($64.20 USD) | confidence=65% | RSI overbought threshold breached #AITrading #NotFinancialAdvice",
      date: new Date(Date.now() - 1000 * 60 * 150).toISOString(),
    },
  ];

  function renderTweets(tweets) {
    const feed = document.getElementById("tweet-feed");
    if (!feed) return;

    feed.innerHTML = "";
    if (!tweets.length) {
      feed.innerHTML = '<p class="loading">No recent activity found.</p>';
      return;
    }

    tweets.forEach(function (t) {
      const item = document.createElement("div");
      item.className = "tweet-item";
      const dateStr = new Date(t.date).toLocaleString(undefined, {
        dateStyle: "medium",
        timeStyle: "short",
      });
      item.innerHTML =
        '<p>' + escapeHtml(t.text) + '</p>' +
        '<p class="tweet-date">' + escapeHtml(dateStr) + '</p>';
      feed.appendChild(item);
    });
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  // Render placeholder tweets on load.
  renderTweets(sampleTweets);

  // ----- Smooth scroll polyfill for older browsers -----
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
})();
