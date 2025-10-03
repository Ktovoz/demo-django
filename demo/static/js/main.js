// 全局JavaScript工具函数

// 初始化Materialize组件
document.addEventListener('DOMContentLoaded', function() {
    M.AutoInit();
    
    // 初始化所有模态框
    var modals = document.querySelectorAll('.modal');
    M.Modal.init(modals);
    
    // 初始化所有选择框
    var selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);
    
    // 初始化所有工具提示
    var tooltips = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltips);
});

// 显示提示信息
function showToast(message, classes = 'rounded') {
    M.toast({html: message, classes: classes, displayLength: 3000});
}

// 显示操作提示
function showHint(message) {
    const hintEl = document.getElementById('actionHint');
    if (hintEl) {
        document.getElementById('hintContent').textContent = message;
        hintEl.classList.add('show');
        
        // 5秒后自动关闭
        setTimeout(() => {
            closeHint();
        }, 5000);
    }
}

// 关闭操作提示
function closeHint() {
    const hintEl = document.getElementById('actionHint');
    if (hintEl) {
        hintEl.classList.remove('show');
    }
}

// 确认对话框
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// 获取CSRF令牌
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// 发送AJAX请求的通用函数
async function sendRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    };
    
    const finalOptions = Object.assign(defaultOptions, options);
    
    try {
        const response = await fetch(url, finalOptions);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('请求失败:', error);
        showToast('请求失败，请稍后重试', 'rounded red');
        throw error;
    }
}

// 显示加载动画
function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="loading-spinner"></div>处理中...';
        element.disabled = true;
    }
}

// 隐藏加载动画
function hideLoading(element, originalText) {
    if (element && originalText) {
        element.innerHTML = originalText;
        element.disabled = false;
    }
}

// 表单验证
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('invalid');
            showToast('请填写所有必填字段', 'rounded red');
        } else {
            input.classList.remove('invalid');
        }
    });
    
    return isValid;
}

// 密码强度检查
function checkPasswordStrength(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    let strength = 0;
    let feedback = [];
    
    if (password.length >= minLength) strength++;
    else feedback.push('至少8个字符');
    
    if (hasUpperCase) strength++;
    else feedback.push('包含大写字母');
    
    if (hasLowerCase) strength++;
    else feedback.push('包含小写字母');
    
    if (hasNumbers) strength++;
    else feedback.push('包含数字');
    
    if (hasSpecialChar) strength++;
    else feedback.push('包含特殊字符');
    
    return {
        strength: strength,
        feedback: feedback,
        isStrong: strength >= 4
    };
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', {hour12: false});
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}