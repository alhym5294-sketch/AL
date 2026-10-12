# MUQ Frontend

## Overview
This is the frontend for the MUQ attendance system with face recognition. It's a vanilla JavaScript/HTML/CSS application that communicates with the Django REST API backend.

## Structure
```
frontend/
├── HTML/           # HTML pages
├── Js/             # JavaScript modules
├── css/            # Stylesheets
└── index.html      # Entry point
```

## Pages

### Authentication
- `login.html` - Login page

### Dashboards
- `admin-dashboard.html` - Admin dashboard
- `teacher-dashboard.html` - Teacher dashboard
- `student-dashboard.html` - Student dashboard
- `staff-dashboard.html` - Staff dashboard

### Face Registration
- `face-registration-new.html` - Face registration for all users
- `student-face-registration-new.html` - Student face registration
- `teacher-face-registration-new.html` - Teacher face registration
- `staff-face-registration-new.html` - Staff face registration

### Other
- `attendance-report.html` - Attendance reports
- `gate-entry.html` - Gate entry with face recognition
- `monitoring-system.html` - Monitoring system
- `add-departments.html` - Department management

## JavaScript Modules

### Core
- `database.js` - Local storage database (legacy, being phased out)
- `api-client.js` - API client for Django backend
- `login.js` - Login logic
- `portal-auth.js` - Portal authentication

### Face Recognition
- `face-recognition-engine.js` - Face recognition engine
- `face-recognition.js` - Face recognition interface
- `face-config.js` - Face recognition configuration
- `face-storage.js` - Face data storage
- `face-registration.js` - Face registration logic
- `face-registration-new.js` - New face registration logic

### Dashboards
- `admin-dashboard.js` - Admin dashboard logic
- `teacher-dashboard.js` - Teacher dashboard logic
- `student-dashboard.js` - Student dashboard logic
- `staff-dashboard.js` - Staff dashboard logic

### Reports
- `attendance-report.js` - Attendance report generation
- `data-migration.js` - Data migration tool

### Database
- `database.js` - Local storage database
- `database-api.js` - Database API interface

## Configuration

### API URL
Update the API URL in `Js/api-client.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';  // Local development
// const API_BASE_URL = 'https://your-app.railway.app/api';  // Production
```

## Development

### Prerequisites
- Modern web browser (Chrome, Firefox, Edge)
- Python backend running (or deployed)

### Local Development

1. **Start the backend:**
   ```bash
   cd ../backend
   python manage.py runserver
   ```

2. **Open the frontend:**
   - Open `index.html` in your browser
   - Or use a local server (recommended):
     ```bash
     python -m http.server 8010
     ```

3. **Configure API URL:**
   - Edit `Js/api-client.js`
   - Set `API_BASE_URL` to your backend URL

## Deployment

### Static Hosting Options

1. **Netlify**
   - Connect your Git repository
   - Set publish directory to `frontend`
   - Deploy

2. **Vercel**
   - Connect your Git repository
   - Set output directory to `frontend`
   - Deploy

3. **GitHub Pages**
   - Push to GitHub
   - Enable GitHub Pages on your repository
   - Set source to `frontend` folder

### Environment Variables

If using a hosting service that supports environment variables:
- `VITE_API_URL` or `REACT_APP_API_URL` for the backend URL

## Features

### Authentication
- JWT-based authentication
- Token refresh
- Role-based access control

### Face Recognition
- Real-time face detection
- Face embedding extraction
- Face matching with database
- Anti-spoofing (blink detection)

### Dashboards
- User management
- Attendance tracking
- Schedule management
- Department/Stage/Branch hierarchy
- Report generation

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

Required features:
- WebRTC (camera access)
- ES6+ JavaScript
- LocalStorage
- Fetch API

## Security Notes

- HTTPS is required for camera access in production
- API tokens are stored in localStorage (consider HttpOnly cookies for production)
- CORS must be configured on the backend
- Face data is sent to the server for processing

## Migration to API

The frontend is currently transitioning from localStorage to the Django API:
- ✅ API client created (`api-client.js`)
- ✅ Authentication migrated to JWT
- ⏳ User management migration
- ⏳ Attendance tracking migration
- ⏳ Face recognition integration

## Troubleshooting

### Camera not working
- Check browser permissions
- Ensure HTTPS in production
- Verify WebRTC support

### API connection errors
- Check backend is running
- Verify API_BASE_URL configuration
- Check CORS settings on backend
- Check network connectivity

### Face recognition issues
- Ensure face-api.js models are loaded
- Check camera quality and lighting
- Verify face profile exists in database

## License

Proprietary - MUQ System
