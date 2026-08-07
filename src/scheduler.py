from datetime import datetime

def resolve_run_date(date_text=None):
    return datetime.strptime(date_text, "%Y-%m-%d") if date_text else datetime.now()
