import subprocess

__author__ = 'ataylor'
#!/usr/bin/python

import smtplib
import shutil
import os
import time


def mail_results(test_name, result, output):
    message = """
    Test {:s} {:s}
    \n

    {:s}
    """.format(test_name, result, output)
    try:
        session = smtplib.SMTP('smtp.gmail.com',587)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login("rostestmailer@gmail.com", "#MailMeResults")
        session.sendmail("rostestmailer@gmail.com", "aktaylor08@gmail.com", message)
        session.quit()
    except smtplib.SMTPException:
        print "Error: unable to send email"



def run_cmd():
    # # build clean
    st = time.time()
    cmd = ["make"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    et = time.time()
    t_clean = et - st
    if exit_code != 0:
        mail_results("llvm_build", "failed on build", err + "Time: " + str(t_clean))
        return
    else:
        mail_results("llvm_buld", "Build is done",  "Took: "  + str(t_clean))

if __name__ == '__main__':
    run_cmd()

