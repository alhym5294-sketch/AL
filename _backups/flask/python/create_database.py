"""
سكريبت إنشاء قاعدة بيانات MySQL والجداول
"""
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def create_database():
    """إنشاء قاعدة البيانات"""
    try:
        # الاتصال بـ MySQL بدون اسم قاعدة بيانات
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        
        # إنشاء قاعدة البيانات
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'muq_system')} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ قاعدة البيانات '{os.getenv('DB_NAME', 'muq_system')}' تم إنشاؤها بنجاح")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        return False
    
    return True

def create_tables():
    """إنشاء الجداول المخصصة للوجه"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'muq_system')
        )
        
        cursor = connection.cursor()
        
        # إنشاء جدول face_profiles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS face_profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                person_type VARCHAR(20) NOT NULL,
                person_id INT NOT NULL,
                model_version VARCHAR(50) DEFAULT 'face-api.js',
                model_name VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_person (person_type, person_id)
            )
        """)
        print("✅ جدول face_profiles تم إنشاؤه")
        
        # إنشاء جدول face_samples
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS face_samples (
                id INT AUTO_INCREMENT PRIMARY KEY,
                face_profile_id INT NOT NULL,
                embedding JSON NOT NULL,
                pose VARCHAR(20),
                quality_score FLOAT DEFAULT 0.0,
                captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (face_profile_id) REFERENCES face_profiles(id) ON DELETE CASCADE,
                INDEX idx_profile (face_profile_id)
            )
        """)
        print("✅ جدول face_samples تم إنشاؤه")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
    except Exception as e:
        print(f"❌ خطأ في إنشاء الجداول: {e}")
        return False

if __name__ == '__main__':
    if create_database():
        print("✅ تم إنشاء قاعدة البيانات بنجاح")
        if create_tables():
            print("✅ تم إنشاء الجداول بنجاح")
            print("الآن يمكنك تشغيل 'python app.py'")
        else:
            print("❌ فشل إنشاء الجداول")
    else:
        print("❌ فشل إنشاء قاعدة البيانات")
