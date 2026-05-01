try:
    from apscheduler.schedulers.background import BackgroundScheduler
    _has_apscheduler = True
except ImportError:
    BackgroundScheduler = None
    _has_apscheduler = False

from datetime import datetime
import logging
import os
import time

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========================================
# Task 1 — Daily Check-in
# ========================================

def daily_checkin():
    logger.info(f"✅ Daily check-in at {datetime.now()}")
    try:
        response = requests.post(
            "https://billions.network/api/checkin",
            json={
                "did": "did:iden3:billions:main:2VmAkXrihYaM5GFwgwhz4ytE2ZDd1xmog7c9kDwBvL",
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        logger.info(f"Check-in response: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"Check-in failed: {e}", exc_info=True)


# ========================================
# Task 2 — Auto Post Listings
# ========================================

def auto_post_listings(app=None):
    logger.info(f"🏠 Auto posting listings at {datetime.now()}")
    try:
        if app is None:
            from app import create_app
            app = create_app(os.environ.get('FLASK_ENV', 'development'))

        from app import db, Property

        with app.app_context():
            listings = Property.query.filter_by(featured=False).all()
            if not listings:
                logger.info('No new listings found to post.')
                return

            for listing in listings:
                listing.featured = True
                db.session.add(listing)
            db.session.commit()
            logger.info(f"Posted {len(listings)} listing(s)")
    except Exception as e:
        logger.error(f"Auto post failed: {e}", exc_info=True)


# ========================================
# Task 3 — Auto Send Messages
# ========================================

def auto_send_messages(app=None):
    logger.info(f"📧 Auto sending messages at {datetime.now()}")
    try:
        if app is None:
            from app import create_app
            app = create_app(os.environ.get('FLASK_ENV', 'development'))

        from app import db, Lead

        with app.app_context():
            leads = Lead.query.filter_by(status='new').all()
            if not leads:
                logger.info('No new leads found to message.')
                return

            for lead in leads:
                logger.info(f"Messaging lead: {lead.email}")
                lead.status = 'contacted'
                db.session.add(lead)
            db.session.commit()
            logger.info(f"Contacted {len(leads)} lead(s)")
    except Exception as e:
        logger.error(f"Auto message failed: {e}", exc_info=True)


# ========================================
# Start Scheduler
# ========================================

def start_scheduler(app=None):
    if not _has_apscheduler:
        logger.warning('⚠️ APScheduler is not installed. Scheduler will not start.')
        return None

    if app is None:
        from app import create_app
        app = create_app(os.environ.get('FLASK_ENV', 'development'))

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        daily_checkin,
        'cron',
        hour=9,
        minute=0,
        id='daily_checkin',
        replace_existing=True
    )
    scheduler.add_job(
        lambda: auto_post_listings(app),
        'interval',
        hours=6,
        id='auto_post_listings',
        replace_existing=True
    )
    scheduler.add_job(
        lambda: auto_send_messages(app),
        'interval',
        minutes=30,
        id='auto_send_messages',
        replace_existing=True
    )

    scheduler.start()
    logger.info('✅ Scheduler started!')
    return scheduler


if __name__ == '__main__':
    scheduler = start_scheduler()
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info('Scheduler stopped.')
