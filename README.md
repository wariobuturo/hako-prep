# Hako Interview Prep — Telegram Bot

## What you get
- `/start` → menu with Open Player button + episode download buttons
- `/ep1` to `/ep4` → sends audio file directly into Telegram chat
- `/all` → sends all 4 episodes at once
- **Audio Player Mini App** → opens the custom player inside Telegram
  - 10-sec forward/backward (on-screen buttons)
  - Earphone: 1× = Play/Pause · 2× = +10s · 3× = -10s
  - Background playback · Progress bar · Auto-advance

---

## Setup (15 minutes total)

### Step 1 — Create your bot (2 min)
1. Open Telegram → search **@BotFather**
2. Send `/newbot`
3. Choose a name e.g. `Hako Interview Prep`
4. Choose a username e.g. `hako_prep_bot`
5. Copy the **token** (looks like `123456:ABC-DEF...`)
6. Open `bot.py` → paste token into `BOT_TOKEN = "..."`

### Step 2 — Host the player on GitHub Pages (8 min)
1. Go to **github.com** → click **+** → **New repository**
2. Name it `hako-prep` → set to **Public** → click **Create**
3. Click **Add file** → **Upload files** → drag in `player.html`
4. Commit changes
5. Go to **Settings** → **Pages** → Source: **Deploy from branch** → branch: **main** → Save
6. Wait ~1 minute → your URL will be:
   `https://YOUR_USERNAME.github.io/hako-prep/player.html`
7. Open `bot.py` → paste this URL into `WEBAPP_URL = "..."`

### Step 3 — Register the Mini App with BotFather (2 min)
1. Go back to @BotFather → send `/mybots`
2. Select your bot → **Bot Settings** → **Menu Button** → **Configure menu button**
3. Enter your GitHub Pages URL
4. BotFather will confirm

### Step 4 — Add audio files
Put the 4 MP3 files in an `audio/` folder next to `bot.py`:
```
hako-prep/
  bot.py
  player.html
  README.md
  audio/
    ep01.mp3
    ep02.mp3
    ep03.mp3
    ep04.mp3
```

### Step 5 — Run the bot (1 min)
```bash
pip install python-telegram-bot
python bot.py
```
Bot runs on your computer. Keep terminal open while practicing.
To run permanently → deploy to a free server (Railway.app, Render.com).

---

## Earphone button mapping (in Mini App player)
| Press | Action |
|-------|--------|
| 1×    | Play / Pause |
| 2×    | +10 seconds forward |
| 3×    | −10 seconds back |

## Two ways to listen
| Method | Background | Earphone skip | 10-sec skip |
|--------|-----------|---------------|-------------|
| 📥 Download in chat | ✅ Yes | ✅ Yes (Telegram native) | ❌ No (drag bar only) |
| 🎙 Open Player (Mini App) | ✅ Yes* | ✅ Yes (2×/3× tap) | ✅ Yes |

*Background audio in Mini App works on Android (Chrome webview). On iOS it may pause when screen locks — use the download option on iPhone.
