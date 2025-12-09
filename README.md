# What to Watch

Flask web app for sharing movie opinions with Dropbox image upload support.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/hawkxdev/what_to_watch.git
cd what_to_watch
```

Install dependencies with uv:

```bash
uv sync
```

Create `.env` file from example:

```bash
cp .env.example .env
```

Edit `.env` with your values.

To get `DROPBOX_TOKEN`:
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
