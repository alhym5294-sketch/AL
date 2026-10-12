// Face Storage Manager
// إدارة تخزين بيانات الوجه (MySQL أو localStorage)

class FaceStorageManager {
    constructor() {
        this.storageType = FACE_CONFIG.STORAGE.TYPE;
        this.apiUrl = FACE_CONFIG.STORAGE.API_URL;
    }

    // حفظ بيانات الوجه
    async saveFaceData(personType, personId, faceData) {
        if (this.storageType === 'mysql') {
            return await this.saveToMySQL(personType, personId, faceData);
        } else {
            return this.saveToLocal(personType, personId, faceData);
        }
    }

    // حفظ في MySQL
    async saveToMySQL(personType, personId, faceData) {
        try {
            const response = await fetch(`${this.apiUrl}/api/face-profiles`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    person_type: personType,
                    person_id: personId,
                    model_version: faceData.model,
                    model_name: faceData.model,
                    samples: faceData.samples || []
                })
            });

            const result = await response.json();

            if (result.success) {
                console.log('✅ Face data saved to MySQL:', result);
                return { success: true, id: result.id, samples_count: result.samples_count };
            } else {
                console.error('❌ Failed to save to MySQL:', result);
                return { success: false, error: result.error };
            }
        } catch (error) {
            console.error('❌ Error saving to MySQL:', error);
            // Fallback to localStorage if MySQL fails
            console.log('⚠️ Fallback to localStorage');
            return this.saveToLocal(personType, personId, faceData);
        }
    }

    // حفظ في localStorage
    saveToLocal(personType, personId, faceData) {
        try {
            const key = this.getLocalKey(personType, personId);
            localStorage.setItem(key, JSON.stringify(faceData));
            console.log('✅ Face data saved to localStorage:', key);
            return { success: true, storage: 'local' };
        } catch (error) {
            console.error('❌ Error saving to localStorage:', error);
            return { success: false, error: error.message };
        }
    }

    // قراءة بيانات الوجه
    async getFaceData(personType, personId) {
        if (this.storageType === 'mysql') {
            return await this.getFromMySQL(personType, personId);
        } else {
            return this.getFromLocal(personType, personId);
        }
    }

    // قراءة من MySQL
    async getFromMySQL(personType, personId) {
        try {
            const response = await fetch(`${this.apiUrl}/api/face-profiles/${personType}/${personId}`);
            const result = await response.json();

            if (result.success) {
                // تحميل العينات
                const samples = result.samples;
                const faceData = {
                    version: 2,
                    model: result.profile.model_version,
                    samples: samples.map(s => ({
                        embedding: s.embedding,
                        pose: s.pose,
                        quality: s.quality_score,
                        capturedAt: s.captured_at
                    })),
                    createdAt: result.profile.created_at
                };
                console.log('✅ Face data loaded from MySQL');
                return faceData;
            } else {
                console.log('⚠️ No face profile in MySQL, checking localStorage');
                return this.getFromLocal(personType, personId);
            }
        } catch (error) {
            console.error('❌ Error loading from MySQL:', error);
            return this.getFromLocal(personType, personId);
        }
    }

    // قراءة من localStorage
    getFromLocal(personType, personId) {
        try {
            const key = this.getLocalKey(personType, personId);
            const data = localStorage.getItem(key);

            if (data) {
                const faceData = JSON.parse(data);
                console.log('✅ Face data loaded from localStorage:', key);
                return faceData;
            }

            console.log('⚠️ No face data found');
            return null;
        } catch (error) {
            console.error('❌ Error loading from localStorage:', error);
            return null;
        }
    }

    // التعرف على الوجه
    async recognizeFace(embedding) {
        if (this.storageType === 'mysql') {
            return await this.recognizeFromMySQL(embedding);
        } else {
            return this.recognizeFromLocal(embedding);
        }
    }

    // التعرف من MySQL
    async recognizeFromMySQL(embedding) {
        try {
            const response = await fetch(`${this.apiUrl}/api/face-recognition/recognize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    embedding: embedding,
                    threshold: FACE_CONFIG.RECOGNITION.THRESHOLD
                })
            });

            const result = await response.json();

            if (result.success) {
                console.log('✅ Recognition result from MySQL:', result);
                return result;
            } else {
                console.error('❌ Recognition failed:', result);
                return { matched: false, reason: result.error };
            }
        } catch (error) {
            console.error('❌ Error recognizing from MySQL:', error);
            return { matched: false, reason: error.message };
        }
    }

    // التعرف من localStorage
    recognizeFromLocal(embedding) {
        try {
            // البحث في جميع المستخدمين في localStorage
            const faceDatabase = [];

            // الطلاب
            const students = JSON.parse(localStorage.getItem('muq_students') || '[]');
            students.forEach(student => {
                if (student.faceData && student.faceData.version === 2) {
                    faceDatabase.push({
                        type: 'student',
                        id: student.id,
                        name: student.name,
                        faceData: student.faceData
                    });
                }
            });

            // المدرسين
            const teachers = JSON.parse(localStorage.getItem('muq_teachers') || '[]');
            teachers.forEach(teacher => {
                if (teacher.faceData && teacher.faceData.version === 2) {
                    faceDatabase.push({
                        type: 'teacher',
                        id: teacher.id,
                        name: teacher.name,
                        faceData: teacher.faceData
                    });
                }
            });

            // الموظفين
            ['administrative', 'security', 'service'].forEach(type => {
                const staff = JSON.parse(localStorage.getItem(`muq_${type}_staff`) || '[]');
                staff.forEach(person => {
                    if (person.faceData && person.faceData.version === 2) {
                        faceDatabase.push({
                            type: type,
                            id: person.id,
                            name: person.name,
                            faceData: person.faceData
                        });
                    }
                });
            });

            // البحث عن أفضل تطابق
            let bestMatch = null;
            let bestDistance = Infinity;

            for (const person of faceDatabase) {
                for (const sample of person.faceData.samples) {
                    const distance = faceEngine.euclideanDistance(embedding, sample.embedding);
                    if (distance < bestDistance) {
                        bestDistance = distance;
                        bestMatch = person;
                    }
                }
            }

            const threshold = FACE_CONFIG.RECOGNITION.THRESHOLD;

            if (bestMatch && bestDistance < threshold) {
                return {
                    matched: true,
                    person: bestMatch,
                    distance: bestDistance,
                    confidence: Math.max(0, 1 - (bestDistance / threshold))
                };
            }

            return {
                matched: false,
                reason: 'No match found',
                distance: bestDistance
            };
        } catch (error) {
            console.error('❌ Error recognizing from local:', error);
            return { matched: false, reason: error.message };
        }
    }

    // الحصول على مفتاح localStorage
    getLocalKey(personType, personId) {
        return `${FACE_CONFIG.STORAGE.LOCAL_KEY_PREFIX}face_${personType}_${personId}`;
    }

    // التحقق من هوية محددة
    async verifyIdentity(personType, personId, embedding) {
        const faceData = await this.getFaceData(personType, personId);

        if (!faceData || faceData.version !== 2) {
            return {
                verified: false,
                reason: 'No face data found or old version'
            };
        }

        let bestDistance = Infinity;

        for (const sample of faceData.samples) {
            const distance = faceEngine.euclideanDistance(embedding, sample.embedding);
            if (distance < bestDistance) {
                bestDistance = distance;
            }
        }

        const threshold = FACE_CONFIG.RECOGNITION.THRESHOLD;

        return {
            verified: bestDistance < threshold,
            distance: bestDistance,
            confidence: bestDistance < threshold ? Math.max(0, 1 - (bestDistance / threshold)) : 0
        };
    }
}

// إنشاء نسخة واحدة من مدير التخزين
const faceStorage = new FaceStorageManager();
