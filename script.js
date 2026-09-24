// ============ KHỞI TẠO REVEAL.JS ============
Reveal.initialize({
    // Cấu hình cơ bản
    hash: true,
    controls: true,
    progress: true,
    center: true,
    slideNumber: 'c/t',
    transition: 'slide',           // none/fade/slide/convex/concave/zoom
    transitionSpeed: 'default',    // default/fast/slow
    backgroundTransition: 'fade',
    
    // Kích thước
    width: 1280,
    height: 720,
    margin: 0.04,
    minScale: 0.2,
    maxScale: 1.5,
    
    // Animation fragments
    fragments: true,
    fragmentInURL: true,
    
    // Auto-animate
    autoAnimate: true,
    autoAnimateDuration: 0.8,
    autoAnimateEasing: 'ease-out',
    
    // Plugins
    plugins: [ RevealNotes, RevealMarkdown, RevealHighlight, RevealZoom ]
});

// ============ COUNTER ANIMATION ============
// Đếm số khi fragment hiển thị
Reveal.addEventListener('fragmentshown', function(event) {
    const fragment = event.fragment;
    
    // Nếu fragment chứa counter
    const counter = fragment.querySelector('.counter') || 
                    (fragment.classList.contains('counter') ? fragment : null);
    
    if (counter) {
        animateCounter(counter);
    }
});

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// ============ HIỆU ỨNG ĐẶC BIỆT ============
// Tạo hiệu ứng particles cho slide bìa
Reveal.addEventListener('slidechanged', function(event) {
    const currentSlide = event.currentSlide;
    
    // Nếu là slide bìa hoặc kết thúc, thêm particles
    if (currentSlide.classList.contains('slide-bia') || 
        currentSlide.classList.contains('slide-ket-thuc')) {
        createParticles(currentSlide);
    }
});

function createParticles(slide) {
    // Xóa particles cũ
    const oldParticles = slide.querySelector('.particles-container');
    if (oldParticles) oldParticles.remove();
    
    const container = document.createElement('div');
    container.className = 'particles-container';
    container.style.cssText = `
        position: absolute;
        inset: 0;
        overflow: hidden;
        z-index: 1;
        pointer-events: none;
    `;
    
    // Tạo 20 particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        const size = Math.random() * 8 + 4;
        const colors = ['#FFC107', '#FFFFFF', '#1E88E5', '#E53935'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        particle.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: ${color};
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            opacity: ${Math.random() * 0.5 + 0.3};
            animation: float ${Math.random() * 10 + 5}s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        
        container.appendChild(particle);
    }
    
    // Thêm CSS animation
    if (!document.getElementById('particle-style')) {
        const style = document.createElement('style');
        style.id = 'particle-style';
        style.textContent = `
            @keyframes float {
                0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
                25% { transform: translate(30px, -40px) scale(1.2); opacity: 0.7; }
                50% { transform: translate(-20px, -80px) scale(0.8); opacity: 0.5; }
                75% { transform: translate(40px, -40px) scale(1.1); opacity: 0.6; }
            }
        `;
        document.head.appendChild(style);
    }
    
    slide.appendChild(container);
}

// ============ ÂM THANH CHUYỂN SLIDE (tùy chọn) ============
// Bỏ comment nếu muốn có âm thanh
/*
const slideSound = new Audio('data:audio/wav;base64,UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=');
Reveal.addEventListener('slidechanged', () => {
    slideSound.play().catch(() => {});
});
*/

// ============ PHÍM TẮT ============
document.addEventListener('keydown', function(event) {
    // Nhấn 'F' để fullscreen
    if (event.key === 'f' || event.key === 'F') {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }
    
    // Nhấn 'S' để mở speaker notes
    if (event.key === 's' || event.key === 'S') {
        // Mở cửa sổ notes
        window.open(window.location.href + '?receiver', 'receiver');
    }
});

// ============ HIỂN THỊ HƯỚNG DẪN ============
console.log(`
🎯 HƯỚNG DẪN ĐIỀU KHIỂN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ / Space    : Slide tiếp theo
←            : Slide trước
↑ / ↓        : Di chuyển fragment
F            : Bật/tắt fullscreen
S            : Speaker notes
ESC / O      : Xem tổng quan các slide
B / .        : Tạm dừng (màn hình đen)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`);
