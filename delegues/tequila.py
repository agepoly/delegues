
import urllib
import re


from delegues.models import DegUser

from django.conf import settings

class Backend(object):
    """Backend to authenticate users"""

    def get_user(self, user_id):
        try:
            return DegUser.objects.get(pk=user_id)
        except DegUser.DoesNotExist:
            return None

    def authenticate(self, token=None):

        # Check if token is valid
        params = 'key=' + token
        f = urllib.request.urlopen(
            settings.TEQUILA_SERVER + '/cgi-bin/tequila/fetchattributes',
            params.encode('utf-8'))
        data = f.read().decode('utf-8')

        if data.find('status=ok') == -1:
            return None

        # Get informations about user
        firstName = re.search('\nfirstname=(.*)', data).group(1).split(',')[0]
        name = re.search('\nname=(.*)', data).group(1).split(',')[0]
        email = re.search('\nemail=(.*)', data).group(1)
        sciper = re.search('\nuniqueid=(.*)', data).group(1)

        # Find user in database
        try:
            user = DegUser.objects.get(username=sciper)
        except DegUser.DoesNotExist:
            # Should we create it ?
            if settings.TEQUILA_AUTOCREATE:
                user = DegUser(username=sciper)
                user.first_name = firstName
                user.last_name = name
                user.email = email
                user.update_ldap()
                user.save()
            else:
                user = None

        return user
