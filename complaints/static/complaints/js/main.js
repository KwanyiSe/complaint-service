// Scroll navbar shadow
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  if (navbar) {
    navbar.style.boxShadow = window.scrollY > 10 
      ? '0 4px 12px rgba(0,0,0,0.06)' 
      : '0 2px 4px rgba(0,0,0,0.03)';
  }
});

// Navbar shadow on scroll
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  if (navbar) {
    navbar.style.boxShadow = window.scrollY > 10 
      ? '0 4px 12px rgba(0,0,0,0.06)' 
      : '0 2px 4px rgba(0,0,0,0.03)';
  }
});

// Scroll‑triggered animations (for elements with class .anim-on-scroll)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('anim-visible');
      // Trigger stat counters if any
      const statAnimate = entry.target.querySelector('.stat-animate');
      if (statAnimate && !statAnimate.dataset.animated) {
        animateStat(statAnimate);
      }
      // Trigger hero progress bars
      const progressBars = entry.target.querySelectorAll('.hero-progress-fill');
      progressBars.forEach(bar => {
        if (!bar.style.width || bar.style.width === '0px') {
          bar.style.width = bar.getAttribute('data-width') || '0%';
        }
      });
    }
  });
}, { threshold: 0.2 });

document.addEventListener('DOMContentLoaded', () => {
  // Observe elements with .anim-on-scroll
  const animElements = document.querySelectorAll('.anim-on-scroll');
  animElements.forEach(el => observer.observe(el));

  // Also trigger hero progress bars if they're already in view
  document.querySelectorAll('.hero-progress-fill').forEach(bar => {
    bar.style.width = bar.getAttribute('data-width') || '0%';
  });
});

// Stat counter animation
function animateStat(el) {
  el.dataset.animated = true;
  const target = parseInt(el.getAttribute('data-target'), 10);
  const suffix = el.getAttribute('data-suffix') || '';
  const duration = 1500;
  const start = performance.now();
  const initial = 0;
  
  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const current = Math.floor(progress * target);
    el.textContent = current + suffix;
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  requestAnimationFrame(update);
}