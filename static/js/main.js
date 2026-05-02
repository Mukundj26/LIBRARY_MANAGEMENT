/**
 * Library Administration JS Utilities
 */

// Modal Handling
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    const overlay = document.getElementById('modalOverlay');
    
    overlay.style.display = 'block';
    modal.style.display = 'block';
    
    // Force reflow for animation
    setTimeout(() => {
        overlay.style.opacity = '1';
        modal.classList.add('active');
    }, 10);
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    const overlay = document.getElementById('modalOverlay');
    
    overlay.style.opacity = '0';
    modal.classList.remove('active');
    
    setTimeout(() => {
        overlay.style.display = 'none';
        modal.style.display = 'none';
    }, 300);
}

// Global Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Close modal on overlay click
    const overlay = document.getElementById('modalOverlay');
    if(overlay) {
        overlay.addEventListener('click', () => {
            const activeModal = document.querySelector('.modal.active');
            if(activeModal) closeModal(activeModal.id);
        });
    }

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            alert.style.transition = 'all 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

/**
 * Toast Notifications
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if(!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fa-solid fa-circle-info"></i>
            <span>${message}</span>
        </div>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 10);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}
