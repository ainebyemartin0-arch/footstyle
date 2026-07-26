// ========================================================================
// FOOTSTYLE - ELITE PREMIUM ANIMATION UPGRADE (ES6+)
// ========================================================================

// 1. Dynamic Copyright Date
document.getElementById('copyright-year').textContent = new Date().getFullYear();

// 2. Page Load Fade-In (Smooth transition between pages)
const mainContent = document.getElementById('main-content');
if (mainContent) {
    mainContent.classList.add('main-fade-in');
    // Remove class after animation to allow normal DOM updates
    mainContent.addEventListener('animationend', () => {
        mainContent.classList.remove('main-fade-in');
    }, { once: true });
}

// 3. IntersectionObserver for Scroll Reveal (Strict Phase 3 rule)
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) { 
            entry.target.classList.add('is-visible'); 
            observer.unobserve(entry.target); 
        }
    });
}, observerOptions);
document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));

// 4. Back to Top Logic
const backToTopBtn = document.getElementById('backToTopBtn');
window.addEventListener('scroll', () => { backToTopBtn.style.display = window.scrollY > 300 ? 'flex' : 'none'; }, { passive: true });
backToTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// 5. Cart Badge Pop Logic (Visual feedback when returning from Add-to-Cart)
// If user returns to a page with items in cart, pop the badge once
const cartBadge = document.querySelector('.cart-badge-nav');
if (cartBadge) {
    // Pop on initial load if cart has items
    cartBadge.classList.add('pop');
}

// 6. Event Delegation for Interactions (Performance Phase 4)
document.addEventListener('click', (e) => {
    // Wishlist Toggle
    if (e.target.closest('.wishlist-btn')) {
        e.preventDefault();
        e.target.closest('.wishlist-btn').classList.toggle('is-liked');
    }
    // Gallery Thumbnail
    if (e.target.closest('.thumb')) {
        const thumb = e.target.closest('.thumb');
        const mainImg = document.getElementById('mainDetailImg');
        if (mainImg && thumb.dataset.full) {
            mainImg.style.opacity = '0';
            setTimeout(() => { mainImg.src = thumb.dataset.full; mainImg.style.opacity = '1'; }, 250);
            document.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
        }
    }
    // Size/Color Selectors
    if (e.target.closest('.pill-btn')) {
        const group = e.target.closest('.selector-group');
        if (group) {
            group.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('selected'));
            e.target.closest('.pill-btn').classList.add('selected');
        }
    }
});

console.log("FootStyle Elite Engine Initialized (Premium Animation Mode).");
