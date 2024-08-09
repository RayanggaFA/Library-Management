AOS.init({
    duration: 1200,
});

// Add a click animation to buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('mousedown', () => {
        button.classList.add('clicked');
    });
    button.addEventListener('mouseup', () => {
        setTimeout(() => {
            button.classList.remove('clicked');
        }, 150);
    });
});

// Custom scroll to top button
const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.innerHTML = '<i class="fa fa-arrow-up"></i>';
scrollToTopBtn.classList.add('btn', 'btn-primary', 'scroll-to-top');
document.body.appendChild(scrollToTopBtn);

window.addEventListener('scroll', () => {
    if (window.scrollY > 200) {
        scrollToTopBtn.classList.add('visible');
    } else {
        scrollToTopBtn.classList.remove('visible');
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// CSS for scroll-to-top button
const style = document.createElement('style');
style.innerHTML = `
    .scroll-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: none;
        opacity: 0.8;
        transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
    }

    .scroll-to-top.visible {
        display: block;
        opacity: 1;
        visibility: visible;
    }
`;
document.head.appendChild(style);
