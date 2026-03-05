# Deploy PH Prefix API to Railway (Free Tier)

## Prerequisites

- GitHub account (you already have: ClawKazmu)
- Railway account (free signup at railway.app)
- Git installed

## Steps (5 minutes)

1. **Sign up / log in to Railway**
   - Go to https://railway.app
   - Click "Login" → "Continue with GitHub"
   - Authorize Railway to access your repos

2. **Create a new project**
   - Click "New Project" (top right)
   - Select "Deploy from GitHub repo"
   - Choose `ClawKazmu/ph-prefix-api` from the list
   - Railway auto-detects Python and sets up build

3. **Configure environment variables (optional)**
   - Go to "Variables" tab
   - Add `PORT=8000` (Railway sets this automatically, but good to have)
   - Add any other config if needed later

4. **Deploy**
   - Click "Deploy Now"
   - Railway will:
     - Install dependencies (`pip install -r requirements.txt`)
     - Run build (NixPacks)
     - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Wait ~2-3 minutes

5. **Get your live URL**
   - After successful deploy, go to "Settings" → "Domains"
   - You'll get a random subdomain like `https://ph-prefix-api.up.railway.app`
   - (Optional) Add custom domain later

6. **Test the API**
   - Visit: `https://your-url.up.railway.app/health`
   - Should return: `{"status":"ok","timestamp":"..."}`
   - Try lookup: `https://your-url.up.railway.app/api/v1/lookup?number=09171234567`

7. **Monitor usage**
   - Railway free tier includes $5 credit/month
   - Our API is lightweight—should fit within free tier
   - Check "Metrics" tab for request count

## Custom Domain (Optional, later)

When you're ready to use a custom domain (e.g., `api.clawkazmu.dev`):

1. Buy domain (₱500–1,000/year)
2. In Railway: Settings → Domains → Add Domain
3. Set CNAME to `your-project.up.railway.app`
4. Enable HTTPS (automatic via Railway)

## Billing & Limits

- **Free tier:** $5 credit monthly (enough for ~100,000 requests)
- **Sleep:** After 30 days of inactivity, Railway may suspend (wake by visiting)
- **Upgrade:** $5/month for always-on

## Updating the API

- Push changes to GitHub `main` branch
- Railway auto-deploys on new commits
- Check "Deployments" tab for build logs

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails (pip install) | Ensure `requirements.txt` has fastapi and uvicorn |
| 502 Bad Gateway | Check logs: app crashed? Likely missing deps or port issue |
| Rate limit errors | Increase `MAX_REQUESTS_PER_MINUTE` in code |
| Need more requests | Upgrade Railway plan or optimize caching |

---

That's it! Deploy once and the API is live 24/7 for free.
