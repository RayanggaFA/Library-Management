document.addEventListener('DOMContentLoaded', function() {
    M.AutoInit();
    createShapes();
});

function validateForm() {
    let valid = true;
    document.querySelectorAll('.validate').forEach(input => {
        if (input.value.trim() === '') {
            valid = false;
            input.classList.add('invalid');
        } else {
            input.classList.remove('invalid');
        }
    });
    return valid;
}

function createShapes() {
    const background = document.getElementById('background');
    for (let i = 0; i < 30; i++) {
        const shape = document.createElement('div');
        shape.classList.add('shape');

        const size = Math.random() * 100 + 50;
        shape.style.width = `${size}px`;
        shape.style.height = `${size}px`;
        shape.style.borderRadius = `${Math.random() * 50}%`;

        shape.style.left = `${Math.random() * window.innerWidth}px`;
        shape.style.top = `${Math.random() * window.innerHeight}px`;

        shape.style.animationDelay = `${Math.random() * 20}s`;
        shape.style.animationDuration = `${Math.random() * 20 + 20}s`;

        background.appendChild(shape);
    }
}
