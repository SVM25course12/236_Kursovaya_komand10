document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section');

    const navDots = document.querySelectorAll('.nav-dot');

    const observerOptions = {
        root: null,
        threshold: 0.3,
        rootMargin: '-10% 0px -10% 0px'
    };
    function handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sectionId = entry.target.id;
                updateActiveNav(sectionId);
            }
        });
    }

    const observer = new IntersectionObserver(handleIntersection, observerOptions);
    sections.forEach(section => {
        observer.observe(section);
    });

    function updateActiveNav(activeSectionId) {
        navDots.forEach(dot => {
            const dotSection = dot.getAttribute('data-section');
            dot.classList.remove('active');
            if (dotSection === activeSectionId) {
                dot.classList.add('active');
            }
        });
    }

    navDots.forEach(dot => {
        dot.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    sections.forEach(section => {
        if (section.id !== 'hero') {
            animationObserver.observe(section);
        }
    });

    console.log('🎨 Навигация инициализирована');
    console.log('📍 Найдено секций:', sections.length);
    console.log('🔘 Найдено пунктов навигации:', navDots.length);
});

