// 用户管理JavaScript模块

// 全局变量
let currentUserId = null;
let currentUserGroup = '';
let currentUserName = '';
let hasChangeUserPerm = false;
let hasDeleteUserPerm = false;
let currentGroupId = null;

// 初始化函数
document.addEventListener('DOMContentLoaded', function() {
    // 初始化Materialize组件
    M.AutoInit();
    
    // 初始化模态框
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
    
    // 初始化表单选择器
    var selects = document.querySelectorAll('select');
    var selectInstances = M.FormSelect.init(selects);
    
    // 绑定表格行事件
    bindTableRowEvents();
    
    // 绑定菜单切换事件
    bindMenuToggleEvents();
    
    // 显示默认视图
    showUserList(document.querySelector('.collection-item[data-view="userListView"]'));
    
    // 首次访问提示
    if (!localStorage.getItem('hasVisitedBefore')) {
        setTimeout(() => {
            showHint('欢迎使用系统！点击侧边栏菜单项可切换不同功能界面。');
            localStorage.setItem('hasVisitedBefore', 'true');
        }, 1000);
    }
    
    // 绑定密码输入事件
    bindPasswordEvents();
});

// 绑定表格行事件
function bindTableRowEvents() {
    document.querySelectorAll('tbody tr').forEach(tr => {
        tr.addEventListener('mouseenter', function() {
            this.classList.add('hovered');
        });
        tr.addEventListener('mouseleave', function() {
            this.classList.remove('hovered');
        });
    });
}

// 绑定菜单切换事件
function bindMenuToggleEvents() {
    const menuToggle = document.getElementById('menuToggle');
    const sideNav = document.getElementById('sideNav');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sideNav.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }
    
    const main = document.querySelector('main');
    if (main && window.innerWidth < 992) {
        main.addEventListener('click', function() {
            sideNav.classList.remove('active');
            if (menuToggle) {
                menuToggle.classList.remove('active');
            }
        });
    }
}

// 绑定密码输入事件
function bindPasswordEvents() {
    const passwordInput = document.getElementById('newPassword');
    if (passwordInput) {
        passwordInput.addEventListener('input', debounce(function() {
            const password = this.value;
            if (password.length > 0) {
                const strength = checkPasswordStrength(password);
                let feedback = '密码强度: ';
                if (strength.strength <= 2) {
                    feedback += '弱';
                } else if (strength.strength <= 3) {
                    feedback += '中';
                } else {
                    feedback += '强';
                }
                // 可以在这里显示密码强度提示
            }
        }, 300));
    }
}

// 显示用户列表
function showUserList(element) {
    document.getElementById('userListView').style.display = 'block';
    document.getElementById('groupListView').style.display = 'none';
    
    updateMenuActiveState(element);
    
    if (window.innerWidth < 992) {
        document.getElementById('sideNav').classList.remove('active');
        document.getElementById('menuToggle').classList.remove('active');
    }
    
    // 添加淡入动画
    document.getElementById('userListView').classList.add('fade-in-up');
}

// 显示用户组列表
function showGroupList(element) {
    document.getElementById('userListView').style.display = 'none';
    document.getElementById('groupListView').style.display = 'block';
    
    updateMenuActiveState(element);
    
    if (window.innerWidth < 992) {
        document.getElementById('sideNav').classList.remove('active');
        document.getElementById('menuToggle').classList.remove('active');
    }
    
    // 添加淡入动画
    document.getElementById('groupListView').classList.add('fade-in-up');
}

// 更新菜单激活状态
function updateMenuActiveState(element) {
    document.querySelectorAll('.collection-item').forEach(item => {
        item.classList.remove('active');
    });
    
    if (element) {
        element.classList.add('active');
    }
}

// 显示创建用户模态框
function showCreateUserModal() {
    document.getElementById('userModalTitle').textContent = '新增用户';
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';

    document.getElementById('password').setAttribute('required', 'required');
    document.getElementById('passwordGroup').classList.add('required-field');
    
    M.updateTextFields();
    M.FormSelect.init(document.querySelectorAll('select'));
    M.Modal.getInstance(document.getElementById('userModal')).open();
    
    setTimeout(() => {
        document.getElementById('username').focus();
    }, 300);
}

// 显示编辑用户模态框
function showEditUserModal(userId) {
    document.getElementById('userModalTitle').textContent = '编辑用户';
    
    showToast('正在加载用户信息...', 'rounded blue');
    
    sendRequest(`/users/${userId}/`)
        .then(data => {
            document.getElementById('userId').value = userId;
            document.getElementById('username').value = data.username;
            document.getElementById('email').value = data.email || '';
            document.getElementById('userGroup').value = data.group_id || '';
            document.getElementById('isActive').checked = data.is_active;
            
            document.getElementById('password').removeAttribute('required');
            document.getElementById('passwordGroup').classList.remove('required-field');
            
            M.updateTextFields();
            M.FormSelect.init(document.querySelectorAll('select'));
            M.Modal.getInstance(document.getElementById('userModal')).open();
        })
        .catch(error => {
            showToast('加载用户信息失败', 'rounded red');
            console.error('错误:', error);
        });
}

// 保存用户
function saveUser() {
    // 验证表单
    if (!validateForm('userForm')) {
        return;
    }
    
    const saveBtn = document.querySelector('#userModal .modal-footer .btn');
    const originalText = saveBtn.innerHTML;
    showLoading(saveBtn);
    
    const userId = document.getElementById('userId').value;
    const data = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        group_id: document.getElementById('userGroup').value,
        is_active: document.getElementById('isActive').checked
    };

    const password = document.getElementById('password').value;
    if (password) {
        data.password = password;
    }

    const url = userId ? `/users/${userId}/update/` : '/users/create/';
    sendRequest(url, {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(data => {
        if (data.status === 'success') {
            M.Modal.getInstance(document.getElementById('userModal')).close();
            showToast('操作成功', 'rounded green');
            showHint(userId ? '用户信息已更新成功' : '新用户创建成功');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showToast(data.message, 'rounded red');
        }
    })
    .catch(error => {
        console.error('保存失败:', error);
        showToast('保存失败，请稍后重试', 'rounded red');
    })
    .finally(() => {
        hideLoading(saveBtn, originalText);
    });
}

// 删除用户
function deleteUser(userId) {
    const userRow = document.querySelector(`tr[data-user-id="${userId}"]`);
    const username = userRow ? userRow.querySelector('td:first-child').textContent : '该用户';
    
    confirmAction(`确定要删除用户【${username}】吗？此操作不可恢复！`, () => {
        const deleteBtn = event.target;
        const originalText = deleteBtn ? deleteBtn.innerHTML : '';
        if (deleteBtn) showLoading(deleteBtn);
        
        sendRequest(`/users/${userId}/delete/`, {
            method: 'POST'
            })
        .then(data => {
            if (data.status === 'success') {
                showToast('删除成功', 'rounded green');
                showHint('用户已成功删除');
                if (userRow) {
                    userRow.style.animation = 'fadeOut 0.3s ease-out';
                    setTimeout(() => {
                        userRow.remove();
                    }, 300);
                }
            } else {
                showToast(data.message, 'rounded red');
            }
        })
        .catch(error => {
            console.error('删除失败:', error);
            showToast('删除失败，请稍后重试', 'rounded red');
        })
        .finally(() => {
            if (deleteBtn) hideLoading(deleteBtn, originalText);
        });
    });
}

// 显示修改密码模态框
function showChangePasswordModal(userId) {
    document.getElementById('passwordUserId').value = userId;
    document.getElementById('passwordForm').reset();
    
    const oldPasswordGroup = document.getElementById('oldPasswordGroup');
    if (oldPasswordGroup) {
        oldPasswordGroup.style.display = (userId == currentUserId) ? 'block' : 'none';
    }
    
    M.Modal.getInstance(document.getElementById('passwordModal')).open();
    
    setTimeout(() => {
        document.getElementById('newPassword').focus();
    }, 300);
}

// 保存密码
function savePassword() {
    // 验证表单
    if (!validateForm('passwordForm')) {
        return;
    }
    
    const saveBtn = document.querySelector('#passwordModal .modal-footer .btn');
    const originalText = saveBtn.innerHTML;
    showLoading(saveBtn);
    
    const userId = document.getElementById('passwordUserId').value;
    const data = {
        new_password: document.getElementById('newPassword').value
    };
    
    const oldPasswordInput = document.getElementById('oldPassword');
    if (oldPasswordInput && oldPasswordInput.parentElement.style.display !== 'none') {
        data.old_password = oldPasswordInput.value;
    }

    sendRequest(`/users/${userId}/change-password/`, {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(data => {
        if (data.status === 'success') {
            M.Modal.getInstance(document.getElementById('passwordModal')).close();
            showToast('密码修改成功', 'rounded green');
            showHint('密码已成功修改');
        } else {
            showToast(data.message, 'rounded red');
        }
    })
    .catch(error => {
        console.error('修改密码失败:', error);
        showToast('修改密码失败，请稍后重试', 'rounded red');
    })
    .finally(() => {
        hideLoading(saveBtn, originalText);
    });
}

// 显示用户组成员
function showGroupMembers(groupId) {
    currentGroupId = groupId;
    
    showToast('正在加载成员信息...', 'rounded blue');
    
    sendRequest(`/groups/${groupId}/members/`)
        .then(data => {
            document.getElementById('groupMembersModalTitle').textContent = `${data.group_name} - 成员列表`;
            const tbody = document.getElementById('groupMembersTableBody');
            tbody.innerHTML = '';
            
            data.members.forEach(member => {
                const tr = document.createElement('tr');
                const currentUserGroup = '{{ user.groups.all.0.name }}';
                const currentUserName = '{{ user.username }}';
                const canManageUser = (
                    (currentUserGroup === '超级管理员' && member.username !== currentUserName) ||
                    (currentUserGroup === '管理员' && data.group_name === '普通用户' && member.username !== currentUserName)
                );
                
                tr.innerHTML = `
                    <td>${member.username}</td>
                    <td>${member.email || '-'}</td>
                    <td>
                        <span class="badge ${member.is_active ? 'active' : 'inactive'}">
                            ${member.is_active ? '正常' : '禁用'}
                        </span>
                    </td>
                    <td>
                        ${canManageUser ? 
                            `<a class="waves-effect waves-light btn-small red" onclick="removeUserFromGroup(${member.id})">
                                <i class="material-icons">person_remove</i>
                            </a>` : ''}
                    </td>
                `;
                tbody.appendChild(tr);
            });
            
            const addUserSection = document.querySelector('#groupMembersModal .row');
            if (addUserSection) {
                const canManageGroup = (
                    '{{ user.groups.all.0.name }}' === '超级管理员' ||
                    ('{{ user.groups.all.0.name }}' === '管理员' && data.group_name === '普通用户')
                );
                addUserSection.style.display = canManageGroup ? 'block' : 'none';
                
                if (canManageGroup) {
                    sendRequest('/users/available-for-group/' + groupId)
                        .then(data => {
                            const select = document.getElementById('userToAdd');
                            select.innerHTML = '<option value="">选择用户...</option>';
                            data.users.forEach(user => {
                                select.innerHTML += `<option value="${user.id}">${user.username}</option>`;
                            });
                            M.FormSelect.init(select);
                        });
                }
            }
            
            M.Modal.getInstance(document.getElementById('groupMembersModal')).open();
        })
        .catch(error => {
            console.error('加载成员信息失败:', error);
            showToast('加载成员信息失败', 'rounded red');
        });
}

// 添加用户到组
function addUserToGroup() {
    const userId = document.getElementById('userToAdd').value;
    if (!userId) {
        showToast('请选择用户', 'rounded red');
        return;
    }
    
    const addBtn = event.target;
    const originalText = addBtn.innerHTML;
    showLoading(addBtn);

    sendRequest(`/users/${userId}/change-group/`, {
        method: 'POST',
        body: JSON.stringify({
            group_id: currentGroupId
        })
    })
    .then(data => {
        if (data.status === 'success') {
            showToast('添加成功', 'rounded green');
            showHint('用户已成功添加到组');
            showGroupMembers(currentGroupId);
        } else {
            showToast(data.message, 'rounded red');
        }
    })
    .catch(error => {
        console.error('添加失败:', error);
        showToast('添加失败，请稍后重试', 'rounded red');
    })
    .finally(() => {
        hideLoading(addBtn, originalText);
    });
}

// 从组中移除用户
function removeUserFromGroup(userId) {
    confirmAction('确定要将此用户从组中移除吗？', () => {
        const removeBtn = event.target;
        const originalText = removeBtn.innerHTML;
        showLoading(removeBtn);
        
        sendRequest(`/users/${userId}/change-group/`, {
            method: 'POST',
            body: JSON.stringify({
                group_id: null
            })
        })
        .then(data => {
            if (data.status === 'success') {
                showToast('移除成功', 'rounded green');
                showHint('用户已成功从组中移除');
                showGroupMembers(currentGroupId);
            } else {
                showToast(data.message, 'rounded red');
            }
        })
        .catch(error => {
            console.error('移除失败:', error);
            showToast('移除失败，请稍后重试', 'rounded red');
        })
        .finally(() => {
            hideLoading(removeBtn, originalText);
        });
    });
}

// 刷新用户列表
function refreshUserList() {
    const refreshBtn = event.target;
    const originalText = refreshBtn.innerHTML;
    showLoading(refreshBtn);
    
    sendRequest('/users/api/')
        .then(data => {
            const tbody = document.getElementById('userTableBody');
            tbody.innerHTML = '';
            
            data.users.forEach(user => {
                const tr = document.createElement('tr');
                tr.setAttribute('data-user-id', user.id);
                let btnHtml = '';
                
                if (hasChangeUserPerm) {
                    btnHtml += `<a class="waves-effect waves-light btn-small" onclick="showEditUserModal(${user.id})">
                        <i class="material-icons">edit</i>
                    </a>
                    <a class="waves-effect waves-light btn-small orange" onclick="showChangePasswordModal(${user.id})">
                        <i class="material-icons">lock</i>
                    </a>`;
                }
                
                if (hasDeleteUserPerm && user.id != currentUserId) {
                    btnHtml += `<a class="waves-effect waves-light btn-small red" onclick="deleteUser(${user.id})">
                        <i class="material-icons">delete</i>
                    </a>`;
                }
                
                tr.innerHTML = `
                    <td>${user.username}</td>
                    <td>${user.email || '-'}</td>
                    <td>${user.group_name || '无'}</td>
                    <td>
                        <span class="badge ${user.is_active ? 'active' : 'inactive'}">
                            ${user.is_active ? '正常' : '禁用'}
                        </span>
                    </td>
                    <td>${btnHtml}</td>
                `;
                tbody.appendChild(tr);
            });
            
            showToast('列表刷新成功', 'rounded green');
            showHint('用户列表已刷新');
        })
        .catch(error => {
            console.error('刷新失败:', error);
            showToast('刷新列表失败，请稍后重试', 'rounded red');
        })
        .finally(() => {
            hideLoading(refreshBtn, originalText);
        });
}

// 保存用户组成员
function saveGroupMembers() {
    showToast('正在保存...', 'rounded blue');
    // 这里可以添加保存逻辑
    setTimeout(() => {
        M.Modal.getInstance(document.getElementById('groupMembersModal')).close();
        showToast('保存成功', 'rounded green');
    }, 1000);
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