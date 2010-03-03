=====================
post_receive_email.py
=====================

Introduction
============

This is a Git post-receive hook script written in Python that will send
emails when commits are pushed to the repository. It has no
dependencies other than Python and Git (i.e. it does not use
sendmail).

Status
======

The script:

* Always uses TLS when sending emails.
* Only handles commits. No effort has yet been made to handle merge commits.

I will continue to develop this script as the need for more
functionality arises.

Configuration
=============

The script uses the following configuration variables:

**hooks.mailinglist**
    A comma separted list of email recipients.
**hooks.emailprefix**
    All emails will have their subjects prefixed with the value of this 
    variable
**hooks.smtp-host**
    Emails will be sent using this SMTP host.
**hooks.smtp-port**
    This port will be used when communicating with the SMTP host.
**hooks.smtp-sender**
    This is the user that will login to the SMTP host to send emails.
**hooks.smtp-sender-password**
    This password will be used when authenticating the email sender with
    the SMTP host.
**hook.post-receive-logfile**
    Debuging informatun will be logged to this file.

Licence
=======

MIT License.
