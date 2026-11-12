/* COSMO'S — FAQ behaviour shared by Services + Comfort Club (one answer open at a time). */
(function () {
  'use strict';
  var items = Array.prototype.slice.call(document.querySelectorAll('.faq details'));
  items.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      items.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });
})();
