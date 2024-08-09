// Create and animate circles using GSAP
for (let i = 0; i < 20; i++) {
    let circle = document.createElement('div');
    circle.classList.add('circle');
    document.querySelector('.animated-bg').appendChild(circle);
    gsap.set(circle, {
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      width: Math.random() * 100 + 50,
      height: Math.random() * 100 + 50,
      opacity: 0.5
    });
    animateCircle(circle);
  }
  
  function animateCircle(circle) {
    gsap.to(circle, {
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      duration: Math.random() * 5 + 5,
      ease: 'power1.inOut',
      repeat: -1,
      yoyo: true
    });
  }
  
  // Animate the form elements
  gsap.from('.signup-form', { 
    opacity: 0, 
    y: 50, 
    duration: 1 
  });
  gsap.from('.signup-form h2', { 
    opacity: 0, 
    y: -20, 
    duration: 1, 
    delay: 0.5 
  });
  gsap.from('.form-group', { 
    opacity: 0, 
    y: 30, 
    duration: 0.8, 
    delay: 0.7, 
    stagger: 0.2 
  });
  gsap.from('.btn', { 
    opacity: 0, 
    y: 20, 
    duration: 0.8, 
    delay: 1.5 
  });
  