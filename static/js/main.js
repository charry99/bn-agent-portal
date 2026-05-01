const typedPhrases = [
    'Secure on-chain identity',
    'Build reputation across apps',
    'Verified Billions Network Agent',
    'Unlock premium ecosystem perks'
];

const typedTextElement = document.getElementById('typed-text');
let phraseIndex = 0;
let charIndex = 0;
let typing = true;

function typeWriter() {
    const currentPhrase = typedPhrases[phraseIndex];
    if (typing) {
        typedTextElement.textContent = currentPhrase.slice(0, charIndex + 1);
        charIndex++;
        if (charIndex === currentPhrase.length) {
            typing = false;
            setTimeout(typeWriter, 1400);
            return;
        }
    } else {
        typedTextElement.textContent = currentPhrase.slice(0, charIndex - 1);
        charIndex--;
        if (charIndex === 0) {
            typing = true;
            phraseIndex = (phraseIndex + 1) % typedPhrases.length;
        }
    }
    setTimeout(typeWriter, typing ? 90 : 45);
}

document.addEventListener('DOMContentLoaded', () => {
    AOS.init({
        duration: 900,
        easing: 'ease-in-out',
        once: true,
        offset: 120
    });

    typeWriter();

    const navbar = document.getElementById('navbar');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });

    document.querySelectorAll('#mobile-menu a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    });

    if (window.particlesJS) {
        particlesJS('particles-js', {
            particles: {
                number: { value: 70, density: { enable: true, value_area: 1100 } },
                color: { value: ['#0FC7FF', '#1EF286', '#F5C54D'] },
                shape: { type: 'circle' },
                opacity: { value: 0.2, random: true },
                size: { value: 3, random: true },
                line_linked: { enable: true, distance: 180, color: '#0FC7FF', opacity: 0.12, width: 1 },
                move: { enable: true, speed: 1.5, direction: 'none', random: false, straight: false, out_mode: 'out', bounce: false }
            },
            interactivity: {
                detect_on: 'canvas',
                events: { onhover: { enable: true, mode: 'grab' }, onclick: { enable: true, mode: 'push' } },
                modes: { grab: { distance: 180, line_linked: { opacity: 0.2 } }, push: { particles_nb: 4 } }
            },
            retina_detect: true
        });
    }
});
