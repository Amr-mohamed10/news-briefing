# 📰 Daily Middle East News Briefing Bot

Automatically scrapes news every morning, summarizes policies & conflicts with GPT, and emails you a clean briefing — all for **free** using GitHub Actions.

---

## How It Works

```
6:00 AM Cairo Time
      │
      ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Scrape      │ ──▶ │  GPT-4.1     │ ──▶ │  Email to   │
│  Al Jazeera  │     │  Summarize   │     │  Your Gmail │
│  BBC         │     │  Middle East │     │             │
│  Reuters     │     │  Focus       │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
```

---

## Setup (10 minutes, one time only)

### Step 1: Get a Gmail App Password

1. Go to https://myaccount.google.com/security
2. Make sure **2-Step Verification** is ON
3. Go to https://myaccount.google.com/apppasswords
4. App name: type `News Briefing Bot` → click **Create**
5. Copy the 16-character password (looks like: `abcd efgh ijkl mnop`)
6. Save it somewhere safe — you'll need it in Step 3

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `news-briefing`
3. Make it **Private**
4. Click **Create repository**
5. Upload all the files from this project:
   - `daily_news.py`
   - `requirements.txt`
   - `.github/workflows/daily_briefing.yml`

**Or use terminal:**
```bash
cd news-briefing
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/news-briefing.git
git push -u origin main
```

### Step 3: Add Secrets to GitHub

This is where you add your passwords — **encrypted and hidden**, nobody can see them.

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add these 3 secrets:

| Secret Name          | Value                                    |
|----------------------|------------------------------------------|
| `OPENAI_API_KEY`     | Your OpenAI API key (starts with sk-proj-) |
| `EMAIL_ADDRESS`      | amr.khairy20@gmail.com                   |
| `EMAIL_APP_PASSWORD` | The 16-char password from Step 1         |

### Step 4: Test It!

1. Go to your repo → **Actions** tab
2. Click **Daily Middle East Briefing** on the left
3. Click **Run workflow** → **Run workflow**
4. Wait 1-2 minutes
5. Check your email! 📬

---

## That's It!

Every morning at 6:00 AM Cairo time, you'll receive a clean email briefing about:
- 🔴 Wars and conflicts in the Middle East
- 📋 Government policies and political decisions
- 🤝 Diplomatic relations and treaties
- 🏥 Humanitarian updates

---

## Customize

**Change the time?** Edit `.github/workflows/daily_briefing.yml`:
```yaml
cron: "0 4 * * *"  # 4 AM UTC = 6 AM Cairo
```

**Add more sources?** Edit `NEWS_SOURCES` in `daily_news.py`:
```python
NEWS_SOURCES = {
    "Al Jazeera": "https://www.aljazeera.com/middle-east",
    "BBC Middle East": "https://www.bbc.com/news/world/middle_east",
    "Reuters Middle East": "https://www.reuters.com/world/middle-east/",
    "Your New Source": "https://example.com/news",  # add here
}
```

**Change language to Arabic?** Add this to the system prompt:
```
Respond in Arabic (العربية)
```

---

## Cost

- **GitHub Actions:** FREE (2,000 minutes/month on free plan, this uses ~2 min/day)
- **OpenAI API:** ~$0.01-0.03 per day with gpt-4.1-mini (less than $1/month)
