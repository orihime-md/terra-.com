import os
import time
import threading
import requests
from flask import Flask, jsonify

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
API = f'https://api.telegram.org/bot{TOKEN}' if TOKEN else ''
IMAGE = os.path.join(os.path.dirname(__file__), 'assets', 'ff-menu-wide.jpg')
app = Flask(__name__)

@app.get('/')
def health():
    return jsonify(service='Terra% Telegram test bot', status='online', bot_token_configured=bool(TOKEN))

@app.get('/health')
def health_check():
    return jsonify(status='ok'), 200


def api(method, **kwargs):
    response = requests.post(f'{API}/{method}', data=kwargs, timeout=40)
    response.raise_for_status()
    result = response.json()
    if not result.get('ok'):
        raise RuntimeError(result.get('description', 'Telegram API error'))
    return result.get('result')


def send_test(chat_id):
    keyboard = {
        'inline_keyboard': [
            [{'text': '🎮 Free Fire Menu', 'callback_data': 'ff_menu'}, {'text': '🧪 Test Button', 'callback_data': 'test'}],
            [{'text': '📱 Full-width image test', 'callback_data': 'image_test'}],
            [{'text': 'ℹ️ About this test bot', 'callback_data': 'about'}]
        ]
    }
    with open(IMAGE, 'rb') as photo:
        api('sendPhoto', chat_id=chat_id, photo=photo,
            caption='TERRA% — WIDE IMAGE TEST\n\nThis sample uses the wide Free Fire menu artwork. Telegram controls the chat bubble alignment; bots cannot force normal messages to the center.',
            reply_markup=__import__('json').dumps(keyboard))


def polling():
    if not TOKEN:
        print('ERROR: TELEGRAM_BOT_TOKEN Render environment variable is missing.', flush=True)
        return
    offset = 0
    print('Terra% bot polling started.', flush=True)
    while True:
        try:
            updates = requests.get(f'{API}/getUpdates', params={'offset': offset, 'timeout': 25}, timeout=35).json()
            if not updates.get('ok'):
                print('getUpdates error:', updates.get('description'), flush=True)
                time.sleep(4)
                continue
            for update in updates.get('result', []):
                offset = update['update_id'] + 1
                try:
                    if 'message' in update:
                        msg = update['message']
                        chat_id = msg['chat']['id']
                        text = (msg.get('text') or '').strip().lower()
                        if text.startswith('/start') or text.startswith('/menu') or text.startswith('/test'):
                            send_test(chat_id)
                        else:
                            api('sendMessage', chat_id=chat_id, text='Send /start to view the wide-image and button-layout test.')
                    elif 'callback_query' in update:
                        cb = update['callback_query']
                        api('answerCallbackQuery', callback_query_id=cb['id'], text='Test button received!')
                        data = cb.get('data', '')
                        chat_id = cb['message']['chat']['id']
                        if data == 'about':
                            api('sendMessage', chat_id=chat_id, text='Terra% is a separate demo bot testing wide Telegram photo messages and inline keyboard rows.')
                        elif data in ('ff_menu', 'test', 'image_test'):
                            send_test(chat_id)
                except Exception as e:
                    print('Update handling error:', repr(e), flush=True)
        except Exception as e:
            print('Polling connection error:', repr(e), flush=True)
            time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=polling, daemon=True).start()
    port = int(os.getenv('PORT', '10000'))
    app.run(host='0.0.0.0', port=port)
