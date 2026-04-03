from datetime import datetime
MONTH_ABBR = {1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"}
def tos_date_str(expiration: str) -> str:
    ts = datetime.fromisoformat(expiration)
    return f"{ts.day:02d} {MONTH_ABBR[ts.month]} {str(ts.year)[-2:]}"
