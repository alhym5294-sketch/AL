// Import database class
// The database is defined in database.js and will be available when loaded

const HOME_BY_TYPE = {
    admin: 'admin-dashboard.html',
    teacher: 'teacher-dashboard.html',
    student: 'student-dashboard.html',
    administrative: 'staff-dashboard.html',
    security: 'staff-dashboard.html',
    service: 'staff-dashboard.html',
    gate: 'gate-entry.html',
    registration: 'face-registration-new.html'
};

const PORTALS = {
    gate: { label: 'بوابة الدخول', page: 'gate-entry.html' },
    registration: { label: 'بوابة التسجيل', page: 'face-registration-new.html' }
};

function getQueryParam(name) {
    return new URLSearchParams(window.location.search).get(name);
}

function canOpenPortal(user, portalKey) {
    return user.type === portalKey || user.type === 'admin';
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
}

// البوابة المطلوبة عبر ?next= — تُتجاهل أي قيمة غير معروفة لمنع إعادة التوجيه الخارجية
const requestedPortalKey = PORTALS[getQueryParam('next')] ? getQueryParam('next') : null;

if (requestedPortalKey) {
    document.getElementById('userType').value = requestedPortalKey;
}

// Login form handler
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const userType = document.getElementById('userType').value;

    const user = db.authenticateUser(username, password, userType);

    if (!user) {
        showError('اسم المستخدم أو كلمة المرور غير صحيحة');
        return;
    }

    if (requestedPortalKey && !canOpenPortal(user, requestedPortalKey)) {
        showError(`هذا الحساب غير مخوّل بفتح ${PORTALS[requestedPortalKey].label}.`);
        return;
    }

    localStorage.setItem('currentUser', JSON.stringify(user));
    window.location.href = requestedPortalKey ? PORTALS[requestedPortalKey].page : HOME_BY_TYPE[userType];
});

// Check if user is already logged in
window.addEventListener('load', function() {
    const deniedParam = getQueryParam('denied');

    if (PORTALS[deniedParam]) {
        showError(`حسابك الحالي غير مخوّل بفتح ${PORTALS[deniedParam].label}. سجّل الدخول بحساب آخر.`);
        return;
    }

    const raw = localStorage.getItem('currentUser');
    if (!raw) return;

    let user;
    try {
        user = JSON.parse(raw);
    } catch (err) {
        localStorage.removeItem('currentUser');
        return;
    }

    if (requestedPortalKey) {
        if (canOpenPortal(user, requestedPortalKey)) {
            window.location.href = PORTALS[requestedPortalKey].page;
        } else {
            showError(`حسابك الحالي غير مخوّل بفتح ${PORTALS[requestedPortalKey].label}. سجّل الدخول بحساب آخر.`);
        }
        return;
    }

    if (HOME_BY_TYPE[user.type]) {
        window.location.href = HOME_BY_TYPE[user.type];
    }
});
