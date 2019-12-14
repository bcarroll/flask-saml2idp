from flask import render_template


def saml_IDP_error_view(**kwargs):
    """ Default error view when a 'known' error occurs in the saml2 authentication views.
    """
    exception = kwargs.get("exception")

    context = {
        "exception_type": exception.__class__.__name__ if exception else None,
        "exception_msg": str(exception) if exception else None,
        "extra_message": kwargs.get("extra_message"),
    }

    return render_template('djangosaml2idp/error.html', context)
