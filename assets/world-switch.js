// Plays the switch flip, then follows the link. Modified clicks open as usual.
document.addEventListener("click", (e) => {
  const link = e.target.closest(".world-switch");
  if (!link || e.defaultPrevented || e.button !== 0) return;
  if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  e.preventDefault();
  link.classList.add("is-going");
  setTimeout(() => {
    window.location.href = link.href;
  }, 240);
});
// Coming back with the browser's back button restores the page as it was.
window.addEventListener("pageshow", () => {
  document.querySelectorAll(".world-switch.is-going").forEach((el) => el.classList.remove("is-going"));
});
