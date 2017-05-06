# -*- coding: utf-8 -*-
# Auto-generated by Stone, do not modify.
try:
    from . import stone_validators as bv
    from . import stone_base as bb
except (SystemError, ValueError):
    # Catch errors raised when importing a relative module when not in a package.
    # This makes testing this file directly (outside of a package) easier.
    import stone_validators as bv
    import stone_base as bb

class AccessError(bb.Union):
    """
    Error occurred because the account doesn't have permission to access the
    resource.

    This class acts as a tagged union. Only one of the ``is_*`` methods will
    return true. To get the associated value of a tag (if one exists), use the
    corresponding ``get_*`` method.

    :ivar InvalidAccountTypeError invalid_account_type: Current account type
        cannot access the resource.
    :ivar PaperAccessError paper_access_denied: Current account cannot access
        Paper.
    """

    _catch_all = 'other'
    # Attribute is overwritten below the class definition
    other = None

    @classmethod
    def invalid_account_type(cls, val):
        """
        Create an instance of this class set to the ``invalid_account_type`` tag
        with value ``val``.

        :param InvalidAccountTypeError val:
        :rtype: AccessError
        """
        return cls('invalid_account_type', val)

    @classmethod
    def paper_access_denied(cls, val):
        """
        Create an instance of this class set to the ``paper_access_denied`` tag
        with value ``val``.

        :param PaperAccessError val:
        :rtype: AccessError
        """
        return cls('paper_access_denied', val)

    def is_invalid_account_type(self):
        """
        Check if the union tag is ``invalid_account_type``.

        :rtype: bool
        """
        return self._tag == 'invalid_account_type'

    def is_paper_access_denied(self):
        """
        Check if the union tag is ``paper_access_denied``.

        :rtype: bool
        """
        return self._tag == 'paper_access_denied'

    def is_other(self):
        """
        Check if the union tag is ``other``.

        :rtype: bool
        """
        return self._tag == 'other'

    def get_invalid_account_type(self):
        """
        Current account type cannot access the resource.

        Only call this if :meth:`is_invalid_account_type` is true.

        :rtype: InvalidAccountTypeError
        """
        if not self.is_invalid_account_type():
            raise AttributeError("tag 'invalid_account_type' not set")
        return self._value

    def get_paper_access_denied(self):
        """
        Current account cannot access Paper.

        Only call this if :meth:`is_paper_access_denied` is true.

        :rtype: PaperAccessError
        """
        if not self.is_paper_access_denied():
            raise AttributeError("tag 'paper_access_denied' not set")
        return self._value

    def __repr__(self):
        return 'AccessError(%r, %r)' % (self._tag, self._value)

AccessError_validator = bv.Union(AccessError)

class AuthError(bb.Union):
    """
    Errors occurred during authentication.

    This class acts as a tagged union. Only one of the ``is_*`` methods will
    return true. To get the associated value of a tag (if one exists), use the
    corresponding ``get_*`` method.

    :ivar invalid_access_token: The access token is invalid.
    :ivar invalid_select_user: The user specified in 'Dropbox-API-Select-User'
        is no longer on the team.
    :ivar invalid_select_admin: The user specified in 'Dropbox-API-Select-Admin'
        is not a Dropbox Business team admin.
    :ivar user_suspended: The user has been suspended.
    """

    _catch_all = 'other'
    # Attribute is overwritten below the class definition
    invalid_access_token = None
    # Attribute is overwritten below the class definition
    invalid_select_user = None
    # Attribute is overwritten below the class definition
    invalid_select_admin = None
    # Attribute is overwritten below the class definition
    user_suspended = None
    # Attribute is overwritten below the class definition
    other = None

    def is_invalid_access_token(self):
        """
        Check if the union tag is ``invalid_access_token``.

        :rtype: bool
        """
        return self._tag == 'invalid_access_token'

    def is_invalid_select_user(self):
        """
        Check if the union tag is ``invalid_select_user``.

        :rtype: bool
        """
        return self._tag == 'invalid_select_user'

    def is_invalid_select_admin(self):
        """
        Check if the union tag is ``invalid_select_admin``.

        :rtype: bool
        """
        return self._tag == 'invalid_select_admin'

    def is_user_suspended(self):
        """
        Check if the union tag is ``user_suspended``.

        :rtype: bool
        """
        return self._tag == 'user_suspended'

    def is_other(self):
        """
        Check if the union tag is ``other``.

        :rtype: bool
        """
        return self._tag == 'other'

    def __repr__(self):
        return 'AuthError(%r, %r)' % (self._tag, self._value)

AuthError_validator = bv.Union(AuthError)

class InvalidAccountTypeError(bb.Union):
    """
    This class acts as a tagged union. Only one of the ``is_*`` methods will
    return true. To get the associated value of a tag (if one exists), use the
    corresponding ``get_*`` method.

    :ivar endpoint: Current account type doesn't have permission to access this
        route endpoint.
    :ivar feature: Current account type doesn't have permission to access this
        feature.
    """

    _catch_all = 'other'
    # Attribute is overwritten below the class definition
    endpoint = None
    # Attribute is overwritten below the class definition
    feature = None
    # Attribute is overwritten below the class definition
    other = None

    def is_endpoint(self):
        """
        Check if the union tag is ``endpoint``.

        :rtype: bool
        """
        return self._tag == 'endpoint'

    def is_feature(self):
        """
        Check if the union tag is ``feature``.

        :rtype: bool
        """
        return self._tag == 'feature'

    def is_other(self):
        """
        Check if the union tag is ``other``.

        :rtype: bool
        """
        return self._tag == 'other'

    def __repr__(self):
        return 'InvalidAccountTypeError(%r, %r)' % (self._tag, self._value)

InvalidAccountTypeError_validator = bv.Union(InvalidAccountTypeError)

class PaperAccessError(bb.Union):
    """
    This class acts as a tagged union. Only one of the ``is_*`` methods will
    return true. To get the associated value of a tag (if one exists), use the
    corresponding ``get_*`` method.

    :ivar paper_disabled: Paper is disabled.
    :ivar not_paper_user: The provided user has not used Paper yet.
    """

    _catch_all = 'other'
    # Attribute is overwritten below the class definition
    paper_disabled = None
    # Attribute is overwritten below the class definition
    not_paper_user = None
    # Attribute is overwritten below the class definition
    other = None

    def is_paper_disabled(self):
        """
        Check if the union tag is ``paper_disabled``.

        :rtype: bool
        """
        return self._tag == 'paper_disabled'

    def is_not_paper_user(self):
        """
        Check if the union tag is ``not_paper_user``.

        :rtype: bool
        """
        return self._tag == 'not_paper_user'

    def is_other(self):
        """
        Check if the union tag is ``other``.

        :rtype: bool
        """
        return self._tag == 'other'

    def __repr__(self):
        return 'PaperAccessError(%r, %r)' % (self._tag, self._value)

PaperAccessError_validator = bv.Union(PaperAccessError)

class RateLimitError(object):
    """
    Error occurred because the app is being rate limited.

    :ivar reason: The reason why the app is being rate limited.
    :ivar retry_after: The number of seconds that the app should wait before
        making another request.
    """

    __slots__ = [
        '_reason_value',
        '_reason_present',
        '_retry_after_value',
        '_retry_after_present',
    ]

    _has_required_fields = True

    def __init__(self,
                 reason=None,
                 retry_after=None):
        self._reason_value = None
        self._reason_present = False
        self._retry_after_value = None
        self._retry_after_present = False
        if reason is not None:
            self.reason = reason
        if retry_after is not None:
            self.retry_after = retry_after

    @property
    def reason(self):
        """
        The reason why the app is being rate limited.

        :rtype: RateLimitReason
        """
        if self._reason_present:
            return self._reason_value
        else:
            raise AttributeError("missing required field 'reason'")

    @reason.setter
    def reason(self, val):
        self._reason_validator.validate_type_only(val)
        self._reason_value = val
        self._reason_present = True

    @reason.deleter
    def reason(self):
        self._reason_value = None
        self._reason_present = False

    @property
    def retry_after(self):
        """
        The number of seconds that the app should wait before making another
        request.

        :rtype: long
        """
        if self._retry_after_present:
            return self._retry_after_value
        else:
            return 1

    @retry_after.setter
    def retry_after(self, val):
        val = self._retry_after_validator.validate(val)
        self._retry_after_value = val
        self._retry_after_present = True

    @retry_after.deleter
    def retry_after(self):
        self._retry_after_value = None
        self._retry_after_present = False

    def __repr__(self):
        return 'RateLimitError(reason={!r}, retry_after={!r})'.format(
            self._reason_value,
            self._retry_after_value,
        )

RateLimitError_validator = bv.Struct(RateLimitError)

class RateLimitReason(bb.Union):
    """
    This class acts as a tagged union. Only one of the ``is_*`` methods will
    return true. To get the associated value of a tag (if one exists), use the
    corresponding ``get_*`` method.

    :ivar too_many_requests: You are making too many requests in the past few
        minutes.
    :ivar too_many_write_operations: There are currently too many write
        operations happening in the user's Dropbox.
    """

    _catch_all = 'other'
    # Attribute is overwritten below the class definition
    too_many_requests = None
    # Attribute is overwritten below the class definition
    too_many_write_operations = None
    # Attribute is overwritten below the class definition
    other = None

    def is_too_many_requests(self):
        """
        Check if the union tag is ``too_many_requests``.

        :rtype: bool
        """
        return self._tag == 'too_many_requests'

    def is_too_many_write_operations(self):
        """
        Check if the union tag is ``too_many_write_operations``.

        :rtype: bool
        """
        return self._tag == 'too_many_write_operations'

    def is_other(self):
        """
        Check if the union tag is ``other``.

        :rtype: bool
        """
        return self._tag == 'other'

    def __repr__(self):
        return 'RateLimitReason(%r, %r)' % (self._tag, self._value)

RateLimitReason_validator = bv.Union(RateLimitReason)

class TokenFromOAuth1Arg(object):
    """
    :ivar oauth1_token: The supplied OAuth 1.0 access token.
    :ivar oauth1_token_secret: The token secret associated with the supplied
        access token.
    """

    __slots__ = [
        '_oauth1_token_value',
        '_oauth1_token_present',
        '_oauth1_token_secret_value',
        '_oauth1_token_secret_present',
    ]

    _has_required_fields = True

    def __init__(self,
                 oauth1_token=None,
                 oauth1_token_secret=None):
        self._oauth1_token_value = None
        self._oauth1_token_present = False
        self._oauth1_token_secret_value = None
        self._oauth1_token_secret_present = False
        if oauth1_token is not None:
            self.oauth1_token = oauth1_token
        if oauth1_token_secret is not None:
            self.oauth1_token_secret = oauth1_token_secret

    @property
    def oauth1_token(self):
        """
        The supplied OAuth 1.0 access token.

        :rtype: str
        """
        if self._oauth1_token_present:
            return self._oauth1_token_value
        else:
            raise AttributeError("missing required field 'oauth1_token'")

    @oauth1_token.setter
    def oauth1_token(self, val):
        val = self._oauth1_token_validator.validate(val)
        self._oauth1_token_value = val
        self._oauth1_token_present = True

    @oauth1_token.deleter
    def oauth1_token(self):
        self._oauth1_token_value = None
        self._oauth1_token_present = False

    @property
    def oauth1_token_secret(self):
        """
        The token secret associated with the supplied access token.

        :rtype: str
        """
        if self._oauth1_token_secret_present:
            return self._oauth1_token_secret_value
        else:
            raise AttributeError("missing required field 'oauth1_token_secret'")

    @oauth1_token_secret.setter
    def oauth1_token_secret(self, val):
        val = self._oauth1_token_secret_validator.validate(val)
        self._oauth1_token_secret_value = val
        self._oauth1_token_secret_present = True

    @oauth1_token_secret.deleter
    def oauth1_token_secret(self):
        self._oauth1_token_secret_value = None
        self._oauth1_token_secret_present = False

    def __repr__(self):
        return 'TokenFromOAuth1Arg(oauth1_token={!r}, oauth1_token_secret={!r})'.format(
            self._oauth1_token_value,
            self._oauth1_token_secret_value,
        )

TokenFromOAuth1Arg_validator = bv.Struct(TokenFromOAuth1Arg)

class TokenFromOAuth1Error(bb.Union):
    """
    This class acts as a tagged union. Only one of the ``is_*`` methods will
    return true. To get the associated value of a tag (if one exists), use the
    corresponding ``get_*`` method.

    :ivar invalid_oauth1_token_info: Part or all of the OAuth 1.0 access token
        info is invalid.
    :ivar app_id_mismatch: The authorized app does not match the app associated
        with the supplied access token.
    """

    _catch_all = 'other'
    # Attribute is overwritten below the class definition
    invalid_oauth1_token_info = None
    # Attribute is overwritten below the class definition
    app_id_mismatch = None
    # Attribute is overwritten below the class definition
    other = None

    def is_invalid_oauth1_token_info(self):
        """
        Check if the union tag is ``invalid_oauth1_token_info``.

        :rtype: bool
        """
        return self._tag == 'invalid_oauth1_token_info'

    def is_app_id_mismatch(self):
        """
        Check if the union tag is ``app_id_mismatch``.

        :rtype: bool
        """
        return self._tag == 'app_id_mismatch'

    def is_other(self):
        """
        Check if the union tag is ``other``.

        :rtype: bool
        """
        return self._tag == 'other'

    def __repr__(self):
        return 'TokenFromOAuth1Error(%r, %r)' % (self._tag, self._value)

TokenFromOAuth1Error_validator = bv.Union(TokenFromOAuth1Error)

class TokenFromOAuth1Result(object):
    """
    :ivar oauth2_token: The OAuth 2.0 token generated from the supplied OAuth
        1.0 token.
    """

    __slots__ = [
        '_oauth2_token_value',
        '_oauth2_token_present',
    ]

    _has_required_fields = True

    def __init__(self,
                 oauth2_token=None):
        self._oauth2_token_value = None
        self._oauth2_token_present = False
        if oauth2_token is not None:
            self.oauth2_token = oauth2_token

    @property
    def oauth2_token(self):
        """
        The OAuth 2.0 token generated from the supplied OAuth 1.0 token.

        :rtype: str
        """
        if self._oauth2_token_present:
            return self._oauth2_token_value
        else:
            raise AttributeError("missing required field 'oauth2_token'")

    @oauth2_token.setter
    def oauth2_token(self, val):
        val = self._oauth2_token_validator.validate(val)
        self._oauth2_token_value = val
        self._oauth2_token_present = True

    @oauth2_token.deleter
    def oauth2_token(self):
        self._oauth2_token_value = None
        self._oauth2_token_present = False

    def __repr__(self):
        return 'TokenFromOAuth1Result(oauth2_token={!r})'.format(
            self._oauth2_token_value,
        )

TokenFromOAuth1Result_validator = bv.Struct(TokenFromOAuth1Result)

AccessError._invalid_account_type_validator = InvalidAccountTypeError_validator
AccessError._paper_access_denied_validator = PaperAccessError_validator
AccessError._other_validator = bv.Void()
AccessError._tagmap = {
    'invalid_account_type': AccessError._invalid_account_type_validator,
    'paper_access_denied': AccessError._paper_access_denied_validator,
    'other': AccessError._other_validator,
}

AccessError.other = AccessError('other')

AuthError._invalid_access_token_validator = bv.Void()
AuthError._invalid_select_user_validator = bv.Void()
AuthError._invalid_select_admin_validator = bv.Void()
AuthError._user_suspended_validator = bv.Void()
AuthError._other_validator = bv.Void()
AuthError._tagmap = {
    'invalid_access_token': AuthError._invalid_access_token_validator,
    'invalid_select_user': AuthError._invalid_select_user_validator,
    'invalid_select_admin': AuthError._invalid_select_admin_validator,
    'user_suspended': AuthError._user_suspended_validator,
    'other': AuthError._other_validator,
}

AuthError.invalid_access_token = AuthError('invalid_access_token')
AuthError.invalid_select_user = AuthError('invalid_select_user')
AuthError.invalid_select_admin = AuthError('invalid_select_admin')
AuthError.user_suspended = AuthError('user_suspended')
AuthError.other = AuthError('other')

InvalidAccountTypeError._endpoint_validator = bv.Void()
InvalidAccountTypeError._feature_validator = bv.Void()
InvalidAccountTypeError._other_validator = bv.Void()
InvalidAccountTypeError._tagmap = {
    'endpoint': InvalidAccountTypeError._endpoint_validator,
    'feature': InvalidAccountTypeError._feature_validator,
    'other': InvalidAccountTypeError._other_validator,
}

InvalidAccountTypeError.endpoint = InvalidAccountTypeError('endpoint')
InvalidAccountTypeError.feature = InvalidAccountTypeError('feature')
InvalidAccountTypeError.other = InvalidAccountTypeError('other')

PaperAccessError._paper_disabled_validator = bv.Void()
PaperAccessError._not_paper_user_validator = bv.Void()
PaperAccessError._other_validator = bv.Void()
PaperAccessError._tagmap = {
    'paper_disabled': PaperAccessError._paper_disabled_validator,
    'not_paper_user': PaperAccessError._not_paper_user_validator,
    'other': PaperAccessError._other_validator,
}

PaperAccessError.paper_disabled = PaperAccessError('paper_disabled')
PaperAccessError.not_paper_user = PaperAccessError('not_paper_user')
PaperAccessError.other = PaperAccessError('other')

RateLimitError._reason_validator = RateLimitReason_validator
RateLimitError._retry_after_validator = bv.UInt64()
RateLimitError._all_field_names_ = set([
    'reason',
    'retry_after',
])
RateLimitError._all_fields_ = [
    ('reason', RateLimitError._reason_validator),
    ('retry_after', RateLimitError._retry_after_validator),
]

RateLimitReason._too_many_requests_validator = bv.Void()
RateLimitReason._too_many_write_operations_validator = bv.Void()
RateLimitReason._other_validator = bv.Void()
RateLimitReason._tagmap = {
    'too_many_requests': RateLimitReason._too_many_requests_validator,
    'too_many_write_operations': RateLimitReason._too_many_write_operations_validator,
    'other': RateLimitReason._other_validator,
}

RateLimitReason.too_many_requests = RateLimitReason('too_many_requests')
RateLimitReason.too_many_write_operations = RateLimitReason('too_many_write_operations')
RateLimitReason.other = RateLimitReason('other')

TokenFromOAuth1Arg._oauth1_token_validator = bv.String(min_length=1)
TokenFromOAuth1Arg._oauth1_token_secret_validator = bv.String(min_length=1)
TokenFromOAuth1Arg._all_field_names_ = set([
    'oauth1_token',
    'oauth1_token_secret',
])
TokenFromOAuth1Arg._all_fields_ = [
    ('oauth1_token', TokenFromOAuth1Arg._oauth1_token_validator),
    ('oauth1_token_secret', TokenFromOAuth1Arg._oauth1_token_secret_validator),
]

TokenFromOAuth1Error._invalid_oauth1_token_info_validator = bv.Void()
TokenFromOAuth1Error._app_id_mismatch_validator = bv.Void()
TokenFromOAuth1Error._other_validator = bv.Void()
TokenFromOAuth1Error._tagmap = {
    'invalid_oauth1_token_info': TokenFromOAuth1Error._invalid_oauth1_token_info_validator,
    'app_id_mismatch': TokenFromOAuth1Error._app_id_mismatch_validator,
    'other': TokenFromOAuth1Error._other_validator,
}

TokenFromOAuth1Error.invalid_oauth1_token_info = TokenFromOAuth1Error('invalid_oauth1_token_info')
TokenFromOAuth1Error.app_id_mismatch = TokenFromOAuth1Error('app_id_mismatch')
TokenFromOAuth1Error.other = TokenFromOAuth1Error('other')

TokenFromOAuth1Result._oauth2_token_validator = bv.String(min_length=1)
TokenFromOAuth1Result._all_field_names_ = set(['oauth2_token'])
TokenFromOAuth1Result._all_fields_ = [('oauth2_token', TokenFromOAuth1Result._oauth2_token_validator)]

token_from_oauth1 = bb.Route(
    'token/from_oauth1',
    False,
    TokenFromOAuth1Arg_validator,
    TokenFromOAuth1Result_validator,
    TokenFromOAuth1Error_validator,
    {'host': u'api',
     'style': u'rpc'},
)
token_revoke = bb.Route(
    'token/revoke',
    False,
    bv.Void(),
    bv.Void(),
    bv.Void(),
    {'host': u'api',
     'style': u'rpc'},
)

ROUTES = {
    'token/from_oauth1': token_from_oauth1,
    'token/revoke': token_revoke,
}

