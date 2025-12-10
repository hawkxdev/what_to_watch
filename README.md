# What to Watch

Flask web app for sharing movie opinions with Dropbox image upload support.

## Tech Stack

- [Python 3.12](https://www.python.org/)
- [Flask 3.0](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/)
- [aiohttp](https://docs.aiohttp.org/) — async Dropbox uploads
- [uv](https://docs.astral.sh/uv/) — package manager

## Getting Started

Clone the repository:

```bash
git clone https://github.com/hawkxdev/what_to_watch.git
cd what_to_watch
```

Install dependencies:

```bash
uv sync
```

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your values. To get `DROPBOX_TOKEN`:
1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Create app → Scoped access → Full Dropbox
3. Generate access token in Settings

Apply migrations:

```bash
uv run flask db upgrade
```

Run the project:

```bash
uv run flask run
```

App will be available at http://127.0.0.1:5000
