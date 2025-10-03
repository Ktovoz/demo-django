// 全局JavaScript工具函数

// 初始化Materialize组件
document.addEventListener('DOMContentLoaded', function() {
    M.AutoInit();
});

// 显示提示信息
function showToast(message, classes = 'rounded') {
    M.toast({html: message, classes: classes});
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
        return await response.json();
    } catch (error) {
        console.error('请求失败:', error);
        showToast('请求失败，请稍后重试', 'rounded red');
        throw error;
    }
}