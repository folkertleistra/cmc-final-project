from get_top_streams import run_scraper
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(run_scraper, 'interval', hours=2)
scheduler.start()