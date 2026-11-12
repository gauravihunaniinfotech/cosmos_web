/* COSMO'S — About page interactions. Vanilla JS, no dependencies.
   Runs after the shared script.js (header, mobile nav, counters, smooth anchors). */
(function () {
  'use strict';
  var d = document;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  /* 1 · Split headings into masked words (keeps <em> styling) */
  function splitNode(node, counter) {
    Array.prototype.slice.call(node.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var frag = d.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(' ')); return; }
          var w = d.createElement('span'), i = d.createElement('span');
          w.className = 'w'; i.className = 'wi'; i.style.setProperty('--i', counter.n++); i.textContent = part;
          w.appendChild(i); frag.appendChild(w);
        });
        node.replaceChild(frag, n);
      } else if (n.nodeType === 1) { splitNode(n, counter); }
    });
  }
  $$('[data-split]').forEach(function (el) {
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    splitNode(el, { n: 0 });
    $$('.w', el).forEach(function (w) { w.setAttribute('aria-hidden', 'true'); });
    el.classList.add('is-split');
  });

  /* 2 · Reveal on scroll */
  var targets = $$('[data-a], .a-img, .a-mission__media, .is-split, .a-tl__item, .a-step');
  if ('IntersectionObserver' in window && !reduce) {
    var map = new Map();   /* observed element -> elements to reveal */
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        (map.get(e.target) || []).forEach(function (t) { t.classList.add('is-in'); });
        io.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    /* a fully clip-pathed element reports zero visible area, so watch its parent instead */
    targets.forEach(function (t) {
      var clipped = t.classList.contains('a-img') || t.classList.contains('a-mission__media');
      var host = clipped ? t.parentElement : t;
      if (!map.has(host)) { map.set(host, []); io.observe(host); }
      map.get(host).push(t);
      if (clipped && !map.get(host).includes(host) && targets.indexOf(host) > -1) map.get(host).push(host);
    });
  } else { targets.forEach(function (t) { t.classList.add('is-in'); }); }

  /* 3 · Subtle parallax (transform only, rAF-throttled) */
  var par = $$('[data-par]');
  var run = function () {
    var vh = window.innerHeight;
    par.forEach(function (img) {
      var host = img.parentElement.getBoundingClientRect();
      if (host.bottom < -200 || host.top > vh + 200) return;
      var s = parseFloat(img.dataset.par) || 0.08;
      var y = (host.top + host.height / 2 - vh / 2) * -s;
      img.style.transform = 'translate3d(0,' + y.toFixed(1) + 'px,0)' + (img.closest('.a-hero__bg,.a-commit__bg') ? '' : ' scale(1.06)');
    });
  };
  if (par.length && !reduce) {
    var tick = false;
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(function () { run(); tick = false; }); } }, { passive: true });
    window.addEventListener('resize', run); run();
  }

  /* 4 · Scroll-linked progress for timeline and process line */
  var prog = $$('[data-progress]');
  function progress() {
    var vh = window.innerHeight;
    prog.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = (vh * 0.65 - r.top) / Math.max(r.height, 1);
      el.style.setProperty('--p', Math.max(0, Math.min(1, p)).toFixed(3));
    });
  }
  if (prog.length) {
    if (reduce) { prog.forEach(function (el) { el.style.setProperty('--p', 1); }); }
    else {
      var pt = false;
      window.addEventListener('scroll', function () { if (!pt) { pt = true; requestAnimationFrame(function () { progress(); pt = false; }); } }, { passive: true });
      window.addEventListener('resize', progress); progress();
    }
  }

  /* 5 · Page transition: fade to teal before leaving for another page */
  var curtain = d.querySelector('.a-curtain');
  $$('a[href]').forEach(function (a) {
    var h = a.getAttribute('href');
    if (!h || h.charAt(0) === '#' || /^(mailto:|tel:|https?:|javascript:)/i.test(h) || a.target === '_blank') return;
    a.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0 || reduce || !curtain) return;
      e.preventDefault(); curtain.classList.add('is-leaving');
      setTimeout(function () { window.location.href = a.href; }, 320);
    });
  });
  window.addEventListener('pageshow', function (e) { if (e.persisted && curtain) curtain.classList.remove('is-leaving'); });
})();
