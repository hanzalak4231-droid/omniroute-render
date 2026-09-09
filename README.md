# OmniRoute Server - Render Deployment

## Quick Deploy to Render (Free Tier)

### Prerequisites
- GitHub account
- Render.com account (free)

### Step 1: Push Files to GitHub

1. Create a new GitHub repository: `omniroute-render`
2. Push these files:
   - `app.py` (this file)
   - `Procfile`
   - `requirements.txt`
   - `storage.sqlite.gz` (your database backup)

```bash
cd render-setup
git init
git add .
git commit -m "OmniRoute for Render"
git remote add origin https://github.com/YOUR-USERNAME/omniroute-render.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com and sign in with GitHub
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository `omniroute-render`
4. Configure:
   - **Name:** omniroute
   - **Region:** Oregon (or closest to you)
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. Click **"Create Web Service"**

### Step 3: Wait for Deployment

- First deploy takes ~3-5 minutes
- Check logs for "Database restored!" message

### Step 4: Access Your Server

- Get your URL: `https://omniroute-XXXX.onrender.com`
- Dashboard: `https://omniroute-XXXX.onrender.com/dashboard`

---

## Keep Alive (Prevent Sleep)

Render's **free tier sleeps after 15 min of inactivity**. To prevent this:

### Option A: Use Render Uptime Monitor (Free)

1. Go to Render Dashboard → Your Service → **Uptime**
2. Add health check: `https://YOUR-URL.onrender.com/health`
3. Set interval: **5 minutes**
4. Enable → Render keeps your service awake!

### Option B: Self-Ping (Already Included in app.py)

The `app.py` includes a self-ping feature that runs in the background to keep the service active.

---

## Troubleshooting

### "Service unavailable" after deployment
- Wait 2-3 minutes for first startup
- Check Build Logs in Render dashboard

### Database not loading
- Make sure `storage.sqlite.gz` is in the repo root
- Check deploy logs for "Database restored"

### Service sleeping
- Enable Uptime monitoring in Render dashboard
- Or upgrade to paid tier ($7/mo)

---

## Get Your API Endpoint

Once deployed, your OmniRoute API is at:
```
https://YOUR-APP-NAME.onrender.com/v1
```

### Example Usage

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR-OMNIROUTE-API-KEY",
    base_url="https://YOUR-APP-NAME.onrender.com/v1"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

## Your Database Contents

Your uploaded `storage.sqlite.gz` contains:
- ✅ 25 provider connections
- ✅ 5 model combos
- ✅ 5 API keys
- ✅ All settings and configurations

The service will automatically restore everything on startup!