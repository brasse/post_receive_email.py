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
* Sets the Reply-To header to the author of the commit.
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
**hooks.smtp-subject**
    If this variable is set the subject line will be formatted according
    to this template. The format is the same as for Python string
    interpolation when using dictionaries for the values.

    The available keys are: 

        * ``%(prefix)s``  - The value of hooks.emailprefix.
        * ``%(ref_name)s`` - The ref name sent to post_receive 
          (eg. refs/heads/master)
        * ``%(hash)s``    - The abbreviated commit hash.
        * ``%(index)s``   - An individual commit's order number among all the
          commits being pushed.
        * ``%(message)s`` - The first line of the commit message.

    The default subject template is 
    ``%(prefix)s %(ref_name)s commit %(hash)s`` if one commit is being pushed
    and ``%(prefix)s %(ref_name)s commit #%(index)s %(hash)s`` if more than
    one is being pushed.

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
    Debuging information will be logged to this file.

Licence
=======

MIT License.
