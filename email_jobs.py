from app import create_app, db, mail
from app import User, Ledger
from celery import Celery, schedules
from flask_mail import Message
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from flask import render_template

app = create_app()
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def send_async_email(email_data):
    with app.app_context():
        msg = Message(email_data['subject'],
                      sender=email_data['sender'],
                      recipients=[email_data['recipient']])
        msg.body = email_data['body']
        mail.send(msg)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        schedules.crontab(hour="19", minute="0"),
        send_email_to_all_users.s(),
    )
    sender.add_periodic_task(
        schedules.crontab(hour="0", minute="0", day_of_month="1"),
        send_monthly_activity_report.s(),
    )

@celery.task
def send_email_to_all_users():
    with app.app_context():
        current_date = datetime.utcnow().date()
        users = User.query.all()
        for user in users:
            purchased_today = Ledger.query.filter(Ledger.userid == user.username, db.func.date(Ledger.purchaseDate) == current_date).first()
            if not purchased_today:
                email_data = {
                    'subject': "We noticed you didn't buy anything today...",
                    'sender': 'tracerswaifu@gmail.com',
                    'recipient': user.email,
                    'body': 'Visit the website and make a purchase today!'
                }
                send_async_email.delay(email_data)
                
@celery.task
def send_async_email_report(email_data):
    with app.app_context():
        message = Message(email_data['subject'],
                      sender=email_data['sender'],
                      recipients=[email_data['recipient']],
                      html=email_data['html_body'])
        mail.send(message)
        
@celery.task
def send_monthly_activity_report():
    with app.app_context():
        today = datetime.utcnow()
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = (today.replace(day=1) - timedelta(days=1))
        users = User.query.all()
        for user in users:
            total_expenditure = db.session.query(func.sum(Ledger.rateUnit * Ledger.quantity)).filter(
                Ledger.userid == user.username, 
                extract("year", Ledger.purchaseDate) == first_day_last_month.year, 
                extract("month", Ledger.purchaseDate) == first_day_last_month.month,
            ).scalar() or 0
            orders = Ledger.query.filter(Ledger.userid == user.username, Ledger.purchaseDate >= first_day_last_month,
                                         Ledger.purchaseDate <= last_day_last_month).all()
            html_body = render_template("ActivityReport.html", orders=orders, total_expenditure=total_expenditure)
            email_data = {
                'subject': 'Monthly Activity Report',
                'sender': 'tracerswaifu@gmail.com',
                'recipient': user.email,
                'html_body': html_body,
            }
            send_async_email_report.delay(email_data)