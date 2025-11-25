# 💳 Stripe Rebilling Frontend

Modern, minimalist dark-themed dashboard for batch charging Stripe customers.

## Features

✨ **Modern Dark Theme** - Beautiful dark UI with clean minimalist design  
⚡ **Real-time Processing** - Live updates during charging  
📊 **Detailed Results** - Full payment details with card information  
🚫 **Auto-Skip** - Automatically skips Link, Google Pay, Apple Pay  
📱 **Responsive** - Works on desktop and mobile  
🎯 **Single Page** - Everything in one view  

## Quick Start

### Option 1: Simple HTTP Server (Recommended)
```bash
python3 -m http.server 8000
```

Then open: `http://localhost:8000`

### Option 2: Any Web Server
Simply serve the `index.html` file with any web server.

## Configuration

No build process required! This is a pure HTML/CSS/JavaScript app using:
- React 18 (via CDN)
- Babel Standalone (for JSX)
- No npm, no webpack, no build tools needed

## Setup

1. **Start the backend server** (required):
   ```bash
   cd backend
   python3 server.py
   ```
   Backend runs on `http://localhost:5001`

2. **Start the frontend**:
   ```bash
   cd frontend
   python3 -m http.server 8000
   ```
   Frontend runs on `http://localhost:8000`

3. **Open in browser**: `http://localhost:8000`

## Usage

1. **Enter Stripe API Key**
   - Get from https://dashboard.stripe.com/apikeys
   - Test mode: `sk_test_...`
   - Live mode: `sk_live_...`

2. **Configure Charge Settings**
   - Amount (dollars)
   - Currency (USD, EUR, GBP, CAD, AUD)
   - Description
   - Max customers (0 = all)
   - Delay between charges (seconds)

3. **Start Charging**
   - Click "Start Charging" button
   - Watch real-time progress
   - View detailed results

## Payment Filtering

The system **automatically skips**:
- 🚫 Link payment methods
- 🚫 Google Pay
- 🚫 Apple Pay

Only regular card payments are processed.

## Results Display

After charging, you'll see:
- ✅ Successful charges with full details
- 💳 Card brand and last 4 digits
- 🆔 Charge ID and timestamp
- 💰 Amount and currency
- ❌ Failed charges with error details
- 📊 Statistics summary

## Browser Support

Works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## API Backend

This frontend connects to the Flask backend API:
- Backend URL: `http://localhost:5001`
- All API calls are CORS-enabled
- Stripe API key sent securely to backend only

## Customization

To customize colors, edit the CSS in `index.html`:
- Dark background: `#0f172a`
- Card background: `#1e293b`
- Accent color: `#667eea`
- Success color: `#10b981`
- Error color: `#ef4444`

## Security

✅ API keys never stored in browser  
✅ All charges processed server-side  
✅ CORS enabled for local development  
✅ No external dependencies (except React CDN)  

## License

MIT

