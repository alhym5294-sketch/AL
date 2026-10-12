from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration - MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}/{os.getenv('DB_NAME', 'muq_system')}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== Models ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # admin, teacher, student, administrative, security, service
    name = db.Column(db.String(100), nullable=False)
    face_data = db.Column(db.JSON)  # Legacy face data (version 1)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('administrative_staff.id'), nullable=True)
    staff_type = db.Column(db.String(20))  # administrative, security, service
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    stages = db.relationship('Stage', backref='department', lazy=True)

class Stage(db.Model):
    __tablename__ = 'stages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    branches = db.relationship('Branch', backref='stage', lazy=True)

class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_number = db.Column(db.String(50), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'), nullable=True)
    branch = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    face_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref='student', uselist=False)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'), nullable=True)
    branch = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    face_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref='teacher', uselist=False)

class AdministrativeStaff(db.Model):
    __tablename__ = 'administrative_staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    face_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref='staff', uselist=False)

class SecurityStaff(db.Model):
    __tablename__ = 'security_staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    face_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ServiceStaff(db.Model):
    __tablename__ = 'service_staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    face_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'), nullable=True)
    branch = db.Column(db.String(50))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    teacher = db.relationship('Teacher', backref='schedule', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # present, absent, pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    student = db.relationship('Student', backref='attendance', lazy=True)
    schedule = db.relationship('Schedule', backref='attendance', lazy=True)

class StaffAttendance(db.Model):
    __tablename__ = 'staff_attendance'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)
    staff_type = db.Column(db.String(20), nullable=False)  # administrative, security, service
    status = db.Column(db.String(20), default='pending')  # present, absent, pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Face Profile Table
class FaceProfile(db.Model):
    __tablename__ = 'face_profiles'
    id = db.Column(db.Integer, primary_key=True)
    person_type = db.Column(db.String(20), nullable=False)  # student, teacher, administrative, security, service
    person_id = db.Column(db.Integer, nullable=False)
    model_version = db.Column(db.String(50), default='face-api.js')
    model_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    samples = db.relationship('FaceSample', backref='profile', lazy=True, cascade='all, delete-orphan')

# Face Sample Table
class FaceSample(db.Model):
    __tablename__ = 'face_samples'
    id = db.Column(db.Integer, primary_key=True)
    face_profile_id = db.Column(db.Integer, db.ForeignKey('face_profiles.id'), nullable=False)
    embedding = db.Column(db.JSON, nullable=False)  # 128-dimensional vector
    pose = db.Column(db.String(20))  # front, right_15, right_30, left_15, left_30, up, down
    quality_score = db.Column(db.Float, default=0.0)
    captured_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# ==================== API Routes ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

# ==================== Login ====================

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('type')
        
        user = None
        
        if user_type == 'student':
            user = User.query.join(Student).filter(
                User.username == username,
                User.password == password,
                User.type == 'student'
            ).first()
        elif user_type == 'teacher':
            user = User.query.join(Teacher).filter(
                User.username == username,
                User.password == password,
                User.type == 'teacher'
            ).first()
        elif user_type in ['administrative', 'security', 'service']:
            user = User.query.join(AdministrativeStaff).filter(
                User.username == username,
                User.password == password,
                User.type == user_type
            ).first()
        else:
            user = User.query.filter(
                username=username,
                password=password,
                type='admin'
            ).first()
        
        if user:
            user_dict = {
                'id': user.id,
                'username': user.username,
                'type': user.type,
                'name': user.name,
                'face_data': user.face_data
            }
            if user.student_id:
                user_dict['student_id'] = user.student_id
            if user.teacher_id:
                user_dict['teacher_id'] = user.teacher_id
            if user.staff_id:
                user_dict['staff_id'] = user.staff_id
                user_dict['staff_type'] = user.staff_type
            return jsonify({'success': True, 'user': user_dict})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== Departments ====================

@app.route('/api/departments', methods=['GET'])
def get_departments():
    try:
        departments = Department.query.all()
        return jsonify([{
            'id': d.id,
            'name': d.name,
            'description': d.description,
            'stage_ids': [s.id for s in d.stages]
        } for d in departments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/departments', methods=['POST'])
def create_department():
    try:
        data = request.json
        department = Department(
            name=data.get('name'),
            description=data.get('description')
        )
        db.session.add(department)
        db.session.commit()
        
        # Update stages if stageIds provided
        stage_ids = data.get('stageIds', [])
        if stage_ids:
            for stage_id in stage_ids:
                stage = Stage.query.get(stage_id)
                if stage:
                    stage.department_id = department.id
        
        db.session.commit()
        return jsonify({'success': True, 'id': department.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/departments/<int:id>', methods=['PUT'])
def update_department(id):
    try:
        data = request.json
        department = Department.query.get_or_404(id)
        
        # Update department
        department.name = data.get('name', department.name)
        department.description = data.get('description', department.description)
        
        # Update stage links
        stage_ids = data.get('stageIds')
        if stage_ids is not None:
            # Remove old links
            Stage.query.filter_by(department_id=id).update({'department_id': None})
            
            # Add new links
            for stage_id in stage_ids:
                stage = Stage.query.get(stage_id)
                if stage:
                    stage.department_id = id
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    try:
        department = Department.query.get_or_404(id)
        db.session.delete(department)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Stages ====================

@app.route('/api/stages', methods=['GET'])
def get_stages():
    try:
        department_id = request.args.get('department_id', type=int)
        query = Stage.query.order_by(Stage.id)
        
        if department_id:
            query = query.filter_by(department_id=department_id)
        
        stages = query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'description': s.description,
            'department_id': s.department_id
        } for s in stages])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stages', methods=['POST'])
def create_stage():
    try:
        data = request.json
        stage = Stage(
            name=data.get('name'),
            description=data.get('description'),
            department_id=data.get('department_id')
        )
        db.session.add(stage)
        db.session.commit()
        return jsonify({'success': True, 'id': stage.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/stages/<int:id>', methods=['PUT'])
def update_stage(id):
    try:
        data = request.json
        stage = Stage.query.get_or_404(id)
        stage.name = data.get('name', stage.name)
        stage.description = data.get('description', stage.description)
        stage.department_id = data.get('department_id')
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/stages/<int:id>', methods=['DELETE'])
def delete_stage(id):
    try:
        stage = Stage.query.get_or_404(id)
        db.session.delete(stage)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Branches ====================

@app.route('/api/branches', methods=['GET'])
def get_branches():
    try:
        stage_id = request.args.get('stage_id', type=int)
        query = Branch.query.order_by(Branch.id)
        
        if stage_id:
            query = query.filter_by(stage_id=stage_id)
        
        branches = query.all()
        return jsonify([{
            'id': b.id,
            'name': b.name,
            'description': b.description,
            'stage_id': b.stage_id
        } for b in branches])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/branches', methods=['POST'])
def create_branch():
    try:
        data = request.json
        branch = Branch(
            name=data.get('name'),
            description=data.get('description'),
            stage_id=data.get('stage_id')
        )
        db.session.add(branch)
        db.session.commit()
        return jsonify({'success': True, 'id': branch.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/branches/<int:id>', methods=['PUT'])
def update_branch(id):
    try:
        data = request.json
        branch = Branch.query.get_or_404(id)
        branch.name = data.get('name', branch.name)
        branch.description = data.get('description', branch.description)
        branch.stage_id = data.get('stage_id')
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/branches/<int:id>', methods=['DELETE'])
def delete_branch(id):
    try:
        branch = Branch.query.get_or_404(id)
        db.session.delete(branch)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Students ====================

@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        students = Student.query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'id_number': s.id_number,
            'department_id': s.department_id,
            'stage_id': s.stage_id,
            'branch': s.branch,
            'email': s.email,
            'phone': s.phone,
            'username': s.username,
            'face_data': s.face_data
        } for s in students])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def create_student():
    try:
        data = request.json
        student = Student(
            name=data.get('name'),
            id_number=data.get('id_number'),
            department_id=data.get('department_id'),
            stage_id=data.get('stage_id'),
            branch=data.get('branch'),
            email=data.get('email'),
            phone=data.get('phone'),
            username=data.get('username'),
            password=data.get('password')
        )
        db.session.add(student)
        db.session.commit()
        
        # Create user account
        user = User(
            username=data.get('username'),
            password=data.get('password'),
            type='student',
            name=data.get('name'),
            student_id=student.id
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'id': student.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.json
        student = Student.query.get_or_404(id)
        
        student.name = data.get('name', student.name)
        student.id_number = data.get('id_number', student.id_number)
        student.department_id = data.get('department_id')
        student.stage_id = data.get('stage_id')
        student.branch = data.get('branch')
        student.email = data.get('email', student.email)
        student.phone = data.get('phone', student.phone)
        student.username = data.get('username', student.username)
        student.password = data.get('password', student.password)
        student.face_data = data.get('face_data')
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Teachers ====================

@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    try:
        teachers = Teacher.query.all()
        return jsonify([{
            'id': t.id,
            'name': t.name,
            'specialization': t.specialization,
            'subject': t.subject,
            'department_id': t.department_id,
            'stage_id': t.stage_id,
            'branch': t.branch,
            'email': t.email,
            'phone': t.phone,
            'username': t.username,
            'face_data': t.face_data
        } for t in teachers])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teachers', methods=['POST'])
def create_teacher():
    try:
        data = request.json
        teacher = Teacher(
            name=data.get('name'),
            specialization=data.get('specialization'),
            subject=data.get('subject'),
            department_id=data.get('department_id'),
            stage_id=data.get('stage_id'),
            branch=data.get('branch'),
            email=data.get('email'),
            phone=data.get('phone'),
            username=data.get('username'),
            password=data.get('password')
        )
        db.session.add(teacher)
        db.session.commit()
        
        # Create user account
        user = User(
            username=data.get('username'),
            password=data.get('password'),
            type='teacher',
            name=data.get('name'),
            teacher_id=teacher.id
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'id': teacher.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/teachers/<int:id>', methods=['PUT'])
def update_teacher(id):
    try:
        data = request.json
        teacher = Teacher.query.get_or_404(id)
        
        teacher.name = data.get('name', teacher.name)
        teacher.specialization = data.get('specialization', teacher.specialization)
        teacher.subject = data.get('subject', teacher.subject)
        teacher.department_id = data.get('department_id')
        teacher.stage_id = data.get('stage_id')
        teacher.branch = data.get('branch')
        teacher.email = data.get('email', teacher.email)
        teacher.phone = data.get('phone', teacher.phone)
        teacher.username = data.get('username', teacher.username)
        teacher.password = data.get('password', teacher.password)
        teacher.face_data = data.get('face_data')
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/teachers/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        teacher = Teacher.query.get_or_404(id)
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Staff ====================

@app.route('/api/staff/<string:staff_type>', methods=['GET'])
def get_staff(staff_type):
    try:
        if staff_type == 'administrative':
            model = AdministrativeStaff
        elif staff_type == 'security':
            model = SecurityStaff
        elif staff_type == 'service':
            model = ServiceStaff
        else:
            return jsonify({'error': 'Invalid staff type'}), 400
        
        staff = model.query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'department': s.department,
            'position': s.position,
            'email': s.email,
            'phone': s.phone,
            'username': s.username,
            'face_data': s.face_data
        } for s in staff])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/staff/<string:staff_type>', methods=['POST'])
def create_staff(staff_type):
    try:
        data = request.json
        
        if staff_type == 'administrative':
            model = AdministrativeStaff
        elif staff_type == 'security':
            model = SecurityStaff
        elif staff_type == 'service':
            model = ServiceStaff
        else:
            return jsonify({'error': 'Invalid staff type'}), 400
        
        staff = model(
            name=data.get('name'),
            department=data.get('department'),
            position=data.get('position'),
            email=data.get('email'),
            phone=data.get('phone'),
            username=data.get('username'),
            password=data.get('password')
        )
        db.session.add(staff)
        db.session.commit()
        
        # Create user account
        user = User(
            username=data.get('username'),
            password=data.get('password'),
            type=staff_type,
            name=data.get('name'),
            staff_id=staff.id,
            staff_type=staff_type
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'id': staff.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/staff/<string:staff_type>/<int:id>', methods=['PUT'])
def update_staff(staff_type, id):
    try:
        data = request.json
        
        if staff_type == 'administrative':
            model = AdministrativeStaff
        elif staff_type == 'security':
            model = SecurityStaff
        elif staff_type == 'service':
            model = ServiceStaff
        else:
            return jsonify({'error': 'Invalid staff type'}), 400
        
        staff = model.query.get_or_404(id)
        staff.name = data.get('name', staff.name)
        staff.department = data.get('department', staff.department)
        staff.position = data.get('position', staff.position)
        staff.email = data.get('email', staff.email)
        staff.phone = data.get('phone', staff.phone)
        staff.username = data.get('username', staff.username)
        staff.password = data.get('password', staff.password)
        staff.face_data = data.get('face_data')
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/staff/<string:staff_type>/<int:id>', methods=['DELETE'])
def delete_staff(staff_type, id):
    try:
        if staff_type == 'administrative':
            model = AdministrativeStaff
        elif staff_type == 'security':
            model = SecurityStaff
        elif staff_type == 'service':
            model = ServiceStaff
        else:
            return jsonify({'error': 'Invalid staff type'}), 400
        
        staff = model.query.get_or_404(id)
        db.session.delete(staff)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Schedule ====================

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    try:
        schedule = Schedule.query.join(Teacher).all()
        return jsonify([{
            'id': s.id,
            'day': s.day,
            'time': s.time,
            'subject': s.subject,
            'department_id': s.department_id,
            'stage_id': s.stage_id,
            'branch': s.branch,
            'teacher_id': s.teacher_id,
            'teacher_name': s.teacher.name if s.teacher else 'غير محدد'
        } for s in schedule])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/schedule', methods=['POST'])
def create_schedule():
    try:
        data = request.json
        schedule = Schedule(
            day=data.get('day'),
            time=data.get('time'),
            subject=data.get('subject'),
            department_id=data.get('department_id'),
            stage_id=data.get('stage_id'),
            branch=data.get('branch'),
            teacher_id=data.get('teacher_id')
        )
        db.session.add(schedule)
        db.session.commit()
        return jsonify({'success': True, 'id': schedule.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/schedule/<int:id>', methods=['PUT'])
def update_schedule(id):
    try:
        data = request.json
        schedule = Schedule.query.get_or_404(id)
        schedule.day = data.get('day', schedule.day)
        schedule.time = data.get('time', schedule.time)
        schedule.subject = data.get('subject', schedule.subject)
        schedule.department_id = data.get('department_id')
        schedule.stage_id = data.get('stage_id')
        schedule.branch = data.get('branch')
        schedule.teacher_id = data.get('teacher_id')
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/schedule/<int:id>', methods=['DELETE'])
def delete_schedule(id):
    try:
        schedule = Schedule.query.get_or_404(id)
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Attendance ====================

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    try:
        student_id = request.args.get('student_id', type=int)
        schedule_id = request.args.get('schedule_id', type=int)
        date = request.args.get('date')
        status = request.args.get('status')
        
        query = Attendance.query.join(Student).join(Schedule).join(Teacher)
        
        if student_id:
            query = query.filter(Attendance.student_id == student_id)
        if schedule_id:
            query = query.filter(Attendance.schedule_id == schedule_id)
        if date:
            query = query.filter(Attendance.date == date)
        if status:
            query = query.filter(Attendance.status == status)
        
        attendance = query.order_by(Attendance.date.desc()).all()
        return jsonify([{
            'id': a.id,
            'date': a.date.strftime('%Y-%m-%d'),
            'student_id': a.student_id,
            'student_name': a.student.name if a.student else 'غير محدد',
            'schedule_id': a.schedule_id,
            'subject': a.schedule.subject if a.schedule else 'غير محدد',
            'day': a.schedule.day if a.schedule else 'غير محدد',
            'time': a.schedule.time if a.schedule else 'غير محدد',
            'teacher_name': a.teacher.name if a.teacher else 'غير محدد',
            'status': a.status
        } for a in attendance])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance', methods=['POST'])
def create_attendance():
    try:
        data = request.json
        attendance = Attendance(
            date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
            student_id=data.get('student_id'),
            schedule_id=data.get('schedule_id'),
            status=data.get('status', 'pending')
        )
        db.session.add(attendance)
        db.session.commit()
        return jsonify({'success': True, 'id': attendance.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/<int:id>', methods=['PUT'])
def update_attendance(id):
    try:
        data = request.json
        attendance = Attendance.query.get_or_404(id)
        attendance.status = data.get('status', attendance.status)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Staff Attendance ====================

@app.route('/api/staff-attendance', methods=['GET'])
def get_staff_attendance():
    try:
        staff_id = request.args.get('staff_id', type=int)
        staff_type = request.args.get('staff_type')
        date = request.args.get('date')
        status = request.args.get('status')
        
        query = StaffAttendance.query
        
        if staff_id:
            query = query.filter(StaffAttendance.staff_id == staff_id)
        if staff_type:
            query = query.filter(StaffAttendance.staff_type == staff_type)
        if date:
            query = query.filter(StaffAttendance.date == date)
        if status:
            query = query.filter(StaffAttendance.status == status)
        
        attendance = query.order_by(StaffAttendance.date.desc()).all()
        
        # Get staff names
        result = []
        for a in attendance:
            staff_name = 'غير محدد'
            if a.staff_type == 'administrative':
                staff = AdministrativeStaff.query.get(a.staff_id)
                if staff:
                    staff_name = staff.name
            elif a.staff_type == 'security':
                staff = SecurityStaff.query.get(a.staff_id)
                if staff:
                    staff_name = staff.name
            elif a.staff_type == 'service':
                staff = ServiceStaff.query.get(a.staff_id)
                if staff:
                    staff_name = staff.name
            
            result.append({
                'id': a.id,
                'date': a.date.strftime('%Y-%m-%d'),
                'staff_id': a.staff_id,
                'staff_type': a.staff_type,
                'staff_name': staff_name,
                'status': a.status
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/staff-attendance', methods=['POST'])
def create_staff_attendance():
    try:
        data = request.json
        attendance = StaffAttendance(
            date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
            staff_id=data.get('staff_id'),
            staff_type=data.get('staff_type'),
            status=data.get('status', 'pending')
        )
        db.session.add(attendance)
        db.session.commit()
        return jsonify({'success': True, 'id': attendance.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Face Profiles ====================

@app.route('/api/face-profiles/<string:person_type>/<int:person_id>', methods=['GET'])
def get_face_profile(person_type, person_id):
    try:
        profile = FaceProfile.query.filter_by(
            person_type=person_type,
            person_id=person_id
        ).first()

        if not profile:
            return jsonify({'success': False, 'message': 'No face profile found'}), 404

        samples = FaceSample.query.filter_by(face_profile_id=profile.id).all()

        return jsonify({
            'success': True,
            'profile': {
                'id': profile.id,
                'person_type': profile.person_type,
                'person_id': profile.person_id,
                'model_version': profile.model_version,
                'model_name': profile.model_name,
                'created_at': profile.created_at.isoformat(),
                'samples_count': len(samples)
            },
            'samples': [{
                'id': s.id,
                'pose': s.pose,
                'quality_score': s.quality_score,
                'captured_at': s.captured_at.isoformat()
            } for s in samples]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/face-profiles', methods=['POST'])
def create_face_profile():
    try:
        data = request.json
        profile = FaceProfile(
            person_type=data.get('person_type'),
            person_id=data.get('person_id'),
            model_version=data.get('model_version', 'face-api.js'),
            model_name=data.get('model_name')
        )
        db.session.add(profile)
        db.session.commit()

        # Add samples if provided
        samples = data.get('samples', [])
        for sample_data in samples:
            sample = FaceSample(
                face_profile_id=profile.id,
                embedding=sample_data.get('embedding'),
                pose=sample_data.get('pose'),
                quality_score=sample_data.get('quality_score', 0.0)
            )
            db.session.add(sample)

        db.session.commit()

        return jsonify({'success': True, 'id': profile.id, 'samples_count': len(samples)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/face-profiles/<int:profile_id>', methods=['PUT'])
def update_face_profile(profile_id):
    try:
        data = request.json
        profile = FaceProfile.query.get_or_404(profile_id)

        profile.model_version = data.get('model_version', profile.model_version)
        profile.model_name = data.get('model_name', profile.model_name)

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/face-profiles/<int:profile_id>', methods=['DELETE'])
def delete_face_profile(profile_id):
    try:
        profile = FaceProfile.query.get_or_404(profile_id)
        db.session.delete(profile)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== Face Recognition ====================

@app.route('/api/face-recognition/recognize', methods=['POST'])
def recognize_face():
    try:
        data = request.json
        embedding = data.get('embedding')  # 128-dimensional vector

        if not embedding or len(embedding) != 128:
            return jsonify({'error': 'Invalid embedding - must be 128-dimensional vector'}), 400

        # Get all face profiles
        profiles = FaceProfile.query.all()
        best_match = None
        best_distance = float('inf')

        for profile in profiles:
            samples = FaceSample.query.filter_by(face_profile_id=profile.id).all()

            for sample in samples:
                sample_embedding = sample.embedding
                distance = euclidean_distance(embedding, sample_embedding)

                if distance < best_distance:
                    best_distance = distance
                    best_match = {
                        'profile_id': profile.id,
                        'person_type': profile.person_type,
                        'person_id': profile.person_id,
                        'sample_id': sample.id,
                        'distance': distance
                    }

        threshold = data.get('threshold', 0.6)

        if best_match and best_distance < threshold:
            # Get person details
            person = None
            if best_match['person_type'] == 'student':
                person = Student.query.get(best_match['person_id'])
            elif best_match['person_type'] == 'teacher':
                person = Teacher.query.get(best_match['person_id'])
            elif best_match['person_type'] == 'administrative':
                person = AdministrativeStaff.query.get(best_match['person_id'])
            elif best_match['person_type'] == 'security':
                person = SecurityStaff.query.get(best_match['person_id'])
            elif best_match['person_type'] == 'service':
                person = ServiceStaff.query.get(best_match['person_id'])

            return jsonify({
                'success': True,
                'matched': True,
                'person': {
                    'id': person.id if person else None,
                    'name': person.name if person else 'Unknown',
                    'type': best_match['person_type']
                },
                'distance': best_distance,
                'confidence': max(0, 1 - (best_distance / threshold)),
                'profile_id': best_match['profile_id']
            })
        else:
            return jsonify({
                'success': True,
                'matched': False,
                'reason': 'No match found',
                'distance': best_distance if best_match else None
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def euclidean_distance(embedding1, embedding2):
    if not embedding1 or not embedding2 or len(embedding1) != len(embedding2):
        return float('inf')

    sum_sq = sum((a - b) ** 2 for a, b in zip(embedding1, embedding2))
    return sum_sq ** 0.5

# ==================== Initialize Data ====================

def initialize_data():
    # Check if admin exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password='12345',
            type='admin',
            name='المدير العام'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created")
    
    # Check if stages exist
    if Stage.query.count() == 0:
        stages = [
            Stage(name='المرحلة الأولى'),
            Stage(name='المرحلة الثانية'),
            Stage(name='المرحلة الثالثة'),
            Stage(name='المرحلة الرابعة'),
            Stage(name='المرحلة الخامسة'),
            Stage(name='المرحلة السادسة')
        ]
        for stage in stages:
            db.session.add(stage)
        db.session.commit()
        print("Default stages created")

if __name__ == '__main__':
    initialize_data()
    app.run(debug=True, port=5000)
