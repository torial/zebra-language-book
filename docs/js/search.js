// Zebra Programming Book - Search and Navigation

function initializeSearch(searchBox) {
    if (!searchBox) return;

    searchBox.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const chapters = document.querySelectorAll('.sidebar-nav a');

        chapters.forEach(chapter => {
            const text = chapter.textContent.toLowerCase();
            chapter.style.display = text.includes(query) ? 'block' : 'none';
        });
    });
}

// Theme toggle
function toggleTheme() {
    const isDark = document.documentElement.style.colorScheme === 'dark';
    document.documentElement.style.colorScheme = isDark ? 'light' : 'dark';
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
}

// Load saved theme
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.style.colorScheme = savedTheme;
    }
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
