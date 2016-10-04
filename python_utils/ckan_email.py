import smtplib
from email.mime.text import MIMEText

class CkanEmail(object):
	def __init__(self,config):
		self.config=config
	def send_email(self,subject,content):
		to = self.config["smtp"]["to"]
		smtpserver = smtplib.SMTP(self.config["smtp"]["server"],self.config["smtp"]["port"])
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo
		smtpserver.login(self.config["smtp"]["user"], self.config["smtp"]["pass"])
		msg = MIMEText(content,'html')
		msg['Subject'] = subject
		msg['From'] = self.config["smtp"]["user"]
		msg['To'] = to
		smtpserver.sendmail(self.config["smtp"]["user"], [to], msg.as_string())
		smtpserver.close()


