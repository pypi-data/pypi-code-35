import stdiomask
import os
import json
import click
import smtplib
from appdirs import user_data_dir
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 


APP_DIR_NAME = "easy_kindle"
APP_AUTHOR = "https://github.com/itsron717"

def send_mail(creds, doc, user_data_path):
    try:
        print("Sending to Kindle.......")
        msg = MIMEMultipart() 
        msg['From'] = creds["Email"] 
        msg['To'] = creds["Kindle_email"] 
        msg['Subject'] = "Sending {} to your kindle...".format(doc)
        body = "Peace(?)" # Why do you need a body tho?
        msg.attach(MIMEText(body, 'plain')) 
        attachment = open(doc, "rb") 
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload((attachment).read()) 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % doc) 
        msg.attach(p) 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login(creds["Email"], creds["Password"]) 
        text = msg.as_string() 
        s.sendmail(creds["Email"], creds["Kindle_email"], text) 
        s.quit()
        print("Attachment Sent to Kindle!!!")
    except smtplib.SMTPAuthenticationError:
        print("Are you sure you entered the correct Email and Password? Please check again.")
        if os.path.exists(user_data_path):
            os.remove(user_data_path)
    except:
        print("Please check your internet connection and try again.")


@click.command()
@click.argument('doc')
def main(doc=None):

    """DOC: Filename(with extension) that is to be sent to the kindle."""
    
    user_data_path = user_data_dir(APP_DIR_NAME, APP_AUTHOR)
    if os.path.exists(user_data_path):
        try:
            with open(user_data_path + '/' + 'creds.json') as f:  
                creds = json.load(f)
        except FileNotFoundError:
            print("Bad Path, Check your user data application support folder or reinstall the package again.")
            return
    else:
        os.mkdir(user_data_path)
        print("Enter Gmail ID - ")
        email = input()
        password = stdiomask.getpass()
        print("Enter Send-To-Kindle Email - ")
        destination_mail = input()

        creds = {}
        creds["Email"] = email
        creds["Password"] = password
        creds["Kindle_email"] = destination_mail

        with open(user_data_path + '/' + 'creds.json', 'w') as f:  
            json.dump(creds, f)
    send_mail(creds, doc, user_data_path)