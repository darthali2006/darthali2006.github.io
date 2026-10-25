// Runs before first paint so a saved realm never flashes the default scene.
(function () {
  try {
    if (localStorage.getItem("realm") === "storybook") {
      document.documentElement.setAttribute("data-realm", "storybook");
    }
  } catch (e) {}
})();
