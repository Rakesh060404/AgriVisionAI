# Environment Variables Setup

This document explains how to configure environment variables for both frontend and backend to ensure proper deployment.

## Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Gemini API Key for chatbot functionality
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Production Backend Settings

For production, update your `.env` file:

```env
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

**Important:** Never commit your `.env` file to version control. Add it to `.gitignore`.

## Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
# Backend API Base URL
# For development: http://localhost:5000
# For production: https://your-api-domain.com
VITE_API_BASE_URL=http://localhost:5000
```

### Production Frontend Settings

For production, set the API URL to your deployed backend:

```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

**Note:** In Vite, environment variables must be prefixed with `VITE_` to be accessible in the client code.

## Deployment Checklist

### Backend Deployment
- [ ] Set `GEMINI_API_KEY` in production environment
- [ ] Set `FLASK_DEBUG=False` for production
- [ ] Configure `FLASK_HOST` and `FLASK_PORT` appropriately
- [ ] Ensure model files are in `backend/models/` directory
- [ ] Use a production WSGI server (Gunicorn, uWSGI, etc.)

### Frontend Deployment
- [ ] Set `VITE_API_BASE_URL` to production backend URL
- [ ] Build the frontend: `npm run build`
- [ ] Deploy the `dist/` folder to your hosting service
- [ ] Ensure CORS is properly configured on the backend

## Security Notes

1. **Never commit `.env` files** - They contain sensitive information
2. **Use environment variables** in your hosting platform (Vercel, Heroku, AWS, etc.)
3. **Rotate API keys** if they are accidentally exposed
4. **Use HTTPS** in production for all API calls

## Example Deployment Platforms

### Vercel (Frontend)
Set environment variables in Vercel dashboard:
- `VITE_API_BASE_URL=https://your-backend-url.com`

### Heroku (Backend)
Set environment variables using Heroku CLI:
```bash
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set FLASK_DEBUG=False
```

### Docker
Use environment variables in `docker-compose.yml`:
```yaml
environment:
  - GEMINI_API_KEY=${GEMINI_API_KEY}
  - FLASK_DEBUG=False
```

