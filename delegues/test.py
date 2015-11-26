from unittest import TestCase

from delegues.ldap import is_authorized
from delegues.fixtures import LDAP_ENTRIES

class LdapTestCase(TestCase):

    def test_can_access_delegues(self):
        """The delegues are authorized """
        for entry in LDAP_ENTRIES["delegues"]:
            self.assertTrue(is_authorized(entry))

    def test_can_access_cf(self):
        """The faculty concil members are authorized """
        for entry in LDAP_ENTRIES["faculty_council"]:
            self.assertTrue(is_authorized(entry))

    def test_can_access_ae(self):
        """The EPFL assembly members are authorized """
        for entry in LDAP_ENTRIES["epfl_assembly"]:
            self.assertTrue(is_authorized(entry))

    def test_can_access_agepolitique(self):
        """The agepolitique members are authorized """
        for entry in LDAP_ENTRIES["agepolitique"]:
            self.assertTrue(is_authorized(entry))

    def test_can_access_comite(self):
        """The Agepoly's comite members are authorized """
        for entry in LDAP_ENTRIES["comite"]:
            self.assertTrue(is_authorized(entry))

    def test_can_access_info(self):
        """The Agepinfo members are authorized """
        for entry in LDAP_ENTRIES["agepinfo"]:
            self.assertTrue(is_authorized(entry))

    def test_cant_access(self):
        """Regular students are not authorized """
        for entry in LDAP_ENTRIES["students"]:
            self.assertFalse(is_authorized(entry))
