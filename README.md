# Terra% — Telegram wide-image test bot

Small independent test bot using one wide Free Fire menu image from the supplied bot project.

## Telegram setup
1. In Telegram, open `@BotFather` and create a new bot.
2. The display name can be `Terra%`. Telegram usernames cannot contain `%`; choose an available username ending in `bot` (letters, numbers, underscores only).
3. Copy the token and set it in Render as `TELEGRAM_BOT_TOKEN`.
4. Deploy this folder/repository as a Render Web Service. `render.yaml` contains the service configuration.
5. Open your bot and send `/start`.

## Render environment variable
- `TELEGRAM_BOT_TOKEN` = the token supplied by BotFather (keep it private; never commit it).

Render supplies `PORT` automatically. The app serves a health endpoint at `/health` and uses Telegram long polling.

Note: Telegram's Bot API does not offer a parameter to center standard bot messages or force them to occupy the whole chat. The image is landscape (16:9), so Telegram can render it wide while preserving the complete image. Button row arrangement is configured in `terra.py`; button colors are controlled by Telegram's client, not the bot API.
