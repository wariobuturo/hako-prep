"""
Hako Interview Prep – Telegram Bot
====================================
Commands:
  /start   – Main menu
  /ep1-4   – Send individual episode audio
  /all     – Send all 4 episodes
  /help    – Instructions

Setup:
  1. Create bot via @BotFather → copy token
  2. Set BOT_TOKEN below
  3. Host player.html on GitHub Pages → set WEBAPP_URL
  4. pip install python-telegram-bot
  5. python bot.py
"""

import logging
import os
from pathlib import Path

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN  = "8966991623:AAE-tXo583kbsKUrZXcmKrCYikbi2JXcYcE"       # From @BotFather
WEBAPP_URL = "wariobuturo.github.io/hako-prep/player.html"     # e.g. https://yourusername.github.io/hako-prep/player.html

# Path to the 4 enhanced MP3 files (same folder as this script)
AUDIO_DIR = Path(__file__).parent / "audio"

EPISODES = [
    {
        "cmd":   "ep1",
        "title": "Ep 1 – Vorstellung & Motivation",
        "file":  "ep01.mp3",
        "desc":  "Selbstvorstellung, Wechsel in die Konstruktion, Motivation (2:46)",
    },
    {
        "cmd":   "ep2",
        "title": "Ep 2 – Die Bachelorarbeit",
        "file":  "ep02.mp3",
        "desc":  "Projektbeschreibung, Software, FEA-Ergebnisse, Parallele zu Hako (3:05)",
    },
    {
        "cmd":   "ep3",
        "title": "Ep 3 – Technische Fragen",
        "file":  "ep03.mp3",
        "desc":  "Bauteilverbesserung, Werkstoffauswahl, Ergonomie, autonome Maschinen (2:59)",
    },
    {
        "cmd":   "ep4",
        "title": "Ep 4 – Persönliche Fragen & Abschluss",
        "file":  "ep04.mp3",
        "desc":  "Deutschkenntnisse, Umzug, Stärken/Schwächen, eigene Fragen (2:59)",
    },
]

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ─── KEYBOARDS ────────────────────────────────────────────────────────────────
def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🎙 Audio Player öffnen  (10-sek Skip + Kopfhörer)",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )],
        [
            InlineKeyboardButton("📥 Ep 1", callback_data="ep1"),
            InlineKeyboardButton("📥 Ep 2", callback_data="ep2"),
            InlineKeyboardButton("📥 Ep 3", callback_data="ep3"),
            InlineKeyboardButton("📥 Ep 4", callback_data="ep4"),
        ],
        [InlineKeyboardButton("📦 Alle 4 Episoden senden", callback_data="all")],
    ])


# ─── HANDLERS ─────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "🎙 *Hako Interview Prep*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Vorbereitung für das Gespräch mit *Ricardo Ruiz Porath*\n"
        "Product Line Manager – Cleaning Technology, Hako GmbH\n\n"
        "🎧 *Kopfhörer-Steuerung (im Player):*\n"
        "• 1× Taste = Play / Pause\n"
        "• 2× Taste = +10 Sekunden vor\n"
        "• 3× Taste = −10 Sekunden zurück\n\n"
        "Wähle eine Option:"
    )
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📖 *Anleitung*\n\n"
        "• /start – Hauptmenü\n"
        "• /ep1 bis /ep4 – Episode direkt herunterladen\n"
        "• /all – Alle 4 Episoden auf einmal\n\n"
        "🎙 *Audio Player* (via Schaltfläche):\n"
        "Öffnet den eingebetteten Player mit\n"
        "10-sek-Skip, Fortschrittsbalken und\n"
        "Kopfhörer-Steuerung. Bildschirm kann\n"
        "gesperrt werden.\n\n"
        "📥 *Direkt herunterladen*:\n"
        "Telegram spielt die Audiodatei nativ ab.\n"
        "Hintergrund-Wiedergabe und Kopfhörer\n"
        "funktionieren automatisch über die\n"
        "Telegram-App."
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def send_episode(update: Update, context: ContextTypes.DEFAULT_TYPE,
                        ep_cmd: str) -> None:
    """Send a single episode audio file."""
    ep = next((e for e in EPISODES if e["cmd"] == ep_cmd), None)
    if not ep:
        return

    # Works from both command and callback query
    msg = update.message or update.callback_query.message
    chat_id = msg.chat_id

    audio_path = AUDIO_DIR / ep["file"]
    if not audio_path.exists():
        await context.bot.send_message(
            chat_id,
            f"⚠️ Audiodatei nicht gefunden: {ep['file']}\n"
            "Bitte stelle sicher, dass die MP3-Dateien im 'audio/' Ordner liegen.",
        )
        return

    await context.bot.send_chat_action(chat_id, "upload_audio")
    with open(audio_path, "rb") as f:
        await context.bot.send_audio(
            chat_id=chat_id,
            audio=f,
            title=ep["title"],
            performer="Hako Interview Prep",
            caption=f"🎙 *{ep['title']}*\n{ep['desc']}",
            parse_mode="Markdown",
        )


async def cmd_ep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ep1 /ep2 /ep3 /ep4 commands."""
    cmd = update.message.text.lstrip("/").split()[0].lower()
    await send_episode(update, context, cmd)


async def cmd_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send all episodes."""
    await update.message.reply_text("📦 Sende alle 4 Episoden…")
    for ep in EPISODES:
        await send_episode(update, context, ep["cmd"])


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button presses."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "all":
        await query.message.reply_text("📦 Sende alle 4 Episoden…")
        for ep in EPISODES:
            await send_episode(update, context, ep["cmd"])
    else:
        await send_episode(update, context, data)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",  cmd_start))
    app.add_handler(CommandHandler("help",   cmd_help))
    app.add_handler(CommandHandler("all",    cmd_all))
    for ep in EPISODES:
        app.add_handler(CommandHandler(ep["cmd"], cmd_ep))
    app.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("Bot is running…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
