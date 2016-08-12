#!/usr/bin/python3

import imaplib, email
import email.parser
imaplib._MAXLINE = 50000

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('kvis.dev@gmail.com', 'password')
# mail.select('"[Gmail]/All Mail"', readonly=True)


def get_email(email_uid):
	result, data = mail.fetch(email_uid, '(RFC822.HEADER BODY.PEEK[1])')
	try:
		raw_email = data[0][1]
		original = email.message_from_bytes(raw_email)

		return original
	except Exception as e:
		print(e)

# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

result, data = mail.search(None, "(FROM \"JIRA\")") # search and return uids instead

for email1 in data[0].decode("utf-8").split(' '):
	if email1 and int(email1):
		eml = get_email(email1)

		if eml is not None and 'from' in eml and 'jira@braincon.atlassian.net' in eml['from']:
			mail.store(email1, '+FLAGS', '\\Deleted')

mail.expunge()
