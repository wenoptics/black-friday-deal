# Local Development 

Local Development with ngrok, before deploy on AWS.

## Start local Dev Server (Flask)

`$` `python api_handler.py`

```text
 * Serving Flask app "api_handler" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 333-190-202
```

## Expose local HTTP Application with ngrok

Expose port 5000

`$` `ngrok http 5000`

## Register webhook on Telegram for messages

```bash
https://api.telegram.org/bot${BOT_TOKEN}/setWebHook?url=${ngrok_url}/telegram_bot/local
```
