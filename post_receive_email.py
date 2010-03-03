from __future__ import with_statement

import re
import smtplib
import subprocess
import sys
import time
import traceback
from email.mime.text import MIMEText

MAILINGLIST = 'hooks.mailinglist'
EMAILPREFIX = 'hooks.emailprefix'
SMTP_HOST = 'hooks.smtp-host'
SMTP_PORT = 'hooks.smtp-port'
SMTP_SENDER = 'hooks.smtp-sender'
SMTP_SENDER_PASSWORD = 'hooks.smtp-sender-password'
POST_RECEIVE_LOGFILE = 'hooks.post-receive-logfile'

class Mailer(object):
    def __init__(self, smtp_host, smtp_port,
                 sender, sender_password, recipients, subject_prefix):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender = sender
        self.sender_password = sender_password
        self.recipients = recipients
        self.subject_prefix = subject_prefix

    def send(self, subject, message):
        if not self.recipients:
            return

        mime_text = MIMEText(message, _charset='utf-8')
        mime_text['From'] = self.sender
        mime_text['To'] = ', '.join(self.recipients)
        if self.subject_prefix:
            subject = '%s %s' % (self.subject_prefix, subject)
        mime_text['Subject'] = subject

        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.sender, self.sender_password)
        server.sendmail(self.sender, self.recipients, 
                        mime_text.as_string())
        server.rset()
        server.quit()

def git_config_get(name):
    p = subprocess.Popen(['git', 'config', '--get', name], 
                         stdout=subprocess.PIPE)
    # Cut off the last \n character.
    return p.stdout.read()[:-1]

def git_show(hash):
    p = subprocess.Popen(['git', 'show', hash], stdout=subprocess.PIPE)
    return p.stdout.read()

def git_rev_parse(hash, short=False):
    args = ['git', 'rev-parse']
    if short:
        args.append('--short')
    args.append(hash)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    # Cut off the last \n character.
    return p.stdout.read()[:-1]
    
def process_commits(commits, mailer):
    for ref_name in commits.keys():
        use_index = len(commits[ref_name]) > 1
        for i, commit in enumerate(commits[ref_name]):
            commit_hash = git_rev_parse(commit, short=True)
            if use_index:
                subject = '%s commit (#%d) %s' % (ref_name, i + 1, 
                                                       commit_hash)
            else:
                subject = '%s commit %s' % (ref_name, commit_hash)
            message = git_show(commit)
            mailer.send(subject, message)
            

def get_commits(old_rev, new_rev):
    p = subprocess.Popen(['git', 'log', '--pretty=format:%H', '--reverse',  
                          '%s..%s' % (old_rev, new_rev)], 
                         stdout=subprocess.PIPE)
    return p.stdout.read().split('\n')

def parse_post_receive_line(l):
    return l.split()

def post_receive(mailer):
    lines = sys.stdin.readlines()
    commits = {}
    for line in lines:
        old_rev, new_rev, ref_name = parse_post_receive_line(line)
        commits[ref_name] = get_commits(old_rev, new_rev)
    process_commits(commits, mailer)

def get_config_variables():
    def optional(variable):
        config[variable] = git_config_get(variable)
    def must_have(variable, type_=str):
        v = git_config_get(variable)
        if not v:
            raise RuntimeError('This script needs %s to work.' % variable)
        config[variable] = type_(v)
    def recipients(variable):
        v = git_config_get(variable)
        config[variable] = [r for r in re.split(' *, *| +', v) if r]

    config = {}
    optional(EMAILPREFIX)
    must_have(SMTP_HOST)
    must_have(SMTP_PORT, int)
    must_have(SMTP_SENDER)
    must_have(SMTP_SENDER_PASSWORD)
    recipients(MAILINGLIST)
    return config

def main():
    log_file_path = git_config_get(POST_RECEIVE_LOGFILE)
    with open(log_file_path, 'a') as log_file:
        try:
            config = get_config_variables()
            mailer = Mailer(config[SMTP_HOST], config[SMTP_PORT],
                            config[SMTP_SENDER], config[SMTP_SENDER_PASSWORD],
                            config[MAILINGLIST], config[EMAILPREFIX])
            post_receive(mailer)
        except:
            log_file.write('%s\n' % time.strftime('%Y-%m-%d %X'))
            traceback.print_exc(file=log_file)

if __name__ == '__main__':
    main()
