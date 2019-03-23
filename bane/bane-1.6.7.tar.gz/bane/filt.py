from extrafun import escape_html,unescape_html
from bs4 import BeautifulSoup
'''
the following functions use a strict rules to make sure that the returned input is 100% safe
'''

def filter_xss(s,tags=['br','h1','h2','h3','h4','h5','h6','p','strong','pre','b','center']):
 '''
 the xss vulnerability is a major security problem. There are a couple of methods to prevent it,one of them is by escape all user's input.
 that would work with search boxes or normal inputs, but sometimes it's necessery to add some HTML tags in the input and here it comes the problem!!!
 some forms need those tags :/
 but, there is a simple solution for this:
 1-escape all tags
 2-unescape some tags (you should only unescape the tags with this form: <h1>, <br>, <p>...
 
 by doing that we completely protect our users and allow them to use only simple tags to prevent any possible xss. it will be very limited but very effective and protecting the visitors of your website.
 
 it takes 2 arguments:
 
 s: user's input
 tags: the tags to unescape (set to: None to escape all the input)
 
 '''
 s=escape_html(s)
 if tags:
  for x in tags:
   y='&lt;'+x+'&gt;'
   z='<'+x+'>'
   s=s.replace(y,z)
   y='&lt;/'+x+'&gt;'
   z='</'+x+'>'
   s=s.replace(y,z)
 return s

def filter_html(s,unescape=True):
 '''
 this function is to remove all html tags
 '''
 if unescape==True:
  s=unescape_html(s)
 return BeautifulSoup(s, "lxml").text

def filter_injections(s):
 '''
 in any injection attack (sql injection, code injection, command injection...), the attacker always add in his input ";" then his malicious injection.
 so the best act to sanitize the input is to remove everything after the ";".
 '''
 return s.split(';')[0]

def filter_fi(s,ext='php',remote=None):
 '''
 this function is used to remove any possible expolitaion for File Inclusion (Local and Remote) vulnerability and return safe input only
 
 it takes 3 arguments:
 
 s: user' input
 ext: (set by default to: 'php') file's extension
 remote: (set by default to: None) whitelist for legit weblinks to import files from
 '''
 s=s.replace('../','')
 s=s.replace('%00','')
 if (('etc/' in s)or('proc/' in s)):
  return None
 if (ext not in s):
  return None
 if ('://' in s):
  if remote:
   if (s not in remote):
    return None
  return None
 return s
