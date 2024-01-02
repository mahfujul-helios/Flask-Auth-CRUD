import json
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  login_required,  current_user
from . models import Note,db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            
            flash('note is added', category='success')    
    return render_template('home.html')


@views.route('/delete-note/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        # Ensure the note belongs to the current user before deletion
        flash("You can't delete this note.", category='error')
    else:
        db.session.delete(note)
        db.session.commit()
        flash('Note has been deleted.', category='success')
    return redirect('/')




@views.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    note = Note.query.get_or_404(id)

    if request.method == 'POST':
        data = request.form.get('des')

        if note.user_id != current_user.id:
            flash("You can't update this note.", category='error')
        else:
            note.data = data
            db.session.commit()
            flash('Note has been updated.', category='success')
            return redirect(url_for('views.home'))

    return render_template('update.html', note=note)

