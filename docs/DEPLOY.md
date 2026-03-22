# Deploy Guide — Get ConservaTwin Live in 10 Minutes

Everything is free tier. No credit card needed.

---

## Step 1: Push to GitHub

```bash
cd conservatwin-platform
git init
git add .
git commit -m "Initial release: ConservaTwin Platform MVP"
git branch -M main
git remote add origin https://github.com/Prithweeraj-Acharjee/conservatwin-platform.git
git push -u origin main
```

---

## Step 2: Deploy Backend to Render (Free)

1. Go to https://render.com and sign in with GitHub
2. Click **New** → **Web Service**
3. Connect your `conservatwin-platform` repo
4. Render will auto-detect the `render.yaml` — click **Apply**
5. Wait for build to complete (~2-3 minutes)
6. Your API is live at `https://conservatwin-platform-api.onrender.com`

**Note:** Free tier sleeps after 15min of inactivity. First request after sleep takes ~30s.

---

## Step 3: Deploy Frontend to Vercel (Free)

1. Go to https://vercel.com and sign in with GitHub
2. Click **Import Project** → select `conservatwin-platform`
3. Set **Root Directory** to `frontend`
4. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL` = `https://conservatwin-platform-api.onrender.com`
5. Click **Deploy**
6. Your frontend is live at `https://conservatwin-platform.vercel.app`

---

## Step 4: Seed Demo Data

```bash
# Hit the API to trigger database creation
curl https://conservatwin-platform-api.onrender.com/health

# Then seed demo data (run locally, pointing at remote API)
CONSERVATWIN_API=https://conservatwin-platform-api.onrender.com python -m backend.demo_seed
```

Or register a real museum:
```bash
curl -X POST https://conservatwin-platform-api.onrender.com/api/museums/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Toledo Museum of Art", "slug": "toledo-museum", "location": "Toledo, Ohio"}'
```

---

## Step 5: Share Your Links

- **Landing page:** https://conservatwin-platform.vercel.app
- **Live museum dashboard:** https://conservatwin-platform.vercel.app/museum/toledo-museum
- **API docs:** https://conservatwin-platform-api.onrender.com/docs
- **GitHub:** https://github.com/Prithweeraj-Acharjee/conservatwin-platform

---

## Custom Domain (Optional, $12/year)

1. Buy `conservatwin.org` from Namecheap or Cloudflare (~$12/year)
2. In Vercel: Settings → Domains → Add `conservatwin.org`
3. Update DNS as Vercel instructs
4. Now your pitch becomes: **"Visit conservatwin.org to see it live"**
