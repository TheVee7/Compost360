document.addEventListener('DOMContentLoaded', function() {
    // Initialize custom cursor
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });
});

/* static/js/cursor.js */
class CustomCursor {
    constructor() {
        this.cursor = document.createElement('div');
        this.cursor.className = 'custom-cursor';
        document.body.appendChild(this.cursor);

        this.cursor.style.width = '20px';
        this.cursor.style.height = '20px';
        this.cursor.style.border = '2px solid var(--primary-color)';
        this.cursor.style.borderRadius = '50%';
        this.cursor.style.position = 'fixed';
        this.cursor.style.pointerEvents = 'none';
        this.cursor.style.transition = 'transform 0.1s ease';
        this.cursor.style.zIndex = '9999';

        this.addEventListeners();
    }

    addEventListeners() {
        document.addEventListener('mousemove', (e) => {
            this.cursor.style.transform = `translate(${e.clientX - 10}px, ${e.clientY - 10}px)`;
        });

        document.addEventListener('mousedown', () => {
            this.cursor.style.transform = 'scale(0.8)';
        });

        document.addEventListener('mouseup', () => {
            this.cursor.style.transform = 'scale(1)';
        });
    }
}

new CustomCursor();