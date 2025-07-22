// Revolution Realty Admin Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add Revolution Realty branding
    const header = document.querySelector('#header');
    if (header) {
        header.style.background = 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)';
    }

    // Enhanced form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#ef4444';
                    isValid = false;
                } else {
                    field.style.borderColor = '#10b981';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Auto-save functionality for long forms
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        let timeout;
        textarea.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                // Auto-save logic could be implemented here
                console.log('Auto-saving content...');
            }, 2000);
        });
    });

    // Enhanced table interactions
    const tables = document.querySelectorAll('.results table');
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('click', function(e) {
                if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'A') {
                    const editLink = row.querySelector('a');
                    if (editLink) {
                        window.location.href = editLink.href;
                    }
                }
            });
        });
    });

    // Quick search functionality
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"]');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                this.form.submit();
            }
        });
    });

    // Confirmation dialogs for delete actions
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Dashboard statistics (if on dashboard page)
    if (window.location.pathname.includes('/admin/') && window.location.pathname.endsWith('/admin/')) {
        loadDashboardStats();
    }

    // Bulk actions enhancement
    const actionSelect = document.querySelector('select[name="action"]');
    if (actionSelect) {
        actionSelect.addEventListener('change', function() {
            const selectedAction = this.value;
            const goButton = document.querySelector('button[name="index"]');
            
            if (selectedAction && selectedAction.includes('delete')) {
                goButton.style.background = '#ef4444';
                goButton.textContent = 'Delete Selected';
            } else {
                goButton.style.background = '#2563eb';
                goButton.textContent = 'Go';
            }
        });
    }
});

// Dashboard statistics loader
function loadDashboardStats() {
    // This would typically make AJAX calls to get real-time statistics
    console.log('Loading dashboard statistics...');
    
    // Example: Add a statistics widget
    const content = document.querySelector('#content');
    if (content) {
        const statsWidget = document.createElement('div');
        statsWidget.innerHTML = `
            <div style="background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #374151; margin-bottom: 15px;">📊 Revolution Realty Statistics</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: bold; color: #2563eb;">0</div>
                        <div style="color: #6b7280;">Total Properties</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: bold; color: #10b981;">0</div>
                        <div style="color: #6b7280;">Active Listings</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: bold; color: #f59e0b;">0</div>
                        <div style="color: #6b7280;">Pending Reviews</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: bold; color: #8b5cf6;">0</div>
                        <div style="color: #6b7280;">Total Users</div>
                    </div>
                </div>
            </div>
        `;
        content.insertBefore(statsWidget, content.firstChild);
    }
}

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `messagelist ${type}`;
    notification.innerHTML = `<div class="message">${message}</div>`;
    
    const content = document.querySelector('#content');
    if (content) {
        content.insertBefore(notification, content.firstChild);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

