function celebrateDay() {
    const button = document.querySelector('.great-day-btn');
    const centerContent = document.querySelector('.center-content');
    
    // Add celebration animation to button
    button.classList.add('celebrating');
    
    // Create sparkle effects
    createSparkles(centerContent);
    
    // Change button text temporarily
    const originalText = button.textContent;
    button.textContent = '✨ Amazing! ✨';
    
    // Reset after animation
    setTimeout(() => {
        button.classList.remove('celebrating');
        button.textContent = originalText;
    }, 600);
}

function createSparkles(container) {
    const sparkleCount = 12;
    
    for (let i = 0; i < sparkleCount; i++) {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        
        // Random position around the button
        const angle = (i / sparkleCount) * 2 * Math.PI;
        const radius = 80 + Math.random() * 40;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;
        
        sparkle.style.left = `${x}px`;
        sparkle.style.top = `${y}px`;
        
        container.appendChild(sparkle);
        
        // Remove sparkle after animation
        setTimeout(() => {
            if (sparkle.parentNode) {
                sparkle.parentNode.removeChild(sparkle);
            }
        }, 1000);
    }
}

// Add some gentle movement to clouds on mouse move
document.addEventListener('mousemove', (e) => {
    const clouds = document.querySelectorAll('.cloud');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    clouds.forEach((cloud, index) => {
        const speed = (index + 1) * 0.5;
        const x = (mouseX - 0.5) * speed;
        const y = (mouseY - 0.5) * speed;
        
        cloud.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// Add gentle parallax effect to hot air balloon
document.addEventListener('mousemove', (e) => {
    const balloon = document.querySelector('.hot-air-balloon');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    const x = (mouseX - 0.5) * 10;
    const y = (mouseY - 0.5) * 10;
    
    balloon.style.transform = `translate(${x}px, ${y}px)`;
});