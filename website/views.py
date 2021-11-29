from flask import Blueprint, render_template, request, redirect
from flask.helpers import flash
from flask_login import login_required, current_user
from sqlalchemy.orm import session
from sqlalchemy.sql.functions import user
from .models import Note
from . import db
from flask import flash
from .models import Note
import json

views = Blueprint('views', __name__)

@login_required
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note)<1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Note.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'Eroor in deletion'


