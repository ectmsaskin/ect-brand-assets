/*
 * theme-toggle.js — ECT shared theme toggle.
 *
 * Drop into your <head> via:
 *   <script src="/brand/js/theme-toggle.js"></script>
 *
 * Add a button anywhere in the page:
 *   <button id="theme-toggle" onclick="toggleTheme()" type="button">☀ Light</button>
 *
 * What it does:
 *   - Reads `ect-theme` from localStorage on load and applies `.light` or
 *     `.dark` to <html> synchronously, so the page never flashes the wrong
 *     palette.
 *   - When the user clicks the toggle, flips the class, persists the
 *     choice, and updates the button label to indicate the *opposite*
 *     theme (so the label reads as "click me to go to <opposite>").
 *   - Defers to OS preference (prefers-color-scheme) when no explicit
 *     choice has been persisted.
 *
 * For the toggle to actually flip colors, the app's stylesheet must
 * define the dark and light branches:
 *
 *   :root.dark   { ...dark values...  }
 *   :root.light  { ...light values... }
 *   @media (prefers-color-scheme: dark) {
 *     :root:not(.light) { ...dark values... }
 *   }
 *
 * The :not(.light) check is what makes the explicit user choice win
 * over OS preference.
 */

(function () {
  var saved = localStorage.getItem('ect-theme');
  var root = document.documentElement;
  if (saved === 'light') {
    root.classList.add('light');
    root.classList.remove('dark');
  } else if (saved === 'dark') {
    root.classList.add('dark');
    root.classList.remove('light');
  }

  window.toggleTheme = function () {
    var nowDark = root.classList.contains('dark') ||
      (!root.classList.contains('light') &&
        window.matchMedia('(prefers-color-scheme: dark)').matches);
    root.classList.toggle('dark', !nowDark);
    root.classList.toggle('light', nowDark);
    localStorage.setItem('ect-theme', nowDark ? 'light' : 'dark');
    updateThemeBtn();
  };

  window.updateThemeBtn = function () {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    var isLight = root.classList.contains('light') ||
      (!root.classList.contains('dark') &&
        window.matchMedia('(prefers-color-scheme: light)').matches);
    btn.textContent = isLight ? '☽ Dark' : '☀ Light';
  };

  document.addEventListener('DOMContentLoaded', updateThemeBtn);
})();
