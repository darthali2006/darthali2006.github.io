document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  scatterStars();
  scatterSnow();
  setupRealmToggle();
  revealOnScroll();
  console.log(
    "%cI solemnly swear that I am up to no good.%c\nWell met, fellow hacker. This site has a strict CSP and no " +
      "third-party scripts. If you find a bug anyway, see /.well-known/security.txt. Mischief managed.",
    "font: 700 14px monospace; color: #e3b55b",
    "font: 12px monospace"
  );
});

// Seeded so the sky looks the same on every visit.
function scatterStars() {
  const sky = document.querySelector(".sky");
  if (!sky) return;
  let seed = 42;
  const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const frag = document.createDocumentFragment();
  for (let i = 0; i < 70; i++) {
    const star = document.createElement("span");
    star.className = "star";
    star.style.left = `${rand() * 100}%`;
    star.style.top = `${rand() * 62}%`;
    star.style.setProperty("--o", (0.25 + rand() * 0.6).toFixed(2));
    if (rand() < 0.3) {
      star.classList.add("twinkle");
      star.style.setProperty("--d", `${4 + rand() * 5}s`);
      star.style.setProperty("--delay", `${-rand() * 8}s`);
    }
    frag.appendChild(star);
  }
  sky.appendChild(frag);
}

function revealOnScroll() {
  const items = [...document.querySelectorAll(".reveal")];
  if (!("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("is-in"));
    return;
  }

  // Stagger siblings that enter together, 60ms apart.
  const observer = new IntersectionObserver(
    (entries) => {
      entries
        .filter((e) => e.isIntersecting)
        .forEach((e, i) => {
          e.target.style.setProperty("--stagger", `${Math.min(i, 6) * 60}ms`);
          e.target.classList.add("is-in");
          observer.unobserve(e.target);
        });
    },
    { rootMargin: "0px 0px -8% 0px" }
  );
  items.forEach((el) => observer.observe(el));
}

function scatterSnow() {
  const sky = document.querySelector(".sky");
  if (!sky) return;
  let seed = 7;
  const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const frag = document.createDocumentFragment();
  for (let i = 0; i < 48; i++) {
    const flake = document.createElement("span");
    flake.className = "flake";
    flake.style.left = `${rand() * 100}%`;
    flake.style.setProperty("--o", (0.35 + rand() * 0.5).toFixed(2));
    flake.style.setProperty("--y", `${(rand() * 95).toFixed(1)}vh`);
    flake.style.setProperty("--drift", `${(rand() * 40 - 20).toFixed(0)}px`);
    flake.style.setProperty("--d", `${(10 + rand() * 10).toFixed(1)}s`);
    flake.style.setProperty("--delay", `${(-rand() * 20).toFixed(1)}s`);
    frag.appendChild(flake);
  }
  sky.appendChild(frag);
}

const REALMS = {
  nightfall: { next: "storybook", label: "Storybook" },
  storybook: { next: "nightfall", label: "Nightfall" },
};

function setupRealmToggle() {
  const root = document.documentElement;
  const button = document.querySelector(".realm-toggle");
  if (!button) return;
  const label = button.querySelector(".realm-label");
  const night = document.querySelector(".scene-night");
  const story = document.querySelector(".scene-storybook");

  const render = () => {
    const current = root.getAttribute("data-realm") === "storybook" ? "storybook" : "nightfall";
    label.textContent = REALMS[current].label;
    button.setAttribute("aria-pressed", String(current === "storybook"));
    button.setAttribute("aria-label", `Switch to the ${REALMS[current].label} theme`);
    if (night && story) {
      night.toggleAttribute("aria-hidden", current === "storybook");
      story.toggleAttribute("aria-hidden", current !== "storybook");
    }
  };

  button.addEventListener("click", () => {
    const current = root.getAttribute("data-realm") === "storybook" ? "storybook" : "nightfall";
    const next = REALMS[current].next;
    if (next === "storybook") root.setAttribute("data-realm", "storybook");
    else root.removeAttribute("data-realm");
    try {
      localStorage.setItem("realm", next);
    } catch (e) {}
    render();
  });

  render();
  // Only animate realm changes the visitor makes, never the initial paint.
  requestAnimationFrame(() => requestAnimationFrame(() => root.classList.add("realm-ready")));
}
