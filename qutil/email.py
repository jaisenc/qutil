import imaplib
import mimetypes
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email

import os


def email_smtp(subject, body_html,
               email_to=None,
               email_cc=None,
               email_bcc=None,
               email_from_name='"Report" <do_not_reply@test.com>',
               attachment_list=None):
    """

    :param server: smtplib.SMTP instance
    :param subject: string
    :param body_html: string
    :param email_to: string or list
    :param email_cc: string or list
    :param email_bcc: string or list
    :param email_from_name: string
    :param attachment_list: list of file path
    :return:
    """
    # type: (str, str, str, list, list, list, str, list) -> None

    server = smtplib.SMTP(host='localhost',  # config.get_project_setting('EMAIL_HOST'),
                          port=1025)  # config.get_project_setting('EMAIL_PORT'))
    if attachment_list is None:
        attachment_list = []
    if email_bcc is None:
        email_bcc = []
    if email_cc is None:
        email_cc = []
    if email_to is None:
        email_to = []

    # change from str to list
    if type(email_to) == str:
        email_to = email_to.split(';')
    if type(email_cc) == str:
        email_cc = email_cc.split(';')
    if type(email_bcc) == str:
        email_bcc = email_bcc.split(';')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email_from_name
    msg['To'] = ",".join(email_to)
    msg['Cc'] = ",".join(email_cc)
    msg['Bcc'] = ",".join(email_bcc)
    # msg['Reply-To'] = 'donotreply@purposeinvest.com'

    recipients = email_to + email_cc + email_bcc

    msg.attach(MIMEText(body_html, 'html'))

    for path in attachment_list:
        if not os.path.isfile(path):
            continue
        # Guess the content type based on the file's extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip'd or compressed files.
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open(path)
            # Note: we should handle calculating the charset
            attch = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(path, 'rb')
            attch = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(path, 'rb')
            attch = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(path, 'rb')
            attch = MIMEBase(maintype, subtype)
            attch.set_payload(fp.read())
            fp.close()
            # Encode the payload using Base64
            encoders.encode_base64(attch)
        # Set the filename parameter
        attch.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
        msg.attach(attch)

    server.sendmail(email_from_name, recipients, msg.as_string())
    server.quit()


def get_email(imap_url, imap_user, impa_password, mail_folder="INBOX", mail_search_str=''):
    mail = imaplib.IMAP4(imap_url)
    mail.login(imap_user, impa_password)
    mail.select(mail_folder)

    typ, msgs = mail.search(None, mail_search_str)
    msgs = msgs[0].split()
    message_list = []
    for emailid in msgs:
        resp, data = mail.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        m = email.message_from_bytes(email_body)
        message_list.append(m)
    return message_list


def download_attachment_from_mail(imap_url, imap_user, impa_password, mail_folder="INBOX",
                                  mail_search_str='', svdir=''):
    import imaplib
    import email
    import os

    os.makedirs(svdir, exist_ok=True)

    mail = imaplib.IMAP4(imap_url)
    mail.login(imap_user, impa_password)
    mail.select(mail_folder)

    typ, msgs = mail.search(None, mail_search_str)
    msgs = msgs[0].split()

    for emailid in msgs:
        resp, data = mail.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        m = email.message_from_bytes(email_body)
        if m.get_content_maintype() != 'multipart':
            continue

        for part in m.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename is not None:
                sv_path = os.path.join(svdir, filename)
                if not os.path.isfile(sv_path):
                    print(sv_path)
                    fp = open(sv_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                else:
                    print('File Already Exists, skipping: {}'.format(sv_path))
    mail.close()


if __name__ == '__main__':
    # server = smtplib.SMTP('Relay.appriver.com:2525')
    email_smtp(subject='test subject',
               body_html='<h1>this is a header</h1>',
               email_to='test@test.com',
               attachment_list=[os.path.normpath('C:\\logo.png')])
    # server.quit()
