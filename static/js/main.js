// Theme Toggle Functionality
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    
    if (body.classList.contains('bg-gray-900')) {
        // Switch to light mode
        body.className = body.className.replace('bg-gray-900 text-white', 'bg-white text-gray-900');
        themeIcon.className = 'fas fa-sun';
        localStorage.setItem('theme', 'light');
        
        // Update all dark elements to light
        document.querySelectorAll('.bg-gray-800').forEach(el => {
            el.classList.remove('bg-gray-800');
            el.classList.add('bg-gray-100');
        });
        
        document.querySelectorAll('.text-white').forEach(el => {
            el.classList.remove('text-white');
            el.classList.add('text-gray-900');
        });
        
        document.querySelectorAll('.text-gray-300').forEach(el => {
            el.classList.remove('text-gray-300');
            el.classList.add('text-gray-600');
        });
        
    } else {
        // Switch to dark mode
        body.className = body.className.replace('bg-white text-gray-900', 'bg-gray-900 text-white');
        themeIcon.className = 'fas fa-moon';
        localStorage.setItem('theme', 'dark');
        
        // Update all light elements to dark
        document.querySelectorAll('.bg-gray-100').forEach(el => {
            el.classList.remove('bg-gray-100');
            el.classList.add('bg-gray-800');
        });
        
        document.querySelectorAll('.text-gray-900').forEach(el => {
            el.classList.remove('text-gray-900');
            el.classList.add('text-white');
        });
        
        document.querySelectorAll('.text-gray-600').forEach(el => {
            el.classList.remove('text-gray-600');
            el.classList.add('text-gray-300');
        });
    }
}

// Load saved theme on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const themeIcon = document.getElementById('themeIcon');
    
    if (savedTheme === 'light') {
        document.body.className = document.body.className.replace('bg-gray-900 text-white', 'bg-white text-gray-900');
        if (themeIcon) themeIcon.className = 'fas fa-sun';
    } else {
        if (themeIcon) themeIcon.className = 'fas fa-moon';
    }
});

// File upload functionality
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('cv-file');
    const uploadArea = document.getElementById('fileUploadArea');
    
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('border-blue-500');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('border-blue-500');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-blue-500');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                updateFileName(fileInput);
            }
        });
    }
});

function updateFileName(input) {
    const fileName = input.files[0]?.name || '';
    const fileNameDisplay = document.querySelector('.file-name');
    if (fileNameDisplay) {
        fileNameDisplay.textContent = fileName;
    }
}