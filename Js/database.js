// Database simulation using localStorage
class Database {
    constructor() {
        this.initializeData();
    }

    initializeData() {
        if (!localStorage.getItem('muq_users')) {
            const initialUsers = [
                {
                    id: 1,
                    username: 'admin',
                    password: '12345',
                    type: 'admin',
                    name: 'المدير العام',
                    faceData: null
                }
            ];
            localStorage.setItem('muq_users', JSON.stringify(initialUsers));
        }

        if (!localStorage.getItem('muq_students')) {
            localStorage.setItem('muq_students', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_teachers')) {
            localStorage.setItem('muq_teachers', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_administrative_staff')) {
            localStorage.setItem('muq_administrative_staff', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_security_staff')) {
            localStorage.setItem('muq_security_staff', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_service_staff')) {
            localStorage.setItem('muq_service_staff', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_gateways')) {
            localStorage.setItem('muq_gateways', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_departments')) {
            localStorage.setItem('muq_departments', JSON.stringify([]));
        }

        // Initialize or update stages to 6 stages
        const stages = localStorage.getItem('muq_stages');
        if (!stages) {
            localStorage.setItem('muq_stages', JSON.stringify([
                { id: 1, name: 'المرحلة الأولى', departmentId: null },
                { id: 2, name: 'المرحلة الثانية', departmentId: null },
                { id: 3, name: 'المرحلة الثالثة', departmentId: null },
                { id: 4, name: 'المرحلة الرابعة', departmentId: null },
                { id: 5, name: 'المرحلة الخامسة', departmentId: null },
                { id: 6, name: 'المرحلة السادسة', departmentId: null }
            ]));
        } else {
            // Update existing stages to ensure 6 stages
            const existingStages = JSON.parse(stages);
            const stageNames = ['المرحلة الأولى', 'المرحلة الثانية', 'المرحلة الثالثة', 'المرحلة الرابعة', 'المرحلة الخامسة', 'المرحلة السادسة'];
            const updatedStages = [];

            for (let i = 0; i < 6; i++) {
                const existingStage = existingStages.find(s => s.name === stageNames[i]);
                if (existingStage) {
                    updatedStages.push(existingStage);
                } else {
                    updatedStages.push({
                        id: Date.now() + i,
                        name: stageNames[i],
                        departmentId: null
                    });
                }
            }

            localStorage.setItem('muq_stages', JSON.stringify(updatedStages));
        }

        if (!localStorage.getItem('muq_branches')) {
            localStorage.setItem('muq_branches', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_schedule')) {
            localStorage.setItem('muq_schedule', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_attendance')) {
            localStorage.setItem('muq_attendance', JSON.stringify([]));
        }

        if (!localStorage.getItem('muq_staff_attendance')) {
            localStorage.setItem('muq_staff_attendance', JSON.stringify([]));
        }
    }

    getUsers() {
        return JSON.parse(localStorage.getItem('muq_users')) || [];
    }

    addUser(user) {
        const users = this.getUsers();
        user.id = Date.now();
        users.push(user);
        localStorage.setItem('muq_users', JSON.stringify(users));
        return user;
    }

    updateUser(id, updatedData) {
        const users = this.getUsers();
        const index = users.findIndex(u => u.id === id);
        if (index !== -1) {
            users[index] = { ...users[index], ...updatedData };
            localStorage.setItem('muq_users', JSON.stringify(users));
            return users[index];
        }
        return null;
    }

    deleteUser(id) {
        const users = this.getUsers();
        const filtered = users.filter(u => u.id !== id);
        localStorage.setItem('muq_users', JSON.stringify(filtered));
    }

    async getStudents() {
        if (this.useMySQL) {
            const result = await dbAPI.getStudents();
            return result || [];
        }
        return JSON.parse(localStorage.getItem('muq_students')) || [];
    }

    addStudent(student) {
        const students = this.getStudents();
        student.id = Date.now();
        student.departmentId = student.departmentId || null; // مرجع القسم
        student.stageId = student.stageId || null; // مرجع المرحلة
        student.branch = student.branch || ''; // اسم الشعبة (نص)
        students.push(student);
        localStorage.setItem('muq_students', JSON.stringify(students));
        return student;
    }

    updateStudent(id, updatedData) {
        const students = this.getStudents();
        const index = students.findIndex(s => s.id === id);
        if (index !== -1) {
            students[index] = { ...students[index], ...updatedData };
            localStorage.setItem('muq_students', JSON.stringify(students));
            return students[index];
        }
        return null;
    }

    deleteStudent(id) {
        const students = this.getStudents();
        const filtered = students.filter(s => s.id !== id);
        localStorage.setItem('muq_students', JSON.stringify(filtered));
    }

    getTeachers() {
        return JSON.parse(localStorage.getItem('muq_teachers')) || [];
    }

    addTeacher(teacher) {
        const teachers = this.getTeachers();
        teacher.id = Date.now();
        teacher.subject = teacher.subject || ''; // المادة التي يدرسها
        teacher.departmentId = teacher.departmentId || null; // مرجع القسم
        teacher.stageId = teacher.stageId || null; // مرجع المرحلة
        teacher.branch = teacher.branch || ''; // اسم الشعبة (نص)
        teachers.push(teacher);
        localStorage.setItem('muq_teachers', JSON.stringify(teachers));
        return teacher;
    }

    updateTeacher(id, updatedData) {
        const teachers = this.getTeachers();
        const index = teachers.findIndex(t => t.id === id);
        if (index !== -1) {
            teachers[index] = { ...teachers[index], ...updatedData };
            localStorage.setItem('muq_teachers', JSON.stringify(teachers));
            return teachers[index];
        }
        return null;
    }

    deleteTeacher(id) {
        const teachers = this.getTeachers();
        const filtered = teachers.filter(t => t.id !== id);
        localStorage.setItem('muq_teachers', JSON.stringify(filtered));
    }

    getSchedule() {
        return JSON.parse(localStorage.getItem('muq_schedule')) || [];
    }

    addScheduleItem(item) {
        const schedule = this.getSchedule();
        item.id = Date.now();
        item.subject = item.subject || ''; // المادة
        item.departmentId = item.departmentId || null; // مرجع القسم
        item.stageId = item.stageId || null; // مرجع المرحلة
        item.branch = item.branch || ''; // اسم الشعبة (نص)
        schedule.push(item);
        localStorage.setItem('muq_schedule', JSON.stringify(schedule));
        return item;
    }

    updateScheduleItem(id, updatedData) {
        const schedule = this.getSchedule();
        const index = schedule.findIndex(s => s.id === id);
        if (index !== -1) {
            schedule[index] = { ...schedule[index], ...updatedData };
            localStorage.setItem('muq_schedule', JSON.stringify(schedule));
            return schedule[index];
        }
        return null;
    }

    deleteScheduleItem(id) {
        const schedule = this.getSchedule();
        const filtered = schedule.filter(s => s.id !== id);
        localStorage.setItem('muq_schedule', JSON.stringify(filtered));
    }

    getAttendance() {
        return JSON.parse(localStorage.getItem('muq_attendance')) || [];
    }

    addAttendance(record) {
        const attendance = this.getAttendance();
        record.id = Date.now();
        attendance.push(record);
        localStorage.setItem('muq_attendance', JSON.stringify(attendance));
        return record;
    }

    updateAttendance(id, updatedData) {
        const attendance = this.getAttendance();
        const index = attendance.findIndex(a => a.id === id);
        if (index !== -1) {
            attendance[index] = { ...attendance[index], ...updatedData };
            localStorage.setItem('muq_attendance', JSON.stringify(attendance));
            return attendance[index];
        }
        return null;
    }

    authenticateUser(username, password, userType) {
        const users = this.getUsers();
        return users.find(u => u.username === username && u.password === password && u.type === userType);
    }

    getStudentById(id) {
        const students = this.getStudents();
        return students.find(s => s.id === id);
    }

    getTeacherById(id) {
        const teachers = this.getTeachers();
        return teachers.find(t => t.id === id);
    }

    getAttendanceByStudentId(studentId) {
        const attendance = this.getAttendance();
        return attendance.filter(a => a.studentId === studentId);
    }

    getAttendanceByDate(date) {
        const attendance = this.getAttendance();
        return attendance.filter(a => a.date === date);
    }

    getAttendanceByScheduleId(scheduleId) {
        const attendance = this.getAttendance();
        return attendance.filter(a => a.scheduleId === scheduleId);
    }

    getStudentsBySubjectAndStage(subject, stage) {
        const students = this.getStudents();
        return students.filter(s => s.stage === stage);
    }

    getStudentsBySubjectStageAndBranch(subject, stage, branch) {
        const students = this.getStudents();
        return students.filter(s => s.stage === stage && s.branch === branch);
    }

    getStudentsByStageAndBranch(stage, branch) {
        const students = this.getStudents();
        return students.filter(s => s.stage === stage && s.branch === branch);
    }

    getStudentsByDepartmentId(departmentId) {
        const students = this.getStudents();
        return students.filter(s => s.departmentId === departmentId);
    }

    getStudentsByStageId(stageId) {
        const students = this.getStudents();
        return students.filter(s => s.stageId === stageId);
    }

    getStudentsByBranchId(branchId) {
        const students = this.getStudents();
        return students.filter(s => s.branchId === branchId);
    }

    getStudentsByClassification(departmentId, stageId, branchId) {
        const students = this.getStudents();
        return students.filter(s => {
            if (departmentId && s.departmentId !== departmentId) return false;
            if (stageId && s.stageId !== stageId) return false;
            if (branchId && s.branchId !== branchId) return false;
            return true;
        });
    }

    getTeachersBySubjectAndStage(subject, stage) {
        const teachers = this.getTeachers();
        return teachers.filter(t => t.subject === subject && t.stage === stage);
    }

    getTeachersBySubjectStageAndBranch(subject, stage, branch) {
        const teachers = this.getTeachers();
        return teachers.filter(t => t.subject === subject && t.stage === stage && t.branch === branch);
    }

    getScheduleByTeacher(teacherId) {
        const schedule = this.getSchedule();
        return schedule.filter(s => s.teacherId === teacherId);
    }

    // Administrative Staff Methods
    getAdministrativeStaff() {
        return JSON.parse(localStorage.getItem('muq_administrative_staff')) || [];
    }

    addAdministrativeStaff(staff) {
        const staffList = this.getAdministrativeStaff();
        staff.id = Date.now();
        staffList.push(staff);
        localStorage.setItem('muq_administrative_staff', JSON.stringify(staffList));
        return staff;
    }

    updateAdministrativeStaff(id, updatedData) {
        const staffList = this.getAdministrativeStaff();
        const index = staffList.findIndex(s => s.id === id);
        if (index !== -1) {
            staffList[index] = { ...staffList[index], ...updatedData };
            localStorage.setItem('muq_administrative_staff', JSON.stringify(staffList));
            return staffList[index];
        }
        return null;
    }

    deleteAdministrativeStaff(id) {
        const staffList = this.getAdministrativeStaff();
        const filtered = staffList.filter(s => s.id !== id);
        localStorage.setItem('muq_administrative_staff', JSON.stringify(filtered));
    }

    // Security Staff Methods
    getSecurityStaff() {
        return JSON.parse(localStorage.getItem('muq_security_staff')) || [];
    }

    addSecurityStaff(staff) {
        const staffList = this.getSecurityStaff();
        staff.id = Date.now();
        staffList.push(staff);
        localStorage.setItem('muq_security_staff', JSON.stringify(staffList));
        return staff;
    }

    updateSecurityStaff(id, updatedData) {
        const staffList = this.getSecurityStaff();
        const index = staffList.findIndex(s => s.id === id);
        if (index !== -1) {
            staffList[index] = { ...staffList[index], ...updatedData };
            localStorage.setItem('muq_security_staff', JSON.stringify(staffList));
            return staffList[index];
        }
        return null;
    }

    deleteSecurityStaff(id) {
        const staffList = this.getSecurityStaff();
        const filtered = staffList.filter(s => s.id !== id);
        localStorage.setItem('muq_security_staff', JSON.stringify(filtered));
    }

    // Service Staff Methods
    getServiceStaff() {
        return JSON.parse(localStorage.getItem('muq_service_staff')) || [];
    }

    addServiceStaff(staff) {
        const staffList = this.getServiceStaff();
        staff.id = Date.now();
        staffList.push(staff);
        localStorage.setItem('muq_service_staff', JSON.stringify(staffList));
        return staff;
    }

    updateServiceStaff(id, updatedData) {
        const staffList = this.getServiceStaff();
        const index = staffList.findIndex(s => s.id === id);
        if (index !== -1) {
            staffList[index] = { ...staffList[index], ...updatedData };
            localStorage.setItem('muq_service_staff', JSON.stringify(staffList));
            return staffList[index];
        }
        return null;
    }

    deleteServiceStaff(id) {
        const staffList = this.getServiceStaff();
        const filtered = staffList.filter(s => s.id !== id);
        localStorage.setItem('muq_service_staff', JSON.stringify(filtered));
    }

    // Gateway Methods
    getGateways() {
        return JSON.parse(localStorage.getItem('muq_gateways')) || [];
    }

    addGateway(gateway) {
        const gatewayList = this.getGateways();
        gateway.id = Date.now();
        gatewayList.push(gateway);
        localStorage.setItem('muq_gateways', JSON.stringify(gatewayList));
        return gateway;
    }

    updateGateway(id, updatedData) {
        const gatewayList = this.getGateways();
        const index = gatewayList.findIndex(g => g.id === id);
        if (index !== -1) {
            gatewayList[index] = { ...gatewayList[index], ...updatedData };
            localStorage.setItem('muq_gateways', JSON.stringify(gatewayList));
            return gatewayList[index];
        }
        return null;
    }

    deleteGateway(id) {
        const gatewayList = this.getGateways();
        const filtered = gatewayList.filter(g => g.id !== id);
        localStorage.setItem('muq_gateways', JSON.stringify(filtered));
    }

    // Staff Attendance Methods
    getStaffAttendance() {
        return JSON.parse(localStorage.getItem('muq_staff_attendance')) || [];
    }

    addStaffAttendance(record) {
        const attendance = this.getStaffAttendance();
        record.id = Date.now();
        attendance.push(record);
        localStorage.setItem('muq_staff_attendance', JSON.stringify(attendance));
        return record;
    }

    getStaffAttendanceByType(staffType) {
        const attendance = this.getStaffAttendance();
        return attendance.filter(a => a.staffType === staffType);
    }

    getStaffAttendanceByDate(date) {
        const attendance = this.getStaffAttendance();
        return attendance.filter(a => a.date === date);
    }

    // Department Methods
    getDepartments() {
        return JSON.parse(localStorage.getItem('muq_departments')) || [];
    }

    addDepartment(department) {
        const departments = this.getDepartments();
        department.id = Date.now();
        department.stageIds = department.stageIds || []; // Array of selected stage IDs
        departments.push(department);
        localStorage.setItem('muq_departments', JSON.stringify(departments));

        // Update stages to link to this department
        if (department.stageIds && department.stageIds.length > 0) {
            department.stageIds.forEach(stageId => {
                this.updateStage(stageId, { departmentId: department.id });
            });
        }

        return department;
    }

    updateDepartment(id, updatedData) {
        const departments = this.getDepartments();
        const index = departments.findIndex(d => d.id === id);
        if (index !== -1) {
            const oldDepartment = departments[index];
            const newDepartment = { ...departments[index], ...updatedData };

            // Update stage links
            if (newDepartment.stageIds) {
                // Remove old stage links
                if (oldDepartment.stageIds) {
                    oldDepartment.stageIds.forEach(stageId => {
                        this.updateStage(stageId, { departmentId: null });
                    });
                }

                // Add new stage links
                newDepartment.stageIds.forEach(stageId => {
                    this.updateStage(stageId, { departmentId: newDepartment.id });
                });
            }

            departments[index] = newDepartment;
            localStorage.setItem('muq_departments', JSON.stringify(departments));
            return newDepartment;
        }
        return null;
    }

    deleteDepartment(id) {
        const departments = this.getDepartments();
        const filtered = departments.filter(d => d.id !== id);
        localStorage.setItem('muq_departments', JSON.stringify(filtered));

        // Also delete stages associated with this department
        const stages = this.getStages().filter(s => s.departmentId === id);
        stages.forEach(stage => {
            this.deleteStage(stage.id);
        });

        // Update students to remove department reference
        const students = this.getStudents().filter(s => s.departmentId === id);
        students.forEach(student => {
            this.updateStudent(student.id, { departmentId: null, stageId: null, branchId: null });
        });
    }

    // Stage Methods
    getStages() {
        return JSON.parse(localStorage.getItem('muq_stages')) || [];
    }

    getStagesByDepartmentId(departmentId) {
        const stages = this.getStages();
        return stages.filter(s => s.departmentId === departmentId);
    }

    addStage(stage) {
        const stages = this.getStages();
        stage.id = Date.now();
        stage.departmentId = stage.departmentId || null;
        stages.push(stage);
        localStorage.setItem('muq_stages', JSON.stringify(stages));
        return stage;
    }

    updateStage(id, updatedData) {
        const stages = this.getStages();
        const index = stages.findIndex(s => s.id === id);
        if (index !== -1) {
            stages[index] = { ...stages[index], ...updatedData };
            localStorage.setItem('muq_stages', JSON.stringify(stages));
            return stages[index];
        }
        return null;
    }

    deleteStage(id) {
        const stages = this.getStages();
        const filtered = stages.filter(s => s.id !== id);
        localStorage.setItem('muq_stages', JSON.stringify(filtered));

        // Also delete branches associated with this stage
        const branches = this.getBranches().filter(b => b.stageId === id);
        branches.forEach(branch => {
            this.deleteBranch(branch.id);
        });

        // Update students to remove stage reference
        const students = this.getStudents().filter(s => s.stageId === id);
        students.forEach(student => {
            this.updateStudent(student.id, { stageId: null, branchId: null });
        });
    }

    // Branch Methods
    getBranches() {
        return JSON.parse(localStorage.getItem('muq_branches')) || [];
    }

    getBranchesByStageId(stageId) {
        const branches = this.getBranches();
        return branches.filter(b => b.stageId === stageId);
    }

    addBranch(branch) {
        const branches = this.getBranches();
        branch.id = Date.now();
        branch.stageId = branch.stageId || null;
        branches.push(branch);
        localStorage.setItem('muq_branches', JSON.stringify(branches));
        return branch;
    }

    updateBranch(id, updatedData) {
        const branches = this.getBranches();
        const index = branches.findIndex(b => b.id === id);
        if (index !== -1) {
            branches[index] = { ...branches[index], ...updatedData };
            localStorage.setItem('muq_branches', JSON.stringify(branches));
            return branches[index];
        }
        return null;
    }

    deleteBranch(id) {
        const branches = this.getBranches();
        const filtered = branches.filter(b => b.id !== id);
        localStorage.setItem('muq_branches', JSON.stringify(filtered));

        // Update students to remove branch reference
        const students = this.getStudents().filter(s => s.branchId === id);
        students.forEach(student => {
            this.updateStudent(student.id, { branchId: null });
        });
    }

    // Helper methods to get names from IDs
    getDepartmentNameById(id) {
        const department = this.getDepartments().find(d => d.id === id);
        return department ? department.name : '';
    }

    getStageNameById(id) {
        const stage = this.getStages().find(s => s.id === id);
        return stage ? stage.name : '';
    }

    getBranchNameById(id) {
        const branch = this.getBranches().find(b => b.id === id);
        return branch ? branch.name : '';
    }

    getDepartmentById(id) {
        return this.getDepartments().find(d => d.id === id);
    }

    getStageById(id) {
        return this.getStages().find(s => s.id === id);
    }

    getBranchById(id) {
        return this.getBranches().find(b => b.id === id);
    }
}

const db = new Database();