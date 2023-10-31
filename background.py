from celery import Celery
from stravalib import Client
from models import db, User, Run

broker = backend ='redis://localhost:6379'

celery = Celery(__name__, backend=broker, broker=broker)
_APP = None


@celery.on_after_configure.connect
def initialize_periodic_tasks(sender , **kwargs):
    sender.add_periodic_task(10.0, fetch_all_runs.s(), name="fetch every 10s")

def activity2run(user, activity):
    run = Run()
    run.runner = user
    run.strava_id = activity.id
    run.name = activity.name
    run.distance = activity.distance
    run.elapsed_time = activity.elapsed_time.total_seconds()
    run.average_speed = activity.average_speed
    run.average_heartrate = activity.average_heartrate
    run.total_elevation_gain = activity.total_elevation_gain
    run.start_date = activity.start_date
    return run


@celery.task
def fetch_all_runs():
    global _APP
    if _APP is None:
        from app import app
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local2.sqlite'
        _APP = app
        #db.init_app(app=_APP)
    else:
        app = _APP

    runs_fetched = {}
    with app.app_context():
        q = db.session.query(User)
        for user in q:
            if user.strava_token is None:
                continue
            runs_fetched[user.uid] = fetch_single_user_run(user)

    return runs_fetched

def fetch_single_user_run(user : User):
    client = Client(access_token= user.strava_token)
    runs = 0
    for activity in client.get_activities(limit=10):
        if activity.type != 'Run':
            continue
        q = db.session.query(Run).filter(Run.strava_id == activity.id)
        run = q.first()
        if run is None:
            db.session.add(activity2run(user, activity))
            runs += 1
    
    db.session.commit()
    return runs