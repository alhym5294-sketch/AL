// بوابة الدخول / بوابة التسجيل — التحقق من صلاحية الحساب قبل فتح البوابة

const PORTALS = {
    gate: { label: 'بوابة الدخول', page: 'gate-entry.html' },
    registration: { label: 'بوابة التسجيل', page: 'face-registration-new.html' }
};

function getPortalSessionUser() {
    const raw = localStorage.getItem('currentUser');
    if (!raw) return null;
    try {
        return JSON.parse(raw);
    } catch (e) {
        localStorage.removeItem('currentUser');
        return null;
    }
}

// تسجيل الطالب/المدرس/الموظف لوجهه بنفسه: نوع ومعرّف الرابط يطابقان حسابه
function isSelfRegistration(user) {
    const params = new URLSearchParams(window.location.search);
    const type = params.get('type');
    const id = parseInt(params.get('id'), 10);

    if (!type || !id) return false;
    if (type === 'student') return user.type === 'student' && user.studentId === id;
    if (type === 'teacher') return user.type === 'teacher' && user.teacherId === id;
    return user.type === type && user.staffType === type && user.staffId === id;
}

// يُستدعى من <head> قبل تنفيذ أي كود آخر في الصفحة
function requirePortalAccess(portalKey, options) {
    const allowSelfRegistration = !!(options && options.allowSelfRegistration);
    const user = getPortalSessionUser();

    if (!user) {
        window.location.replace('login.html?next=' + portalKey);
        return false;
    }

    const isPortalOperator = user.type === portalKey || user.type === 'admin';
    if (!isPortalOperator && !(allowSelfRegistration && isSelfRegistration(user))) {
        window.location.replace('login.html?denied=' + portalKey);
        return false;
    }

    if (isPortalOperator) {
        document.addEventListener('DOMContentLoaded', function() {
            showPortalSessionBar(user, PORTALS[portalKey]);
        });
    }
    return true;
}

function showPortalSessionBar(user, portal) {
    const bar = document.createElement('div');
    bar.className = 'portal-session-bar';
    bar.innerHTML = `
        <span class="portal-session-portal">${portal.label}</span>
        <span class="portal-session-user">${user.name || user.username}</span>
        <button class="logout-btn" onclick="portalLogout()">تسجيل الخروج</button>
    `;
    document.body.appendChild(bar);
}

function portalLogout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'login.html';
}
