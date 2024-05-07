from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Event
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    all_events=Event.query.all()
    all_events=Event.query.order_by(Event.date.desc()).all()                          
    return render_template("home.html", user=current_user, 
    all_events=all_events) 

@views.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST': 
        event = request.form.get('event') 
        price = request.form.get('price')
        day = request.form.get('day')
        time = request.form.get('time')
        place = request.form.get('place')
        link = request.form.get('link')
        name = request.form.get('name')

        if not name or len(name) < 2:
            flash('Event name is too short!', category='error')   
        else:
            new_event = Event(data=event, user_id=current_user.id,
            price=price, day=day, time=time, place=place, link=link, 
            name=name)
            db.session.add(new_event)
            db.session.commit()
            flash('Event added!', category='success')

    return render_template("create.html", user=current_user)







@views.route('/my-events', methods=['GET', 'POST'])
@login_required
def my_events():
    return render_template("my_events.html", user=current_user)    











# @views.route('/create', methods=['GET', 'POST'])
# @login_required
# def create():
#     if request.method == 'POST': 
#         event = request.form.get('event') #event is a DESCRIPTION // in models it is "data"
#         name = request.form.get('name')
#         price = request.form.get('price')
#         day = request.form.get('day')
#         time = request.form.get('time')
#         place = request.form.get('place')
#         link = request.form.get('link')

#         if len(event) < 1:
#             flash('Event is too short!', category='error') 
#         else:
#             # add below: " , name=name, price=price, day=day, time=time, place=place, link=link"
#             new_event = Event(data=event, user_id=current_user.id, name=name, price=price, day=day, time=time, place=place, link=link)  #providing the schema for the event 
#             db.session.add(new_event) #adding the event to the database 
#             db.session.commit()
#             flash('Event added!', category='success')
#     # all_events=Event.query.all()  <--- activate this line
#     return render_template("create.html", user=current_user) #all_events=Event.query.all()   <-add it




@views.route('/delete-event', methods=['POST'])
def delete_event():  
    event = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    eventId = event['eventId']
    event = Event.query.get(eventId)
    if event:
        if event.user_id == current_user.id:
            db.session.delete(event)
            db.session.commit()
            flash('Event Deleted!' , category='success')

    return jsonify({})
