document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  scatterStars();
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
