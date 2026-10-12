const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Database connection
const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'muq_system',
    waitForConnections: true,
    connectionLimit: 10
});

// Test database connection
pool.getConnection()
    .then(connection => {
        console.log('Connected to MySQL database');
        connection.release();
    })
    .catch(error => {
        console.error('Database connection failed:', error);
    });

// API Routes

// Health check
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', message: 'Server is running' });
});

// ==================== Users ====================

// Login
app.post('/api/login', async (req, res) => {
    try {
        const { username, password, type } = req.body;
        
        let query, params;
        
        if (type === 'student') {
            query = `
                SELECT u.*, s.id as student_id, s.name as student_name 
                FROM users u 
                JOIN students s ON u.student_id = s.id 
                WHERE u.username = ? AND u.password = ? AND u.type = 'student'
            `;
            params = [username, password];
        } else if (type === 'teacher') {
            query = `
                SELECT u.*, t.id as teacher_id, t.name as teacher_name 
                FROM users u 
                JOIN teachers t ON u.teacher_id = t.id 
                WHERE u.username = ? AND u.password = ? AND u.type = 'teacher'
            `;
            params = [username, password];
        } else if (type === 'administrative' || type === 'security' || type === 'service') {
            query = `
                SELECT u.*, s.id as staff_id, s.name as staff_name 
                FROM users u 
                JOIN administrative_staff s ON u.staff_id = s.id 
                WHERE u.username = ? AND u.password = ? AND u.type = ?
            `;
            params = [username, password, type];
        } else {
            query = 'SELECT * FROM users WHERE username = ? AND password = ? AND type = "admin"';
            params = [username, password];
        }
        
        const [rows] = await pool.query(query, params);
        
        if (rows.length > 0) {
            res.json({ success: true, user: rows[0] });
        } else {
            res.json({ success: false, message: 'Invalid credentials' });
        }
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ success: false, message: 'Server error' });
    }
});

// ==================== Departments ====================

app.get('/api/departments', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM departments ORDER BY id');
        res.json(rows);
    } catch (error) {
        console.error('Error fetching departments:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/departments', async (req, res) => {
    try {
        const { name, description, stageIds } = req.body;
        const [result] = await pool.query(
            'INSERT INTO departments (name, description) VALUES (?, ?)',
            [name, description]
        );
        
        // Update stages if stageIds provided
        if (stageIds && stageIds.length > 0) {
            for (const stageId of stageIds) {
                await pool.query(
                    'UPDATE stages SET department_id = ? WHERE id = ?',
                    [result.insertId, stageId]
                );
            }
        }
        
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating department:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.put('/api/departments/:id', async (req, res) => {
    try {
        const { name, description, stageIds } = req.body;
        const { id } = req.params;
        
        // Get old department
        const [oldDept] = await pool.query('SELECT * FROM departments WHERE id = ?', [id]);
        
        // Update department
        await pool.query(
            'UPDATE departments SET name = ?, description = ? WHERE id = ?',
            [name, description, id]
        );
        
        // Update stage links
        if (stageIds) {
            // Remove old links
            await pool.query('UPDATE stages SET department_id = NULL WHERE department_id = ?', [id]);
            
            // Add new links
            for (const stageId of stageIds) {
                await pool.query(
                    'UPDATE stages SET department_id = ? WHERE id = ?',
                    [id, stageId]
                );
            }
        }
        
        res.json({ success: true });
    } catch (error) {
        console.error('Error updating department:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.delete('/api/departments/:id', async (req, res) => {
    try {
        const { id } = req.params;
        await pool.query('DELETE FROM departments WHERE id = ?', [id]);
        res.json({ success: true });
    } catch (error) {
        console.error('Error deleting department:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// ==================== Stages ====================

app.get('/api/stages', async (req, res) => {
    try {
        const { department_id } = req.query;
        let query = 'SELECT * FROM stages ORDER BY id';
        let params = [];
        
        if (department_id) {
            query = 'SELECT * FROM stages WHERE department_id = ? ORDER BY id';
            params = [department_id];
        }
        
        const [rows] = await pool.query(query, params);
        res.json(rows);
    } catch (error) {
        console.error('Error fetching stages:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/stages', async (req, res) => {
    try {
        const { name, description, department_id } = req.body;
        const [result] = await pool.query(
            'INSERT INTO stages (name, description, department_id) VALUES (?, ?, ?)',
            [name, description, department_id]
        );
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating stage:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.put('/api/stages/:id', async (req, res) => {
    try {
        const { name, description, department_id } = req.body;
        const { id } = req.params;
        await pool.query(
            'UPDATE stages SET name = ?, description = ?, department_id = ? WHERE id = ?',
            [name, description, department_id, id]
        );
        res.json({ success: true });
    } catch (error) {
        console.error('Error updating stage:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.delete('/api/stages/:id', async (req, res) => {
    try {
        const { id } = req.params;
        await pool.query('DELETE FROM stages WHERE id = ?', [id]);
        res.json({ success: true });
    } catch (error) {
        console.error('Error deleting stage:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// ==================== Branches ====================

app.get('/api/branches', async (req, res) => {
    try {
        const { stage_id } = req.query;
        let query = 'SELECT * FROM branches ORDER BY id';
        let params = [];
        
        if (stage_id) {
            query = 'SELECT * FROM branches WHERE stage_id = ? ORDER BY id';
            params = [stage_id];
        }
        
        const [rows] = await pool.query(query, params);
        res.json(rows);
    } catch (error) {
        console.error('Error fetching branches:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/branches', async (req, res) => {
    try {
        const { name, description, stage_id } = req.body;
        const [result] = await pool.query(
            'INSERT INTO branches (name, description, stage_id) VALUES (?, ?, ?)',
            [name, description, stage_id]
        );
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating branch:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.put('/api/branches/:id', async (req, res) => {
    try {
        const { name, description, stage_id } = req.body;
        const { id } = req.params;
        await pool.query(
            'UPDATE branches SET name = ?, description = ?, stage_id = ? WHERE id = ?',
            [name, description, stage_id, id]
        );
        res.json({ success: true });
    } catch (error) {
        console.error('Error updating branch:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.delete('/api/branches/:id', async (req, res) => {
    try {
        const { id } = req.params;
        await pool.query('DELETE FROM branches WHERE id = ?', [id]);
        res.json({ success: true });
    } catch (error) {
        console.error('Error deleting branch:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// ==================== Students ====================

app.get('/api/students', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM students ORDER BY id');
        res.json(rows);
    } catch (error) {
        console.error('Error fetching students:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/students', async (req, res) => {
    try {
        const { name, id_number, department_id, stage_id, branch, email, phone, username, password } = req.body;
        
        const [result] = await pool.query(
            'INSERT INTO students (name, id_number, department_id, stage_id, branch, email, phone, username, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            [name, id_number, department_id, stage_id, branch, email, phone, username, password]
        );
        
        // Create user account
        await pool.query(
            'INSERT INTO users (username, password, type, name, student_id) VALUES (?, ?, ?, ?, ?)',
            [username, password, 'student', name, result.insertId]
        );
        
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating student:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.put('/api/students/:id', async (req, res) => {
    try {
        const { name, id_number, department_id, stage_id, branch, email, phone, username, password, face_data } = req.body;
        const { id } = req.params;
        
        await pool.query(
            'UPDATE students SET name = ?, id_number = ?, department_id = ?, stage_id = ?, branch = ?, email = ?, phone = ?, username = ?, password = ?, face_data = ? WHERE id = ?',
            [name, id_number, department_id, stage_id, branch, email, phone, username, password, JSON.stringify(face_data), id]
        );
        
        res.json({ success: true });
    } catch (error) {
        console.error('Error updating student:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.delete('/api/students/:id', async (req, res) => {
    try {
        const { id } = req.params;
        await pool.query('DELETE FROM students WHERE id = ?', [id]);
        res.json({ success: true });
    } catch (error) {
        console.error('Error deleting student:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// ==================== Teachers ====================

app.get('/api/teachers', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM teachers ORDER BY id');
        res.json(rows);
    } catch (error) {
        console.error('Error fetching teachers:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/teachers', async (req, res) => {
    try {
        const { name, specialization, subject, department_id, stage_id, branch, email, phone, username, password } = req.body;
        
        const [result] = await pool.query(
            'INSERT INTO teachers (name, specialization, subject, department_id, stage_id, branch, email, phone, username, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            [name, specialization, subject, department_id, stage_id, branch, email, phone, username, password]
        );
        
        // Create user account
        await pool.query(
            'INSERT INTO users (username, password, type, name, teacher_id) VALUES (?, ?, ?, ?, ?)',
            [username, password, 'teacher', name, result.insertId]
        );
        
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating teacher:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.put('/api/teachers/:id', async (req, res) => {
    try {
        const { name, specialization, subject, department_id, stage_id, branch, email, phone, username, password, face_data } = req.body;
        const { id } = req.params;
        
        await pool.query(
            'UPDATE teachers SET name = ?, specialization = ?, subject = ?, department_id = ?, stage_id = ?, branch = ?, email = ?, phone = ?, username = ?, password = ?, face_data = ? WHERE id = ?',
            [name, specialization, subject, department_id, stage_id, branch, email, phone, username, password, JSON.stringify(face_data), id]
        );
        
        res.json({ success: true });
    } catch (error) {
        console.error('Error updating teacher:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.delete('/api/teachers/:id', async (req, res) => {
    try {
        const { id } = req.params;
        await pool.query('DELETE FROM teachers WHERE id = ?', [id]);
        res.json({ success: true });
    } catch (error) {
        console.error('Error deleting teacher:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// ==================== Staff ====================

app.get('/api/staff/:type', async (req, res) => {
    try {
        const { type } = req.params;
        let table;
        
        if (type === 'administrative') {
            table = 'administrative_staff';
        } else if (type === 'security') {
            table = 'security_staff';
        } else if (type === 'service') {
            table = 'service_staff';
        } else {
            return res.status(400).json({ error: 'Invalid staff type' });
        }
        
        const [rows] = await pool.query(`SELECT * FROM ${table} ORDER BY id`);
        res.json(rows);
    } catch (error) {
        console.error('Error fetching staff:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/staff/:type', async (req, res) => {
    try {
        const { type } = req.params;
        const { name, department, position, email, phone, username, password } = req.body;
        
        let table;
        if (type === 'administrative') {
            table = 'administrative_staff';
        } else if (type === 'security') {
            table = 'security_staff';
        } else if (type === 'service') {
            table = 'service_staff';
        } else {
            return res.status(400).json({ error: 'Invalid staff type' });
        }
        
        const [result] = await pool.query(
            `INSERT INTO ${table} (name, department, position, email, phone, username, password) VALUES (?, ?, ?, ?, ?, ?, ?)`,
            [name, department, position, email, phone, username, password]
        );
        
        // Create user account
        await pool.query(
            'INSERT INTO users (username, password, type, name, staff_id, staff_type) VALUES (?, ?, ?, ?, ?, ?)',
            [username, password, type, name, result.insertId, type]
        );
        
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating staff:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.put('/api/staff/:type/:id', async (req, res) => {
    try {
        const { type } = req.params;
        const { name, department, position, email, phone, username, password, face_data } = req.body;
        const { id } = req.params;
        
        let table;
        if (type === 'administrative') {
            table = 'administrative_staff';
        } else if (type === 'security') {
            table = 'security_staff';
        } else if (type === 'service') {
            table = 'service_staff';
        } else {
            return res.status(400).json({ error: 'Invalid staff type' });
        }
        
        await pool.query(
            `UPDATE ${table} SET name = ?, department = ?, position = ?, email = ?, phone = ?, username = ?, password = ?, face_data = ? WHERE id = ?`,
            [name, department, position, email, phone, username, password, JSON.stringify(face_data), id]
        );
        
        res.json({ success: true });
    } catch (error) {
        console.error('Error updating staff:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.delete('/api/staff/:type/:id', async (req, res) => {
    try {
        const { type } = req.params;
        const { id } = req.params;
        
        let table;
        if (type === 'administrative') {
            table = 'administrative_staff';
        } else if (type === 'security') {
            table = 'security_staff';
        } else if (type === 'service') {
            table = 'service_staff';
        } else {
            return res.status(400).json({ error: 'Invalid staff type' });
        }
        
        await pool.query(`DELETE FROM ${table} WHERE id = ?`, [id]);
        res.json({ success: true });
    } catch (error) {
        console.error('Error deleting staff:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// ==================== Schedule ====================

app.get('/api/schedule', async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT s.*, t.name as teacher_name, d.name as department_name, st.name as stage_name 
            FROM schedule s 
            JOIN teachers t ON s.teacher_id = t.id 
            LEFT JOIN departments d ON s.department_id = d.id 
            LEFT JOIN stages st ON s.stage_id = st.id 
            ORDER BY s.day, s.time
        `);
        res.json(rows);
    } catch (error) {
        console.error('Error fetching schedule:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/schedule', async (req, res) => {
    try {
        const { day, time, subject, department_id, stage_id, branch, teacher_id } = req.body;
        const [result] = await pool.query(
            'INSERT INTO schedule (day, time, subject, department_id, stage_id, branch, teacher_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            [day, time, subject, department_id, stage_id, branch, teacher_id]
        );
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating schedule:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.put('/api/schedule/:id', async (req, res) => {
    try {
        const { day, time, subject, department_id, stage_id, branch, teacher_id } = req.body;
        const { id } = req.params;
        await pool.query(
            'UPDATE schedule SET day = ?, time = ?, subject = ?, department_id = ?, stage_id = ?, branch = ?, teacher_id = ? WHERE id = ?',
            [day, time, subject, department_id, stage_id, branch, teacher_id, id]
        );
        res.json({ success: true });
    } catch (error) {
        console.error('Error updating schedule:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.delete('/api/schedule/:id', async (req, res) => {
    try {
        const { id } = req.params;
        await pool.query('DELETE FROM schedule WHERE id = ?', [id]);
        res.json({ success: true });
    } catch (error) {
        console.error('Error deleting schedule:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// ==================== Attendance ====================

app.get('/api/attendance', async (req, res) => {
    try {
        const { student_id, schedule_id, date, status } = req.query;
        let query = `
            SELECT a.*, s.name as student_name, sched.subject, sched.day, sched.time, t.name as teacher_name 
            FROM attendance a 
            JOIN students s ON a.student_id = s.id 
            JOIN schedule sched ON a.schedule_id = sched.id 
            JOIN teachers t ON sched.teacher_id = t.id
        `;
        let params = [];
        let conditions = [];
        
        if (student_id) {
            conditions.push('a.student_id = ?');
            params.push(student_id);
        }
        if (schedule_id) {
            conditions.push('a.schedule_id = ?');
            params.push(schedule_id);
        }
        if (date) {
            conditions.push('a.date = ?');
            params.push(date);
        }
        if (status) {
            conditions.push('a.status = ?');
            params.push(status);
        }
        
        if (conditions.length > 0) {
            query += ' WHERE ' + conditions.join(' AND ');
        }
        
        query += ' ORDER BY a.date DESC';
        
        const [rows] = await pool.query(query, params);
        res.json(rows);
    } catch (error) {
        console.error('Error fetching attendance:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/attendance', async (req, res) => {
    try {
        const { date, student_id, schedule_id, status } = req.body;
        const [result] = await pool.query(
            'INSERT INTO attendance (date, student_id, schedule_id, status) VALUES (?, ?, ?, ?)',
            [date, student_id, schedule_id, status]
        );
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating attendance:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.put('/api/attendance/:id', async (req, res) => {
    try {
        const { status } = req.body;
        const { id } = req.params;
        await pool.query('UPDATE attendance SET status = ? WHERE id = ?', [status, id]);
        res.json({ success: true });
    } catch (error) {
        console.error('Error updating attendance:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// ==================== Staff Attendance ====================

app.get('/api/staff-attendance', async (req, res) => {
    try {
        const { staff_id, staff_type, date, status } = req.query;
        let query = `
            SELECT sa.*, s.name as staff_name 
            FROM staff_attendance sa 
            JOIN administrative_staff s ON sa.staff_id = s.id
        `;
        let params = [];
        let conditions = [];
        
        if (staff_id) {
            conditions.push('sa.staff_id = ?');
            params.push(staff_id);
        }
        if (staff_type) {
            conditions.push('sa.staff_type = ?');
            params.push(staff_type);
        }
        if (date) {
            conditions.push('sa.date = ?');
            params.push(date);
        }
        if (status) {
            conditions.push('sa.status = ?');
            params.push(status);
        }
        
        if (conditions.length > 0) {
            query += ' WHERE ' + conditions.join(' AND ');
        }
        
        query += ' ORDER BY sa.date DESC';
        
        const [rows] = await pool.query(query, params);
        res.json(rows);
    } catch (error) {
        console.error('Error fetching staff attendance:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.post('/api/staff-attendance', async (req, res) => {
    try {
        const { date, staff_id, staff_type, status } = req.body;
        const [result] = await pool.query(
            'INSERT INTO staff_attendance (date, staff_id, staff_type, status) VALUES (?, ?, ?, ?)',
            [date, staff_id, staff_type, status]
        );
        res.json({ success: true, id: result.insertId });
    } catch (error) {
        console.error('Error creating staff attendance:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// Start server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
