from flask import Flask, render_template_string

app = Flask(__name__)

# ==========================================
# CUSTOMIZE YOUR PROFILE & LINKS HERE
# ==========================================
USER_PROFILE = {
    "name": "Alex 'Pixel' Turner",
    "username": "@alex_pixel",
    "bio": "Game Developer • Indie Streamer • Pixel Artist",
    "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=AlexPixel",
    "sections": [
        {
            "category": "Social Media",
            "links": [
                {
                    "title": "Instagrame",
                    "subtitle": "Game Devlogs & Highlights",
                    "url": "https://www.instagram.com/gg_p4rince_sen?igsi=NWd3eWl5a2R0bnp2",
                    "icon": "📺",
                    "badge": "Subscribe",
                },
                {
                    "title": "Twitch",
                    "subtitle": "Live Coding & Gaming Streams",
                    "url": "https://twitch.tv/yourchannel",
                    "icon": "🟣",
                    "badge": "Live",
                },
                {
                    "title": "Discord Server",
                    "subtitle": "Community Chat & Playtests",
                    "url": "https://discord.gg/yourserver",
                    "icon": "💬",
                    "badge": "Join",
                },
                {
                    "title": "X / Twitter",
                    "subtitle": "Daily Updates & Pixel Art",
                    "url": "https://x.com/yourhandle",
                    "icon": "✖️",
                    "badge": None,
                },
            ],
        },
        {
            "category": "My Games & Gaming Profiles",
            "links": [
                {
                    "title": "Steam Profile",
                    "subtitle": "Wishlist My Upcoming Game",
                    "url": "https://store.steampowered.com",
                    "icon": "🎮",
                    "badge": "Wishlist",
                },
                {
                    "title": "Itch.io",
                    "subtitle": "Play Free Browser Prototypes",
                    "url": "https://itch.io",
                    "icon": "🕹️",
                    "badge": "Play Now",
                },
                {
                    "title": "Roblox Hub",
                    "subtitle": "Custom Community Obby",
                    "url": "https://roblox.com",
                    "icon": "🧱",
                    "badge": None,
                },
            ],
        },
    ],
}

# ==========================================
# HTML + CSS TEMPLATE (Rendered via Flask)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{ profile.name }} | Links</title>
  <style>
    :root {
      --bg: #090d16;
      --card-bg: #131b2e;
      --card-hover: #1c2742;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.25);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    body {
      background-color: var(--bg);
      color: var(--text-main);
      display: flex;
      justify-content: center;
      min-height: 100vh;
      padding: 48px 16px;
    }

    .container {
      width: 100%;
      max-width: 480px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 24px;
    }

    .profile-card {
      text-align: center;
    }

    .avatar {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      border: 3px solid var(--accent);
      box-shadow: 0 0 20px var(--accent-glow);
      margin-bottom: 12px;
      object-fit: cover;
      background-color: var(--card-bg);
    }

    .profile-card h1 {
      font-size: 1.5rem;
      font-weight: 700;
    }

    .username {
      color: var(--accent);
      font-size: 0.9rem;
      font-weight: 600;
      margin-top: 2px;
    }

    .bio {
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-top: 8px;
    }

    .section {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .section-title {
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--text-muted);
      font-weight: 700;
      margin-left: 4px;
    }

    .link-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--card-bg);
      border: 1px solid rgba(255, 255, 255, 0.06);
      padding: 14px 18px;
      border-radius: 12px;
      text-decoration: none;
      color: var(--text-main);
      transition: all 0.2s ease;
    }

    .link-item:hover {
      background: var(--card-hover);
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }

    .link-left {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .link-icon {
      font-size: 1.4rem;
    }

    .link-texts h3 {
      font-size: 0.95rem;
      font-weight: 600;
    }

    .link-texts p {
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    .badge {
      font-size: 0.75rem;
      font-weight: 600;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 4px 10px;
      border-radius: 999px;
      white-space: nowrap;
    }

    footer {
      margin-top: 12px;
      font-size: 0.8rem;
      color: var(--text-muted);
    }
  </style>
</head>
<body>

  <main class="container">
    <header class="profile-card">
      <img src="{{ profile.avatar_url }}" alt="Profile avatar" class="avatar" />
      <h1>{{ profile.name }}</h1>
      <div class="username">{{ profile.username }}</div>
      <p class="bio">{{ profile.bio }}</p>
    </header>

    {% for section in profile.sections %}
    <section class="section">
      <span class="section-title">{{ section.category }}</span>
      {% for link in section.links %}
      <a href="{{ link.url }}" target="_blank" rel="noopener noreferrer" class="link-item">
        <div class="link-left">
          <span class="link-icon">{{ link.icon }}</span>
          <div class="link-texts">
            <h3>{{ link.title }}</h3>
            {% if link.subtitle %}<p>{{ link.subtitle }}</p>{% endif %}
          </div>
        </div>
        {% if link.badge %}
        <span class="badge">{{ link.badge }}</span>
        {% endif %}
      </a>
      {% endfor %}
    </section>
    {% endfor %}

    <footer>
      Powered by Flask
    </footer>
  </main>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, profile=USER_PROFILE)


if __name__ == "__main__":
    # Runs the local development server
    app.run(debug=True, port=5000)