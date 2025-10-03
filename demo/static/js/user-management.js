// Behaviour for the user management dashboard
(function () {
    const dashboardState = window.dashboardState || {};
    const state = {
        currentUserId: Number(dashboardState.currentUserId) || null,
        currentUserGroup: dashboardState.currentUserGroup || '',
        currentUserName: dashboardState.currentUserName || '',
        canChangeUser: !!dashboardState.canChangeUser,
        canDeleteUser: !!dashboardState.canDeleteUser,
        canChangeGroup: !!dashboardState.canChangeGroup,
        activeView: 'userListView',
        activeGroupId: null,
        lastModalId: null
    };

    document.addEventListener('DOMContentLoaded', () => {
        const initialTrigger = document.querySelector('.menu-item-trigger.active') || document.querySelector('.menu-item-trigger');
        if (initialTrigger) {
            state.activeView = initialTrigger.getAttribute('data-target') || 'userListView';
        }
        bindTableRowEffects();
        bindMenuToggle();
        bindPasswordStrengthMeter();
        initViewSwitching();
        setupSearch();
        bindGlobalActions();
        showDefaultHint();
        switchView(state.activeView);
    });

    function bindTableRowEffects() {
        document.querySelectorAll('table.highlight tbody tr').forEach(row => {
            row.addEventListener('mouseenter', () => row.classList.add('hovered'));
            row.addEventListener('mouseleave', () => row.classList.remove('hovered'));
            row.addEventListener('click', event => {
                if (event.target.closest('a, button, .btn, .btn-small')) {
                    return;
                }
                document.querySelectorAll('table.highlight tbody tr.selected').forEach(activeRow => {
                    if (activeRow !== row) {
                        activeRow.classList.remove('selected');
                    }
                });
                row.classList.toggle('selected');
            });
        });
    }

    function bindMenuToggle() {
        const trigger = document.getElementById('menuToggle');
        const sideNav = document.getElementById('sideNav');
        const main = document.querySelector('main');
        if (!trigger || !sideNav) {
            return;
        }
        trigger.addEventListener('click', () => {
            sideNav.classList.toggle('active');
            trigger.classList.toggle('active');
        });
        if (main) {
            main.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    sideNav.classList.remove('active');
                    trigger.classList.remove('active');
                }
            });
        }
    }

    function bindPasswordStrengthMeter() {
        const trackedInputs = ['newPassword', 'password'].map(id => document.getElementById(id)).filter(Boolean);
        trackedInputs.forEach(input => {
            input.addEventListener('input', debounce(() => {
                const value = input.value || '';
                if (!value.length) {
                    return;
                }
                const report = checkPasswordStrength(value);
                if (report.isStrong) {
                    showHint('Strong password detected.');
                } else if (report.feedback.length) {
                    showHint(report.feedback[0]);
                }
            }, 280));
        });
    }

    function initViewSwitching() {
        document.querySelectorAll('.view-toggle').forEach(toggle => {
            toggle.addEventListener('click', () => {
                switchView(toggle.getAttribute('data-view'));
            });
        });
    }

    function setupSearch() {
        const input = document.getElementById('userSearchInput');
        if (!input) {
            return;
        }
        input.addEventListener('input', debounce(() => {
            filterUserTable(input.value);
        }, 200));
    }

    function bindGlobalActions() {
        document.addEventListener('click', handleActionClick);
    }

    function handleActionClick(event) {
        const trigger = event.target.closest('[data-action]');
        if (!trigger || trigger.getAttribute('aria-disabled') === 'true') {
            return;
        }
        const action = trigger.getAttribute('data-action');
        switch (action) {
            case 'switch-view':
                event.preventDefault();
                switchView(trigger.getAttribute('data-target') || 'userListView');
                const sideNav = document.getElementById('sideNav');
                const menuToggle = document.getElementById('menuToggle');
                if (sideNav && menuToggle && window.innerWidth < 992) {
                    sideNav.classList.remove('active');
                    menuToggle.classList.remove('active');
                }
                break;
            case 'open-create-user':
                event.preventDefault();
                showCreateUserModal();
                break;
            case 'refresh-users':
                event.preventDefault();
                refreshUserList(trigger);
                break;
            case 'dismiss-hint':
                event.preventDefault();
                closeHint();
                break;
            case 'edit-user':
                event.preventDefault();
                showEditUserModal(trigger.getAttribute('data-user-id'));
                break;
            case 'reset-password':
                event.preventDefault();
                showChangePasswordModal(trigger.getAttribute('data-user-id'));
                break;
            case 'delete-user':
                event.preventDefault();
                deleteUser(trigger, trigger.getAttribute('data-user-id'));
                break;
            case 'show-group-members':
                event.preventDefault();
                showGroupMembers(trigger.getAttribute('data-group-id'));
                break;
            case 'save-user':
                event.preventDefault();
                saveUser(trigger);
                break;
            case 'save-password':
                event.preventDefault();
                savePassword(trigger);
                break;
            case 'add-user-to-group':
                event.preventDefault();
                addUserToGroup(trigger);
                break;
            case 'save-group-members':
                event.preventDefault();
                saveGroupMembers(trigger);
                break;
            case 'remove-user-from-group':
                event.preventDefault();
                removeUserFromGroup(trigger, trigger.getAttribute('data-user-id'));
                break;
            default:
                break;
        }
    }

    function showDefaultHint() {
        if (!window.localStorage) {
            return;
        }
        const key = 'userConsoleOnboarding';
        if (!localStorage.getItem(key)) {
            setTimeout(() => {
                showHint('Use the view toggles to switch between users and groups.');
            }, 800);
            localStorage.setItem(key, 'seen');
        }
    }

    function switchView(viewName) {
        const userView = document.getElementById('userListView');
        const groupView = document.getElementById('groupListView');
        if (!userView || !groupView) {
            return;
        }
        const targetView = viewName === 'groupListView' ? 'groupListView' : 'userListView';
        const isUserView = targetView === 'userListView';
        state.activeView = targetView;
        userView.style.display = isUserView ? 'block' : 'none';
        groupView.style.display = isUserView ? 'none' : 'block';
        userView.classList.toggle('hidden', !isUserView);
        groupView.classList.toggle('hidden', isUserView);
        userView.setAttribute('aria-hidden', isUserView ? 'false' : 'true');
        groupView.setAttribute('aria-hidden', isUserView ? 'true' : 'false');
        (isUserView ? userView : groupView).classList.add('fade-in-up');
        updateMenuActiveState(state.activeView);
        syncViewPills(state.activeView);
    }

    function updateMenuActiveState(viewName) {
        document.querySelectorAll('.menu-item-trigger').forEach(button => {
            const target = button.getAttribute('data-target') || 'userListView';
            const isActive = target === viewName;
            button.classList.toggle('active', isActive);
            button.setAttribute('aria-pressed', isActive ? 'true' : 'false');
            const container = button.closest('.collection-item');
            if (container) {
                container.classList.toggle('is-active', isActive);
            }
        });
    }

    function syncViewPills(viewName) {
        document.querySelectorAll('.view-toggle').forEach(toggle => {
            const isActive = toggle.getAttribute('data-view') === viewName;
            toggle.classList.toggle('active', isActive);
            toggle.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });
    }

    function filterUserTable(keyword) {
        const rows = document.querySelectorAll('#userTableBody tr');
        if (!rows.length) {
            return;
        }
        const normalized = (keyword || '').trim().toLowerCase();
        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            const visible = !normalized || text.includes(normalized);
            row.style.display = visible ? '' : 'none';
        });
    }

    function showCreateUserModal() {
        const form = document.getElementById('userForm');
        if (!form) {
            return;
        }
        form.reset();
        form.querySelector('#userId').value = '';
        const passwordInput = form.querySelector('#password');
        passwordInput.required = true;
        passwordInput.value = '';
        form.querySelector('#passwordGroup').classList.add('required-field');
        const groupSelect = form.querySelector('#userGroup');
        if (groupSelect) {
            groupSelect.value = '';
        }
        setModalTitle('userModalTitle', 'Add user');
        openModal('userModal', '#username');
    }

    function setModalTitle(id, text) {
        const el = document.getElementById(id);
        if (el) {
            el.textContent = text;
        }
    }

    function openModal(id, focusSelector) {
        const focusTarget = focusSelector ? document.querySelector(focusSelector) : null;
        if (window.UIKit && UIKit.ModalManager && typeof UIKit.ModalManager.open === 'function') {
            UIKit.ModalManager.open(id);
        } else {
            const modal = document.getElementById(id);
            if (modal) {
                modal.classList.add('is-open');
                modal.setAttribute('aria-hidden', 'false');
                document.body.classList.add('has-open-modal');
                state.lastModalId = id;
            }
        }
        if (focusTarget) {
            setTimeout(() => {
                focusTarget.focus();
            }, 160);
        }
        state.lastModalId = id;
    }

    function closeActiveModal() {
        if (window.UIKit && UIKit.ModalManager && typeof UIKit.ModalManager.close === 'function') {
            UIKit.ModalManager.close();
        } else if (state.lastModalId) {
            const modal = document.getElementById(state.lastModalId);
            if (modal) {
                modal.classList.remove('is-open');
                modal.setAttribute('aria-hidden', 'true');
            }
            document.body.classList.remove('has-open-modal');
        }
        state.lastModalId = null;
    }

    function showEditUserModal(userId) {
        if (!userId) {
            return;
        }
        setModalTitle('userModalTitle', 'Edit user');
        showToast('Loading user details...', 'success');
        sendRequest(`/users/${userId}/`).then(data => {
            const form = document.getElementById('userForm');
            if (!form || !data) {
                return;
            }
            form.querySelector('#userId').value = userId;
            form.querySelector('#username').value = data.username || '';
            form.querySelector('#email').value = data.email || '';
            form.querySelector('#isActive').checked = data.is_active !== false;
            const groupSelect = form.querySelector('#userGroup');
            if (groupSelect) {
                groupSelect.value = data.group_id || '';
            }
            const passwordInput = form.querySelector('#password');
            passwordInput.value = '';
            passwordInput.required = false;
            form.querySelector('#passwordGroup').classList.remove('required-field');
            openModal('userModal', '#username');
        }).catch(() => {
            showToast('Unable to load user details.', 'error');
        });
    }

    function saveUser(trigger) {
        if (!validateForm('userForm')) {
            return;
        }
        const form = document.getElementById('userForm');
        const saveButton = trigger || document.querySelector('#userModal .modal-footer .btn');
        const originalLabel = saveButton ? saveButton.innerHTML : '';
        if (saveButton) {
            showLoading(saveButton, 'Saving...');
        }

        const payload = {
            username: form.querySelector('#username').value,
            email: form.querySelector('#email').value,
            group_id: form.querySelector('#userGroup').value || null,
            is_active: form.querySelector('#isActive').checked
        };
        const password = form.querySelector('#password').value;
        if (password) {
            payload.password = password;
        }
        const userId = form.querySelector('#userId').value;
        const url = userId ? `/users/${userId}/update/` : '/users/create/';

        sendRequest(url, {
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(data => {
            if (data && data.status === 'success') {
                closeActiveModal();
                showToast('User saved.', 'success');
                showHint(userId ? 'The account was updated.' : 'New account created.');
                setTimeout(() => window.location.reload(), 900);
            } else {
                showToast(data && data.message ? data.message : 'Save failed.', 'error');
            }
        }).catch(() => {
            showToast('Save failed. Please retry.', 'error');
        }).finally(() => {
            if (saveButton) {
                hideLoading(saveButton, originalLabel);
            }
        });
    }

    function deleteUser(trigger, userId) {
        if (!userId) {
            return;
        }
        const row = document.querySelector(`tr[data-user-id="${userId}"]`);
        const username = row ? row.querySelector('.cell-title').textContent : 'this user';
        confirmAction(`Delete ${username}? This cannot be undone.`, () => {
            const button = trigger || null;
            const originalLabel = button ? button.innerHTML : '';
            if (button) {
                showLoading(button, 'Deleting...');
            }
            sendRequest(`/users/${userId}/delete/`, { method: 'POST' }).then(data => {
                if (data && data.status === 'success') {
                    showToast('User removed.', 'success');
                    showHint('The account was deleted from the directory.');
                    if (row) {
                        row.classList.add('fade-out');
                        setTimeout(() => row.remove(), 260);
                    }
                } else {
                    showToast(data && data.message ? data.message : 'Delete failed.', 'error');
                }
            }).catch(() => {
                showToast('Delete failed. Please retry.', 'error');
            }).finally(() => {
                if (button) {
                    hideLoading(button, originalLabel);
                }
            });
        });
    }

    function showChangePasswordModal(userId) {
        const form = document.getElementById('passwordForm');
        if (!form) {
            return;
        }
        form.reset();
        form.querySelector('#passwordUserId').value = userId;
        const oldPasswordGroup = document.getElementById('oldPasswordGroup');
        if (oldPasswordGroup) {
            const isSelf = Number(userId) === state.currentUserId;
            oldPasswordGroup.style.display = isSelf ? 'block' : 'none';
            const input = oldPasswordGroup.querySelector('input');
            if (input) {
                input.required = isSelf;
            }
        }
        setModalTitle('passwordModalTitle', 'Reset password');
        openModal('passwordModal', '#newPassword');
    }

    function savePassword(trigger) {
        if (!validateForm('passwordForm')) {
            return;
        }
        const form = document.getElementById('passwordForm');
        const userId = form.querySelector('#passwordUserId').value;
        const saveButton = trigger || document.querySelector('#passwordModal .modal-footer .btn');
        const originalLabel = saveButton ? saveButton.innerHTML : '';
        if (saveButton) {
            showLoading(saveButton, 'Saving...');
        }

        const payload = {
            new_password: form.querySelector('#newPassword').value
        };
        const oldGroup = document.getElementById('oldPasswordGroup');
        if (oldGroup && oldGroup.style.display !== 'none') {
            payload.old_password = form.querySelector('#oldPassword').value;
        }
        sendRequest(`/users/${userId}/change-password/`, {
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(data => {
            if (data && data.status === 'success') {
                closeActiveModal();
                showToast('Password updated.', 'success');
                showHint('Password has been changed successfully.');
            } else {
                showToast(data && data.message ? data.message : 'Update failed.', 'error');
            }
        }).catch(() => {
            showToast('Update failed. Please retry.', 'error');
        }).finally(() => {
            if (saveButton) {
                hideLoading(saveButton, originalLabel);
            }
        });
    }

    function showGroupMembers(groupId) {
        if (!groupId) {
            return;
        }
        state.activeGroupId = groupId;
        showToast('Loading members...', 'success');
        sendRequest(`/groups/${groupId}/members/`).then(data => {
            renderGroupMembers(data);
            openModal('groupMembersModal');
        }).catch(() => {
            showToast('Unable to load group members.', 'error');
        });
    }

    function renderGroupMembers(data) {
        const title = document.getElementById('groupMembersModalTitle');
        const body = document.getElementById('groupMembersTableBody');
        if (!body) {
            return;
        }
        body.innerHTML = '';
        const groupName = data && data.group_name ? data.group_name : 'Group';
        if (title) {
            title.textContent = `${groupName} members`;
        }
        (data && data.members ? data.members : []).forEach(member => {
            const row = document.createElement('tr');
            const canManage = state.canChangeUser && member.id !== state.currentUserId;
            let actionHtml = '';
            if (canManage) {
                actionHtml = `<button type="button" class="waves-effect waves-light btn-small red" data-action="remove-user-from-group" data-user-id="${member.id}"><i class="material-icons">person_remove</i></button>`;
            }
            row.innerHTML = '' +
                `<td>${escapeHtml(member.username)}</td>` +
                `<td>${escapeHtml(member.email || '-')}</td>` +
                `<td><span class="badge ${member.is_active ? 'active' : 'inactive'}">${member.is_active ? 'Active' : 'Suspended'}</span></td>` +
                `<td>${actionHtml}</td>`;
            body.appendChild(row);
        });
        const addRow = document.querySelector('#groupMembersModal .row');
        if (addRow) {
            addRow.style.display = state.canChangeUser ? 'block' : 'none';
        }
        if (state.canChangeUser) {
            sendRequest(`/users/available-for-group/${state.activeGroupId}`).then(payload => {
                populateUserOptions(payload && payload.users ? payload.users : []);
            });
        }
    }

    function populateUserOptions(users) {
        const select = document.getElementById('userToAdd');
        if (!select) {
            return;
        }
        select.innerHTML = '<option value="">Select a user...</option>';
        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user.id;
            option.textContent = user.username;
            select.appendChild(option);
        });
    }

    function addUserToGroup(trigger) {
        const select = document.getElementById('userToAdd');
        if (!select || !select.value) {
            showToast('Choose a user to add.', 'error');
            return;
        }
        const button = trigger || null;
        const originalLabel = button ? button.innerHTML : '';
        if (button) {
            showLoading(button, 'Adding...');
        }
        sendRequest(`/users/${select.value}/change-group/`, {
            method: 'POST',
            body: JSON.stringify({ group_id: state.activeGroupId })
        }).then(data => {
            if (data && data.status === 'success') {
                showToast('Member added.', 'success');
                showHint('The user has been added to the group.');
                showGroupMembers(state.activeGroupId);
            } else {
                showToast(data && data.message ? data.message : 'Operation failed.', 'error');
            }
        }).catch(() => {
            showToast('Operation failed. Please retry.', 'error');
        }).finally(() => {
            if (button) {
                hideLoading(button, originalLabel);
            }
        });
    }

    function removeUserFromGroup(trigger, userId) {
        if (!userId) {
            return;
        }
        confirmAction('Remove this member from the group?', () => {
            const button = trigger || null;
            const originalLabel = button ? button.innerHTML : '';
            if (button) {
                showLoading(button, 'Removing...');
            }
            sendRequest(`/users/${userId}/change-group/`, {
                method: 'POST',
                body: JSON.stringify({ group_id: null })
            }).then(data => {
                if (data && data.status === 'success') {
                    showToast('Member removed.', 'success');
                    showGroupMembers(state.activeGroupId);
                } else {
                    showToast(data && data.message ? data.message : 'Operation failed.', 'error');
                }
            }).catch(() => {
                showToast('Operation failed. Please retry.', 'error');
            }).finally(() => {
                if (button) {
                    hideLoading(button, originalLabel);
                }
            });
        });
    }

    function refreshUserList(trigger) {
        const button = trigger || null;
        const originalLabel = button ? button.innerHTML : '';
        if (button) {
            showLoading(button, 'Refreshing...');
        }
        sendRequest('/users/api/').then(data => {
            const body = document.getElementById('userTableBody');
            if (!body || !data || !data.users) {
                return;
            }
            body.innerHTML = '';
            data.users.forEach(user => body.appendChild(renderUserRow(user)));
            bindTableRowEffects();
            const searchInput = document.getElementById('userSearchInput');
            if (searchInput && searchInput.value.trim()) {
                filterUserTable(searchInput.value);
            }
            showToast('Directory updated.', 'success');
            showHint('The latest account list is now visible.');
        }).catch(() => {
            showToast('Refresh failed. Please retry.', 'error');
        }).finally(() => {
            if (button) {
                hideLoading(button, originalLabel);
            }
        });
    }

    function renderUserRow(user) {
        const row = document.createElement('tr');
        row.setAttribute('data-user-id', user.id);
        const fullName = user.full_name || 'Name not provided';
        const groupName = user.group_name || 'Unassigned';
        let actions = '';
        if (state.canChangeUser) {
            actions += `<button type="button" class="waves-effect waves-light btn-small" data-action="edit-user" data-user-id="${user.id}" title="Edit user"><i class="material-icons">edit</i></button>`;
            actions += `<button type="button" class="waves-effect waves-light btn-small orange" data-action="reset-password" data-user-id="${user.id}" title="Reset password"><i class="material-icons">lock</i></button>`;
        }
        if (state.canDeleteUser && Number(user.id) !== state.currentUserId) {
            actions += `<button type="button" class="waves-effect waves-light btn-small red" data-action="delete-user" data-user-id="${user.id}" title="Delete user"><i class="material-icons">delete</i></button>`;
        }
        row.innerHTML = '' +
            `<td><div class="table-cell-primary"><span class="cell-title">${escapeHtml(user.username)}</span>` +
            `<span class="cell-subtitle">${escapeHtml(fullName)}</span></div></td>` +
            `<td>${escapeHtml(user.email || '-')}</td>` +
            `<td>${escapeHtml(groupName)}</td>` +
            `<td><span class="badge ${user.is_active ? 'active' : 'inactive'}">${user.is_active ? 'Active' : 'Suspended'}</span></td>` +
            `<td class="align-right"><div class="table-actions">${actions}</div></td>`;
        return row;
    }

    function saveGroupMembers() {
        showToast('Changes saved locally.', 'success');
        showHint('Adjustments to the list are kept until the next refresh.');
    }

    function escapeHtml(value) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
        return (value || '').replace(/[&<>"']/g, match => map[match] || match);
    }

})();
