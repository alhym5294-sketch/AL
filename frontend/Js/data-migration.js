// Data Migration Script
// ترحيل البيانات من localStorage إلى MySQL

class DataMigration {
    constructor() {
        this.apiUrl = FACE_CONFIG.STORAGE.API_URL;
    }

    async migrateAll() {
        console.log('🔄 بدء ترحيل البيانات إلى MySQL...');

        try {
            // ترحيل الأقسام
            await this.migrateDepartments();

            // ترحيل المراحل
            await this.migrateStages();

            // ترحيل الشعب
            await this.migrateBranches();

            // ترحيل الطلاب
            await this.migrateStudents();

            // ترحيل المدرسين
            await this.migrateTeachers();

            // ترحيل الموظفين
            await this.migrateStaff();

            // ترحيل الجدول
            await this.migrateSchedule();

            // ترحيل الحضور
            await this.migrateAttendance();

            console.log('✅ تم ترحيل جميع البيانات بنجاح!');
            return { success: true };
        } catch (error) {
            console.error('❌ فشل في الترحيل:', error);
            return { success: false, error: error.message };
        }
    }

    async migrateDepartments() {
        const departments = JSON.parse(localStorage.getItem('muq_departments')) || [];
        console.log(`📦 ترحيل ${departments.length} قسم...`);

        for (const dept of departments) {
            await dbAPI.createDepartment({
                name: dept.name,
                description: dept.description
            });
        }
    }

    async migrateStages() {
        const stages = JSON.parse(localStorage.getItem('muq_stages')) || [];
        console.log(`📦 ترحيل ${stages.length} مرحلة...`);

        for (const stage of stages) {
            await dbAPI.createStage({
                name: stage.name,
                description: stage.description,
                department_id: stage.departmentId
            });
        }
    }

    async migrateBranches() {
        const branches = JSON.parse(localStorage.getItem('muq_branches')) || [];
        console.log(`📦 ترحيل ${branches.length} شعبة...`);

        for (const branch of branches) {
            await dbAPI.createBranch({
                name: branch.name,
                description: branch.description,
                stage_id: branch.stageId
            });
        }
    }

    async migrateStudents() {
        const students = JSON.parse(localStorage.getItem('muq_students')) || [];
        console.log(`📦 ترحيل ${students.length} طالب...`);

        for (const student of students) {
            await dbAPI.createStudent({
                name: student.name,
                id_number: student.idNumber,
                department_id: student.departmentId,
                stage_id: student.stageId,
                branch: student.branch,
                email: student.email,
                phone: student.phone,
                username: student.username,
                password: student.password
            });
        }
    }

    async migrateTeachers() {
        const teachers = JSON.parse(localStorage.getItem('muq_teachers')) || [];
        console.log(`📦 ترحيل ${teachers.length} مدرس...`);

        for (const teacher of teachers) {
            await dbAPI.createTeacher({
                name: teacher.name,
                specialization: teacher.specialization,
                subject: teacher.subject,
                department_id: teacher.departmentId,
                stage_id: teacher.stageId,
                branch: teacher.branch,
                email: teacher.email,
                phone: teacher.phone,
                username: teacher.username,
                password: teacher.password
            });
        }
    }

    async migrateStaff() {
        const types = ['administrative', 'security', 'service'];

        for (const type of types) {
            const staff = JSON.parse(localStorage.getItem(`muq_${type}_staff`)) || [];
            console.log(`📦 ترحيل ${staff.length} موظف ${type}...`);

            for (const person of staff) {
                await dbAPI.createStaff(type, {
                    name: person.name,
                    department: person.department,
                    position: person.position,
                    email: person.email,
                    phone: person.phone,
                    username: person.username,
                    password: person.password
                });
            }
        }
    }

    async migrateSchedule() {
        const schedule = JSON.parse(localStorage.getItem('muq_schedule')) || [];
        console.log(`📦 ترحيل ${schedule.length} محاضرة...`);

        for (const item of schedule) {
            await dbAPI.createSchedule({
                day: item.day,
                time: item.time,
                subject: item.subject,
                department_id: item.departmentId,
                stage_id: item.stageId,
                branch: item.branch,
                teacher_id: item.teacherId
            });
        }
    }

    async migrateAttendance() {
        const attendance = JSON.parse(localStorage.getItem('muq_attendance')) || [];
        console.log(`📦 ترحيل ${attendance.length} سجل حضور...`);

        for (const record of attendance) {
            await dbAPI.createAttendance({
                date: record.date,
                student_id: record.studentId,
                schedule_id: record.scheduleId,
                status: record.status
            });
        }
    }
}

// إنشاء نسخة واحدة من مدير الترحيل
const dataMigration = new DataMigration();
