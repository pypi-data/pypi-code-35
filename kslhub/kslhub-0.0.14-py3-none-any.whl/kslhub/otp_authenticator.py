
import os
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode, Bool, Integer

import pexpect
import pexpect.pxssh as pxssh
import subprocess
import sys, os
import getpass


from .ssh_authenticator import session_manager

def otp_validate(hostname,port,user,pw,otp):

    print("Username: %s" % user)
    print("Hostname: %s:%s" % (hostname,port))
    print("OTP is: %s" % otp)

    ssh_newkey = 'Are you sure you want to continue connecting'
    # my ssh command line
    p=pexpect.spawn('ssh -p %s %s@%s echo hostname:`hostname`' % (port,user,hostname))

    password_already_sent = False
    otp_already_sent = False

    authenticated = False
    
    while True:
      i=p.expect([ssh_newkey,'assword:',"One-time .*:","Verification .*:","hostname .*$", pexpect.EOF])
      if i==0:
        print("I say yes")
        p.sendline('yes')
      if i==1:
        if password_already_sent:
          authenticated = False
          print("I aleady gave password")
          break
        print("I give password")
        p.sendline(pw)
        password_already_sent = True
      if i==2 or i==3:
        if otp_already_sent:
          authenticated = False
          print("I aleady gave otp")
          break
        print("I give otp")
        p.sendline(otp)
        otp_already_sent = True
      if i==4:
        authenticated = True
        break
      elif i==5:
        print("I either got key or connection timeout")
        break
        pass

    print(p.before) # print out the result
    if not(authenticated):
      authenticated  =  str(p.before).find('hostname')>-1
    p.close()
    
    if authenticated:
      print("SUCESS login %s on %s" % (user,hostname))
    else:
      print("FAILED login %s on %s" % (user,hostname))
      
    print(" ")

    return authenticated

slurm_machine = session_manager()
    
class SshUserLoginHandler(BaseHandler):

    def get(self):
        header_name = self.authenticator.header_name
        ssh_user = self.request.headers.get(header_name, "")
        if ssh_user == "":
            raise web.HTTPError(401)

        user = self.user_from_username(ssh_user)
        self.set_login_cookie(user)
        next_url = self.get_next_url(user)
        self.redirect(next_url)


class SshUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the SSH_USER HTTP header.
    """
    
    hub_greeting_message = Unicode("DataHub Sign in", config=True,
        help="""
        Greeting message to print in the login box
        """
    ).tag(config=True)
    
    otp_required = Bool(False, config=True,
        help="""Ask for an OTP password if True
        """,
    )

    otp_authenticator_host = Unicode("localhost", config=True,
        help="""hostname of where to validate OTP password if otp_required set to True
        """,
    )

    otp_authenticator_port = Integer(22, config=True,
        help="""port of hostname of where to validate OTP password if otp_required set to True
        """,
    )

    hub_name = Unicode("DataHub", config=True,
        help="""
        Greeting message to print in the login box
        """
    ).tag(config=True)
    
    job_template_dir = Unicode("./job_templates", config=True,
        help="""
        job templates directory
        """
    ).tag(config=True)


    
    @gen.coroutine
    def authenticate(self, handler, data):

        if handler.config.Authenticator.otp_required:
            hostname = handler.config.Authenticator.host
            port = handler.config.Authenticator.port
            login_ok = otp_validate(hostname,
                                    port,
                                    data['username'],
                                    data['password'],
                                    data['otp'])
            self.log.info("attempt of authentication of %s@%s:%s with otp -> result = %s" % \
                     (data['username'],hostname,port,login_ok))
            if (not(login_ok)):
                return None
                
        machine = handler.config.Authenticator.host
        self.log.info("hello")
        if slurm_machine.open(machine,data['username'],data['password']):
            return data['username']
        return None

class SshUserLocalAuthenticator(LocalAuthenticator):
    """
    Accept the authenticated user name from the SSH_USER HTTP header.
    Derived from LocalAuthenticator for use of features such as adding
    local accounts through the admin interface.
    """
    header_name = Unicode(
        default_value='SSH_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    def get_handlers(self, app):
        return [
            (r'/login', SshUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()

