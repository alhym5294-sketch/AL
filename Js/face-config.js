// Face Recognition Configuration
// إعدادات مركزية لنظام التعرف على الوجه

const FACE_CONFIG = {
    // إعدادات التخزين
    STORAGE: {
        // نوع التخزين: 'local' أو 'mysql'
        TYPE: 'mysql', // MySQL: تخزين جميع البيانات في MySQL
        // إعدادات MySQL
        API_URL: 'http://localhost:5000',
        // إعدادات localStorage (fallback فقط)
        LOCAL_KEY_PREFIX: 'muq_'
    },

    // إعدادات التسجيل
    REGISTRATION: {
        TARGET_SAMPLES: 3, // العدد المستهدف من العينات
        MIN_QUALITY: 0.7, // الحد الأدنى لجودة العينة (0-1)
        CAPTURE_INTERVAL: 500, // الحد الأدنى بين التقاط الصور (ms)
        POSES: {
            front: 1,
            right_15: 1,
            left_15: 1
        }
    },

    // إعدادات التعرف
    RECOGNITION: {
        // Threshold للتعرف (Euclidean Distance)
        // القيم الأقل تعني تطابق أفضل
        THRESHOLD: 0.6, // قيمة تجريبية، تحتاج للاختبار
        // منع العينات المكررة
        DUPLICATE_DISTANCE_THRESHOLD: 0.3 // قيمة تجريبية
    },

    // إعدادات النماذج
    MODELS: {
        // مسارات نماذج face-api.js (CDN)
        MODELS_URL: 'https://justadudewhohacks.github.io/face-api.js/models',
        // النماذج المطلوبة
        SSD_MOBILENET_V1: 'ssd_mobilenetv1_model-weights_manifest.json',
        FACE_LANDMARK_68: 'face_landmark_68_model-weights_manifest.json',
        FACE_RECOGNITION: 'face_recognition_model-weights_manifest.json'
    },

    // إعدادات Liveness (تحدي بسيط فقط)
    LIVENESS: {
        ENABLED: true,
        BLINK_CHALLENGE: true,
        // ملاحظة: هذا ليس حماية حيوية كاملة
        // This is not full liveness detection
        MESSAGE: "تحدي بسيط للتحقق من الحيوية - ليس حماية ضد جميع أنواع spoofing"
    },

    // إعدادات الجودة
    QUALITY: {
        MIN_FACE_SIZE: 100, // الحد الأدنى لحجم الوجه (بكسل)
        MAX_FACE_SIZE: 400, // الحد الأقصى لحجم الوجه (بكسل)
        MIN_BRIGHTNESS: 50, // الحد الأدنى للإضاءة (0-255)
        MAX_BRIGHTNESS: 200, // الحد الأقصى للإضاءة (0-255)
        BLUR_THRESHOLD: 100 // حد الضبابية
    },

    // إعدادات الإطار
    FRAME: {
        WIDTH: 640,
        HEIGHT: 480,
        FACE_BOX_PADDING: 20
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FACE_CONFIG;
}
