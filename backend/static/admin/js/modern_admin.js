// Revolution Realty - Modern Admin JavaScript
// Interactive features for the modern admin interface

document.addEventListener('DOMContentLoaded', function() {
    initializeModernAdmin();
});

function initializeModernAdmin() {
    // Initialize navigation
    initializeNavigation();
    
    // Initialize dashboard features
    initializeDashboard();
    
    // Initialize responsive features
    initializeResponsive();
    
    // Initialize tooltips and interactions
    initializeInteractions();
}

function initializeNavigation() {
    // Add active state to current navigation item
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath.includes(href)) {
            item.classList.add('active');
        }
    });
    
    // Mobile navigation toggle
    const navToggle = document.createElement('button');
    navToggle.className = 'nav-toggle';
    navToggle.innerHTML = '☰';
    navToggle.style.display = 'none';
    
    const header = document.querySelector('.modern-header');
    if (header) {
        header.appendChild(navToggle);
    }
    
    navToggle.addEventListener('click', function() {
        const nav = document.querySelector('.modern-nav');
        if (nav) {
            nav.classList.toggle('nav-open');
        }
    });
}

function initializeDashboard() {
    // Animate metric cards on load
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add click handlers for quick actions
    const quickActions = document.querySelectorAll('.quick-action');
    quickActions.forEach(action => {
        action.addEventListener('click', function(e) {
            // Add ripple effect
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(37, 99, 235, 0.3)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.left = e.offsetX + 'px';
            ripple.style.top = e.offsetY + 'px';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            
            this.style.position = 'relative';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Update real-time data (simulated)
    updateDashboardData();
    setInterval(updateDashboardData, 30000); // Update every 30 seconds
}

function updateDashboardData() {
    // Simulate real-time updates
    const metricValues = document.querySelectorAll('.metric-value');
    metricValues.forEach(value => {
        const currentValue = parseInt(value.textContent.replace(/[^0-9]/g, ''));
        if (currentValue && Math.random() > 0.8) {
            // Occasionally update values
            const change = Math.floor(Math.random() * 5) - 2;
            const newValue = Math.max(0, currentValue + change);
            
            if (value.textContent.includes('$')) {
                value.textContent = '$' + newValue.toLocaleString();
            } else {
                value.textContent = newValue.toLocaleString();
            }
            
            // Add flash effect
            value.style.background = 'rgba(37, 99, 235, 0.1)';
            setTimeout(() => {
                value.style.background = 'transparent';
            }, 1000);
        }
    });
}

function initializeResponsive() {
    // Handle responsive navigation
    function handleResize() {
        const nav = document.querySelector('.modern-nav');
        const navToggle = document.querySelector('.nav-toggle');
        
        if (window.innerWidth <= 1024) {
            if (navToggle) navToggle.style.display = 'block';
            if (nav) nav.classList.add('nav-mobile');
        } else {
            if (navToggle) navToggle.style.display = 'none';
            if (nav) {
                nav.classList.remove('nav-mobile', 'nav-open');
            }
        }
    }
    
    window.addEventListener('resize', handleResize);
    handleResize(); // Initial call
}

function initializeInteractions() {
    // Add hover effects to cards
    const cards = document.querySelectorAll('.metric-card, .dashboard-widget, .quick-action');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add loading states for buttons
    const buttons = document.querySelectorAll('.action-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="spinner"></span> Loading...';
            this.disabled = true;
            
            // Simulate loading
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 1000);
        });
    });
    
    // Add search functionality
    const searchInputs = document.querySelectorAll('input[placeholder*="filter"]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const items = document.querySelectorAll('.nav-item, .activity-item, .tenant-item');
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-lg);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .spinner {
        display: inline-block;
        width: 12px;
        height: 12px;
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .nav-mobile {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .nav-mobile.nav-open {
        transform: translateX(0);
    }
    
    .nav-toggle {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        padding: 0.5rem;
        border-radius: var(--radius-md);
        cursor: pointer;
        font-size: 1.25rem;
    }
    
    .notification-success {
        border-left: 4px solid var(--success-color);
    }
    
    .notification-warning {
        border-left: 4px solid var(--warning-color);
    }
    
    .notification-error {
        border-left: 4px solid var(--danger-color);
    }
    
    .notification-info {
        border-left: 4px solid var(--info-color);
    }
`;

document.head.appendChild(style);

