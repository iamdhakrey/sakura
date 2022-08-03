
# Info

**Sakura** is a web based discord bot. It is a simple bot that can be used to manage your server. It is currently in development and is not yet fully functional. It is not yet a fully featured bot.

As of now, it can support the following things:

- [x] Manage your server
- [x] Manage your server's roles
- [x] Manage your server's channels
- [x] Fun commands
- [x] Moderation commands
- [x] Welcome messages and role assignment
- [ ] Music commnads
- [ ] Web based configuration
- [ ] Custom commands

![Sakura](static/images/sakura.webp  "Sakura")

## Setup

- copy  settings_sample.ini to settings.ini file

- edit settings.ini file and change variable

- make migration

```bash
python manage.py makemigrations
```

- migrate

```bash
python manage.py migrate
```

- Run Server

```bash
python manage.py runserver
```

- Run Sakura Bot

```bash
python manage.py run-sakura
```
