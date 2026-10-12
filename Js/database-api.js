// Database API Manager
// إدارة الاتصال بـ MySQL Backend

class DatabaseAPI {
    constructor() {
        this.apiUrl = FACE_CONFIG.STORAGE.API_URL;
    }

    // Generic API call
    async apiCall(endpoint, method = 'GET', data = null) {
        try {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(`${this.apiUrl}${endpoint}`, options);
            const result = await response.json();

            return result;
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            return { success: false, error: error.message };
        }
    }

    // ==================== Users ====================

    async login(username, password, type) {
        return await this.apiCall('/api/login', 'POST', {
            username,
            password,
            type
        });
    }

    // ==================== Departments ====================

    async getDepartments() {
        return await this.apiCall('/api/departments');
    }

    async createDepartment(data) {
        return await this.apiCall('/api/departments', 'POST', data);
    }

    async updateDepartment(id, data) {
        return await this.apiCall(`/api/departments/${id}`, 'PUT', data);
    }

    async deleteDepartment(id) {
        return await this.apiCall(`/api/departments/${id}`, 'DELETE');
    }

    // ==================== Stages ====================

    async getStages(departmentId = null) {
        const endpoint = departmentId ? `/api/stages?department_id=${departmentId}` : '/api/stages';
        return await this.apiCall(endpoint);
    }

    async createStage(data) {
        return await this.apiCall('/api/stages', 'POST', data);
    }

    async updateStage(id, data) {
        return await this.apiCall(`/api/stages/${id}`, 'PUT', data);
    }

    async deleteStage(id) {
        return await this.apiCall(`/api/stages/${id}`, 'DELETE');
    }

    // ==================== Branches ====================

    async getBranches(stageId = null) {
        const endpoint = stageId ? `/api/branches?stage_id=${stageId}` : '/api/branches';
        return await this.apiCall(endpoint);
    }

    async createBranch(data) {
        return await this.apiCall('/api/branches', 'POST', data);
    }

    async updateBranch(id, data) {
        return await this.apiCall(`/api/branches/${id}`, 'PUT', data);
    }

    async deleteBranch(id) {
        return await this.apiCall(`/api/branches/${id}`, 'DELETE');
    }

    // ==================== Students ====================

    async getStudents() {
        return await this.apiCall('/api/students');
    }

    async createStudent(data) {
        return await this.apiCall('/api/students', 'POST', data);
    }

    async updateStudent(id, data) {
        return await this.apiCall(`/api/students/${id}`, 'PUT', data);
    }

    async deleteStudent(id) {
        return await this.apiCall(`/api/students/${id}`, 'DELETE');
    }

    // ==================== Teachers ====================

    async getTeachers() {
        return await this.apiCall('/api/teachers');
    }

    async createTeacher(data) {
        return await this.apiCall('/api/teachers', 'POST', data);
    }

    async updateTeacher(id, data) {
        return await this.apiCall(`/api/teachers/${id}`, 'PUT', data);
    }

    async deleteTeacher(id) {
        return await this.apiCall(`/api/teachers/${id}`, 'DELETE');
    }

    // ==================== Staff ====================

    async getStaff(type) {
        return await this.apiCall(`/api/staff/${type}`);
    }

    async createStaff(type, data) {
        return await this.apiCall(`/api/staff/${type}`, 'POST', data);
    }

    async updateStaff(type, id, data) {
        return await this.apiCall(`/api/staff/${type}/${id}`, 'PUT', data);
    }

    async deleteStaff(type, id) {
        return await this.apiCall(`/api/staff/${type}/${id}`, 'DELETE');
    }

    // ==================== Schedule ====================

    async getSchedule() {
        return await this.apiCall('/api/schedule');
    }

    async createSchedule(data) {
        return await this.apiCall('/api/schedule', 'POST', data);
    }

    async updateSchedule(id, data) {
        return await this.apiCall(`/api/schedule/${id}`, 'PUT', data);
    }

    async deleteSchedule(id) {
        return await this.apiCall(`/api/schedule/${id}`, 'DELETE');
    }

    // ==================== Attendance ====================

    async getAttendance(filters = {}) {
        const params = new URLSearchParams(filters);
        const endpoint = `/api/attendance?${params}`;
        return await this.apiCall(endpoint);
    }

    async createAttendance(data) {
        return await this.apiCall('/api/attendance', 'POST', data);
    }

    async updateAttendance(id, data) {
        return await this.apiCall(`/api/attendance/${id}`, 'PUT', data);
    }

    // ==================== Staff Attendance ====================

    async getStaffAttendance(filters = {}) {
        const params = new URLSearchParams(filters);
        const endpoint = `/api/staff-attendance?${params}`;
        return await this.apiCall(endpoint);
    }

    async createStaffAttendance(data) {
        return await this.apiCall('/api/staff-attendance', 'POST', data);
    }
}

// إنشاء نسخة واحدة من مدير API
const dbAPI = new DatabaseAPI();
