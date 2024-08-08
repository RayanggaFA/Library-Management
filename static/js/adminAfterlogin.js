// library/static/library/js/scripts.js

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
  
  // Button Click Animation
  document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('click', function () {
      button.classList.add('animate__animated', 'animate__bounceOut');
      setTimeout(() => {
        button.classList.remove('animate__animated', 'animate__bounceOut');
      }, 1000);
    });
  });
  
  // Tooltip Hover
  document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('mouseover', function () {
      const tooltip = document.createElement('span');
      tooltip.className = 'tooltip';
      tooltip.innerText = 'Click to proceed';
      button.appendChild(tooltip);
    });
    button.addEventListener('mouseout', function () {
      const tooltip = button.querySelector('.tooltip');
      if (tooltip) {
        button.removeChild(tooltip);
      }
    });
  });
  