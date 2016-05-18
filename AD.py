import ldap
import sys
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

class ApiLDAP(object):

  def __init__(self):
    ''' OVERRIDE DE CENAS '''

  def authenticate(self, username, password):
    try:
      conn = ldap.initialize('ldap://xx.xx.xx.xx')
      conn.protocol_version = 3
      conn.set_option(ldap.OPT_REFERRALS, 0)
      #conn.set_option(ldap.OPT_X_TLS_DEMAND, True)
      #conn.start_tls_s()
      conn.simple_bind_s(username, password)
      conn.unbind_s()
      return True
    except ldap.LDAPError, e:
       if type(e.message) == dict and e.message.has_key('desc'):
          return False
	  #raise Exception("AD autentication failure for user %s: %s" % (username, e.message['desc']))
       else:
          #raise Exception("AD autentication failure for user %s: %s" % (username, e.message))
          return False
