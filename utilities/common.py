import time
from flask import current_app
import datetime
import arrow
import bleach
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os
import pytz
from pytz import timezone

def utc_now_ts():
    return int(time.time())

def utc_now_ts_ms():
    return lambda: int(round(time.time() * 1000))

def ms_stamp_humanize(ts):
    ts = datetime.datetime.fromtimestamp(ts/1000.0)
    return arrow.get(ts).humanize()

def linkify(text):
    text = bleach.clean(text, tags=[], attributes={}, styles=[], strip=True)
    return bleach.linkify(text)

def email(to_email, event, body_html):
    # Rip and replaced the boto3 SES service. This creates a meeting invite attachment

    attendees = []
    attendees.append(to_email)
    CRLF = "\r\n"
    login = "hpeeventsnow@gmail.com"
    central = timezone('US/Central')
    organizer = "ORGANIZER;CN=youremail:mailto:youremail"+CRLF+" @gmail.com"
    fro = "yourname <youremail@gmail.com>"
    ddtstart = datetime.datetime.now()
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    description = "DESCRIPTION: Meeting Invite for...."+CRLF

    # Which event to attend

    if event[0] == 'P':
        dtstart = central.localize(datetime.datetime(2016, 10, 25, 14, 0,0)).strftime("%Y%m%dT%H%M%SZ")
        dtend = central.localize(datetime.datetime(2016, 10, 25, 22, 0,0)).strftime("%Y%m%dT%H%M%SZ")
    if event[0] == 'H':
        dtstart = central.localize(datetime.datetime(2016, 10, 27, 14, 0,0)).strftime("%Y%m%dT%H%M%SZ")
        dtend = central.localize(datetime.datetime(2016, 10, 27, 22, 0,0)).strftime("%Y%m%dT%H%M%SZ")

    # Create calendar invitation

    attendee = ""
    for att in attendees:
        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
    ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:dcnevent"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
    ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
    ical+= "UID:FIXMEUID"+dtstamp+CRLF
    ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
    #ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Your subject here"
    msg['From'] = fro
    msg['To'] = ",".join(attendees)

    part_email = MIMEText(body_html,"html")
    part_cal = MIMEText(ical,'calendar;method=REQUEST')

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    modifier = "Your Gmail Password"

    ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
    ical_atch.set_payload(ical)
    Encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

    eml_atch = MIMEBase('text/plain','')
    Encoders.encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)
    mailServer = smtplib.SMTP('smtp.gmail.com',587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.login(login, modifier)
    mailServer.sendmail(fro, attendees, msg.as_string())
    mailServer.close()

def emailman(to_email, event, man_html):
    
	# Send simple mail to manager

    CRLF = "\r\n"
    login = "hpeeventsnow@gmail.com"
    central = timezone('US/Central')
    organizer = "ORGANIZER;CN=youremail:mailto:youremail"+CRLF+" @gmail.com"
    fro = "youremail <youremail@gmail.com>"
    ddtstart = datetime.datetime.now()
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    description = "DESCRIPTION: Meeting Invite for......"+CRLF

    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Your subject here"
    msg['From'] = fro
    msg['To'] = to_email

    part_email = MIMEText(man_html,"html")

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    modifier = "Your Gmail Password"

    msgAlternative.attach(part_email)

    mailServer = smtplib.SMTP('smtp.gmail.com',587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.login(login, modifier)
    mailServer.sendmail(fro, to_email, msg.as_string())
    mailServer.close()
