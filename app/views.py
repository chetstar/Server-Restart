from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app import app
# from app import expect
import smtplib
from app import app
from flask import Flask, render_template, request, flash,redirect,url_for,jsonify
import datetime
from threading import Thread
import os,subprocess
# @app.route('/_add_numbers')
# def add_numbers():
#     a = request.args.get('a', 0, type=int)
#     b = request.args.get('b', 0, type=int)
#     return jsonify(result=a + b)

@app.route('/restartajaxtest')
def restartajaxtest():
    computer = request.args.get('a')
    import pdb;pdb.set_trace()
    def runJob(computer):
        try:
            print computer
            # subprocess.call(r"\\covenas\decisionsupport\meinzer\production\bat\restart\%s" % computer)
        except Exception,e:
            print 'there was an exception', e
    thr = Thread(target = runJob, args = [computer])
    thr.start()
    return jsonify(result=computer)

@app.route('/restartajax/<computer>')
def restartajax(computer):
    def sendEmail(you,html,text,subject):
        print you
        me = 'chet@acbhcs.org'
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ", ".join(you)
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        # Send the message via local SMTP server.
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo
        with open('//covenas/decisionsupport/meinzer/production/ps/secret/pw.txt','r') as pw:
            fillPW=pw.readline()
        s.login('alamedaDST@gmail.com', '%s' % fillPW) 
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(me, you, msg.as_string())
        s.quit()
    # def runJob(computer):
    #     try:
    #         subprocess.call(r"\\covenas\decisionsupport\meinzer\production\bat\restart\%s" % computer)
    #     except Exception,e:
    #         print 'there was an exception', e
    # thr = Thread(target = runJob, args = [computer])
    # thr.start()
    def runJob(computer):
            err='error code 1'                 
            count=0
            while count < 3:
                out='Error'
                err='error'
                worked='Fail!  Please try again..................'
                try:
                    # log = open("//bhcsdbv02/emanio/bhcsdbv02psexec.log", 'w+') 
                    p=subprocess.Popen(r"""\\covenas\decisionsupport\meinzer\production\bat\restart\%s""" % computer,  stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
                    out, err = p.communicate()
                    if 'error code 0' not in err:
                        count+=1  
                    if 'error code 0' in err:
                        count=3                                          
                        out.replace('Offwall','')
                        err.replace('Offwall','')
                        if "error code 0." in err:
                            worked= "Yes, it worked...................."
                            sendEmail(['cmeinzer@acbhcs.org'],'restarting %s' % computer,'restarting %s' % computer,'restarting %s' % computer)
                except Exception,e:
                    print 'there was an exception', e
                return out,err,worked

    o,e,w=runJob(computer)
    print 'this is o ',o,'this is e ', e
    def runOpen(computer):
        try:
            subprocess.call(r"\\covenas\decisionsupport\meinzer\production\bat\open\%s" % computer)
        except Exception,e:
            print 'there was an exception', e
    thr = Thread(target = runOpen, args = [computer])
    if w=="Yes, it worked....................":
        thr.start()
        shift=".......................try server at "+str((datetime.datetime.now()+datetime.timedelta(minutes=8)).strftime('%I:%M %p'))
    else:
        shift=''
    return jsonify(result=w +" results of "+computer+str(e)+shift )

@app.route('/restart', methods=['GET', 'POST'])
def restart():
    # form=restart_form()
    restartFiles=os.listdir('//covenas/decisionsupport/meinzer/production/bat/restart/')
    return render_template("restart.html",restartFiles=restartFiles)

