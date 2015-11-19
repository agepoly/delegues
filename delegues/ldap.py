import ldap3

from django.conf import settings

def make_ldap_request(query, attrs, only_attr=True):
    """
    Issue a query to the LDAP and return the result

    :param query: LDAP filter to apply.
    :type query: str.
    :param attrs: Attributes to query
    :type attrs: list of str.
    :param only_attr: If True, return the only the attributes (as dict) .
    Otherwise, return the ldap entry
    :type only_attr: bool
    :returns: Return the results of the query either as a dict or as an ldap
    Entry object.
    """

    conn = ldap3.Connection(settings.LDAP, auto_bind=True)
    conn.search('c=ch', query, attributes=attrs)

    gen = (e for e in conn.entries)

    if only_attr:
        gen = map(lambda e: e.entry_get_attributes_dict() for e in gen)
        gen = map(lambda e: {k: v for k, v in e.items() if k in attrs}, gen)

    return list(gen)

def get_user_info(sciper, additional_attrs=[], as_dict=True):
    """
    Get the basic user info (sciper, first/lastname, mail, and its memberships)

    :param sciper: Sciper to query.
    :type name: str or int.
    :param additional_attrs: Additional attributes to fetch.
    :type additional_attrs: list
    :param as_dict: If True, return the attributes asked as a dict. Otherwise,
    return an ldap entry.
    """
    query = "(uniqueIdentifier={})".format(sciper)

    # memberOf seems to be return by default
    attrs = ["uniqueIdentifier", "givenName", "sn", "mail", "memberOf"] + additional_attrs

    return make_ldap_request(query, attrs, as_dict)

def is_authorized(entry):
    """
    Take an LDAP entry and return True if the person is authorized to log in to
    the forum.

    :param entry: LDAP entry to verify
    :type entry: ldap3.abstract.entry.Entry
    :returns: True if authorized, False otherwise
    """


