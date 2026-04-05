"""
Daily Middle East News Briefing Bot
Scrapes news → Summarizes with GPT → Emails to you
"""

import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from openai import OpenAI


# ============================================================
# STEP 1: Web Scraper
# ============================================================

def fetch_website_contents(url):
    """Scrape text content from a website URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove scripts, styles, nav, footer
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)


# ============================================================
# STEP 2: News Sources (Middle East focused)
# ============================================================

NEWS_SOURCES = {
    "Al Jazeera": "https://www.aljazeera.com/middle-east",
    "BBC Middle East": "https://www.bbc.com/news/world/middle_east",
    "Reuters Middle East": "https://www.reuters.com/world/middle-east/",
}


def scrape_all_sources():
    """Scrape all news sources and return their content."""
    scraped = {}
    for name, url in NEWS_SOURCES.items():
        try:
            content = fetch_website_contents(url)
            scraped[name] = content[:3000]  # Limit to stay within token limits
            print(f"  ✅ {name} — {len(content)} chars")
        except Exception as e:
            print(f"  ❌ {name} — {e}")
    return scraped


# ============================================================
# STEP 3: Prompts (System + User)
# ============================================================

SYSTEM_PROMPT = """
You are a professional Middle East news analyst and daily briefing writer.
Your job is to analyze raw website content from news sources and produce a
clear, concise daily briefing focused ONLY on the Middle East region.

Focus on:
1. Wars, conflicts, military operations, ceasefires
2. Government policies, political decisions, elections
3. Diplomatic relations, treaties, sanctions
4. Humanitarian situations and refugee updates

Rules:
- Ignore ads, navigation menus, and unrelated content
- Group findings by topic (e.g., "Gaza Conflict", "Syria", "Iran Nuclear", "Yemen")
- Include which source reported each item
- Use bullet points for clarity
- Start with a one-line executive summary
- End with a "Key Developments to Watch" section
- Respond in well-formatted markdown
- Keep the total briefing under 500 words
"""

USER_PROMPT_TEMPLATE = """
Today's date: {date}

Below is scraped content from multiple Middle East news sources.
Analyze and create a focused daily briefing.

--- NEWS CONTENT ---
{content}
"""


# ============================================================
# STEP 4: Build messages (same pattern as Day 1!)
# ============================================================

def messages_for_news(scraped_news):
    """Build the messages list — same pattern as messages_for() from Day 1."""
    combined = ""
    for source_name, content in scraped_news.items():
        combined += f"\n\n=== {source_name} ===\n{content}"

    today = datetime.now().strftime("%A, %B %d, %Y")
    user_prompt = USER_PROMPT_TEMPLATE.format(date=today, content=combined)

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]


# ============================================================
# STEP 5: Call OpenAI
# ============================================================

def generate_briefing(scraped_news):
    """Send to GPT and get the briefing back."""
    client = OpenAI()
    messages = messages_for_news(scraped_news)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    return response.choices[0].message.content


# ============================================================
# STEP 6: Send Email
# ============================================================

def send_email(briefing, to_email):
    """Send the briefing via Gmail."""
    sender_email = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print("❌ Missing EMAIL_ADDRESS or EMAIL_APP_PASSWORD")
        return False

    today = datetime.now().strftime("%B %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📰 Middle East Briefing — {today}"
    msg["From"] = sender_email
    msg["To"] = to_email

    # Plain text
    msg.attach(MIMEText(briefing, "plain"))

    # HTML version
    html = briefing.replace("\n", "<br>")
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; 
                margin: 0 auto; padding: 20px; line-height: 1.6;">
        <h2 style="color: #1a5276; border-bottom: 2px solid #1a5276; padding-bottom: 10px;">
            📰 Middle East Daily Briefing — {today}
        </h2>
        {html}
        <hr style="margin-top: 30px; border: 1px solid #ddd;">
        <p style="color: #888; font-size: 12px;">
            Generated by your News Briefing Bot using OpenAI
        </p>
    </div>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Briefing sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


# ============================================================
# MAIN: Run everything
# ============================================================

def main():
    print("=" * 50)
    print("📰 MIDDLE EAST DAILY BRIEFING")
    print(f"📅 {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    print("=" * 50)

    # 1. Scrape
    print("\n📡 Scraping news sources...")
    scraped = scrape_all_sources()

    if not scraped:
        print("❌ No sources could be scraped. Exiting.")
        return

    # 2. Summarize
    print("\n🤖 Generating briefing with GPT...")
    briefing = generate_briefing(scraped)
    print("\n" + briefing)

    # 3. Email
    print("\n📧 Sending email...")
    to_email = os.getenv("TO_EMAIL", "amr.khairy20@gmail.com")
    send_email(briefing, to_email)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
