// Lightweight UI helpers for the dashboard
(function () {
    const ModalManager = {
        modals: new Map(),
        backdrop: null,
        activeModal: null,

        init() {
            this.backdrop = document.createElement('div');
            this.backdrop.className = 'modal-backdrop';
            this.backdrop.addEventListener('click', () => this.close());
            document.body.appendChild(this.backdrop);

            document.querySelectorAll('.modal').forEach(modal => {
                const id = modal.getAttribute('id') || `modal-${this.modals.size + 1}`;
                if (!modal.getAttribute('id')) {
                    modal.setAttribute('id', id);
                }
                modal.setAttribute('aria-hidden', 'true');
                modal.setAttribute('role', 'dialog');
                modal.setAttribute('aria-modal', 'true');
                modal.setAttribute('tabindex', '-1');
                this.modals.set(id, modal);

                modal.querySelectorAll('[data-modal-close]').forEach(btn => {
                    btn.addEventListener('click', evt => {
                        evt.preventDefault();
                        this.close();
                    });
                });
            });

            document.addEventListener('keydown', evt => {
                if (evt.key === 'Escape' && this.activeModal) {
                    this.close();
                }
            });
        },

        open(id) {
            const modal = this.modals.get(id);
            if (!modal) {
                console.warn(`Modal ${id} not found`);
                return;
            }
            this.activeModal = modal;
            modal.classList.add('is-open');
            modal.setAttribute('aria-hidden', 'false');
            this.backdrop.classList.add('is-visible');
            document.body.classList.add('has-open-modal');
            const focusTarget = modal.querySelector('[data-initial-focus]') || modal.querySelector('input, button, textarea, select');
            if (focusTarget) {
                focusTarget.focus({ preventScroll: true });
            }
        },

        close() {
            if (!this.activeModal) {
                return;
            }
            this.activeModal.classList.remove('is-open');
            this.activeModal.setAttribute('aria-hidden', 'true');
            this.activeModal = null;
            this.backdrop.classList.remove('is-visible');
            document.body.classList.remove('has-open-modal');
        }
    };

    const ToastManager = {
        container: null,
        init() {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        },
        show(message, variant = 'default') {
            if (!this.container) {
                this.init();
            }
            const toast = document.createElement('div');
            toast.className = `toast-message toast-${variant}`;
            toast.setAttribute('role', 'status');
            toast.textContent = message;
            this.container.appendChild(toast);
            requestAnimationFrame(() => toast.classList.add('is-visible'));
            setTimeout(() => {
                toast.classList.remove('is-visible');
                setTimeout(() => toast.remove(), 200);
            }, 3200);
        }
    };

    const TooltipManager = {
        init() {
            document.querySelectorAll('[data-tooltip]').forEach(trigger => {
                trigger.addEventListener('mouseenter', () => this.show(trigger));
                trigger.addEventListener('mouseleave', () => this.hide(trigger));
                trigger.addEventListener('focus', () => this.show(trigger));
                trigger.addEventListener('blur', () => this.hide(trigger));
            });
        },
        show(trigger) {
            const text = trigger.getAttribute('data-tooltip');
            if (!text) {
                return;
            }
            let tooltip = trigger._tooltipEl;
            if (!tooltip) {
                tooltip = document.createElement('div');
                tooltip.className = 'tooltip-bubble';
                tooltip.textContent = text;
                document.body.appendChild(tooltip);
                trigger._tooltipEl = tooltip;
            }
            const rect = trigger.getBoundingClientRect();
            tooltip.style.left = `${rect.left + rect.width / 2}px`;
            tooltip.style.top = `${rect.top - 8}px`;
            tooltip.classList.add('is-visible');
        },
        hide(trigger) {
            if (trigger._tooltipEl) {
                trigger._tooltipEl.classList.remove('is-visible');
            }
        }
    };

    function showHint(message) {
        const hintEl = document.getElementById('actionHint');
        const hintContent = document.getElementById('hintContent');
        if (!hintEl || !hintContent) {
            return;
        }
        hintContent.textContent = message;
        hintEl.classList.add('active');
        if (window.hintTimer) {
            clearTimeout(window.hintTimer);
        }
        window.hintTimer = setTimeout(() => closeHint(), 5000);
    }

    function closeHint() {
        const hintEl = document.getElementById('actionHint');
        if (hintEl) {
            hintEl.classList.remove('active');
        }
        if (window.hintTimer) {
            clearTimeout(window.hintTimer);
            window.hintTimer = null;
        }
    }

    function showToast(message, variant = 'default') {
        ToastManager.show(message, variant);
    }

    function confirmAction(message, callback) {
        if (typeof callback !== 'function') {
            return;
        }
        if (window.confirm(message)) {
            callback();
        }
    }

    function getCSRFToken() {
        const tokenField = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return tokenField ? tokenField.value : '';
    }

    async function sendRequest(url, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        };
        const finalOptions = Object.assign({}, defaultOptions, options);
        if (options.headers) {
            finalOptions.headers = Object.assign({}, defaultOptions.headers, options.headers);
        }
        try {
            const response = await fetch(url, finalOptions);
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }
            const contentType = response.headers.get('content-type') || '';
            if (contentType.includes('application/json')) {
                return await response.json();
            }
            return await response.text();
        } catch (error) {
            console.error('Request error:', error);
            showToast('Request failed. Please try again shortly.', 'error');
            throw error;
        }
    }

    function showLoading(element, label = 'Working...') {
        if (!element) {
            return;
        }
        if (!element.dataset.originalContent) {
            element.dataset.originalContent = element.innerHTML;
        }
        element.innerHTML = `<span class="loading-spinner"></span>${label}`;
        element.classList.add('is-loading');
        element.setAttribute('aria-disabled', 'true');
        element.style.pointerEvents = 'none';
        if ('disabled' in element) {
            element.disabled = true;
        }
    }

    function hideLoading(element, fallbackLabel) {
        if (!element) {
            return;
        }
        const original = element.dataset.originalContent || fallbackLabel;
        if (original) {
            element.innerHTML = original;
        }
        element.classList.remove('is-loading');
        element.removeAttribute('aria-disabled');
        element.style.pointerEvents = '';
        if ('disabled' in element) {
            element.disabled = false;
        }
    }

    function validateForm(formId) {
        const form = document.getElementById(formId);
        if (!form) {
            return true;
        }
        let isValid = true;
        form.querySelectorAll('input[required], select[required], textarea[required]').forEach(field => {
            if (!field.value || !field.value.toString().trim()) {
                field.classList.add('invalid');
                isValid = false;
            } else {
                field.classList.remove('invalid');
            }
        });
        if (!isValid) {
            showToast('Please complete all required fields.', 'error');
        }
        return isValid;
    }

    function checkPasswordStrength(password) {
        const requirements = [
            { rule: /.{8,}/, message: 'Use at least 8 characters.' },
            { rule: /[A-Z]/, message: 'Add an uppercase letter.' },
            { rule: /[a-z]/, message: 'Add a lowercase letter.' },
            { rule: /\d/, message: 'Add a number.' },
            { rule: /[!@#$%^&*(),.?":{}|<>]/, message: 'Add a symbol.' }
        ];
        const feedback = [];
        let strength = 0;
        requirements.forEach(requirement => {
            if (requirement.rule.test(password)) {
                strength += 1;
            } else {
                feedback.push(requirement.message);
            }
        });
        return {
            strength,
            feedback,
            isStrong: strength >= 4
        };
    }

    function formatDate(value) {
        if (!value) {
            return '-';
        }
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) {
            return '-';
        }
        return `${date.toLocaleDateString()} ${date.toLocaleTimeString([], { hour12: false })}`;
    }

    function debounce(fn, wait) {
        let timeout;
        return function debounced(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => fn.apply(this, args), wait);
        };
    }

    function throttle(fn, limit) {
        let inThrottle = false;
        return function throttled(...args) {
            if (inThrottle) {
                return;
            }
            fn.apply(this, args);
            inThrottle = true;
            setTimeout(() => {
                inThrottle = false;
            }, limit);
        };
    }

    document.addEventListener('DOMContentLoaded', () => {
        window.hintTimer = null;
        ModalManager.init();
        ToastManager.init();
        TooltipManager.init();
    });

    window.UIKit = {
        ModalManager,
        ToastManager,
        TooltipManager
    };

    window.showToast = showToast;
    window.showHint = showHint;
    window.closeHint = closeHint;
    window.confirmAction = confirmAction;
    window.getCSRFToken = getCSRFToken;
    window.sendRequest = sendRequest;
    window.showLoading = showLoading;
    window.hideLoading = hideLoading;
    window.validateForm = validateForm;
    window.checkPasswordStrength = checkPasswordStrength;
    window.formatDate = formatDate;
    window.debounce = debounce;
    window.throttle = throttle;
})();
