"""Web views for displaying and adding opinions."""
from random import randrange

from flask import abort, flash, redirect, render_template, url_for
from werkzeug.wrappers import Response

from . import app, db
from .forms import OpinionForm
from .models import Opinion
from .dropbox import async_upload_files_to_dropbox


def random_opinion() -> Opinion | None:
    """Return a random opinion from the database."""
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)  # nosec B311
        opinion = Opinion.query.offset(offset_value).first()
        return opinion
    return None


@app.route('/')
def index_view() -> str:
    """Display a random opinion on the home page."""
    quantity = Opinion.query.count()
    if not quantity:
        abort(500)
    offset_value = randrange(quantity)  # nosec B311
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
async def add_opinion_view() -> str | Response:
    """Handle opinion submission with optional image upload to Dropbox."""
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        urls = await async_upload_files_to_dropbox(form.images.data)
        opinion = Opinion(
            title=form.title.data,
            text=text,
            source=form.source.data,
            images=urls
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id: int) -> str:
    """Display a specific opinion by ID."""
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)
