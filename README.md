# YouTube Transcript Backend

Small server that fetches transcripts for your Android app. Deploy it free on Render.com.

## Deploy to Render (free)

1. Go to https://render.com and sign up (free, no credit card needed for this tier).
2. Push this `transcript-backend` folder to a new GitHub repo (or use Render's
   "Deploy from a public Git repo" if you don't want to use GitHub — see
   alternative below).
3. On Render: **New +** → **Web Service** → connect your repo.
4. Settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free
5. Click **Create Web Service**. Wait for it to build and deploy (a few minutes).
6. Render gives you a URL like `https://your-app-name.onrender.com` — copy it.
7. Test it in a browser: `https://your-app-name.onrender.com/transcript?video_id=dQw4w9WgXcQ`
   You should see JSON with transcript segments.

⚠️ Free Render instances sleep after 15 min of inactivity and take ~30-50s to
wake up on the next request. That's normal — your Android app will just see
a slow first response after idle periods.

## Alternative: no GitHub account

If you don't want to use GitHub, you can zip this folder and deploy via
Render's "Upload files" flow, or use Railway.app / PythonAnywhere, which
have similar free tiers and dashboards.
