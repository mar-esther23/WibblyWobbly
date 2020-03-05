from unidecode import unidecode
from re import sub as resub
from warnings import warn

 def simplify_string(text):
    """Simplify a string to remove special characters, double spaces and use lower case."""
    text = text.lower()
    text = ' '.join([t for t in text.split()])
    text = unidecode.unidecode(text)
    text = resub(r"[^a-zA-Z0-9]+", ' ', text)
    text = ' '.join([t for t in text.split()]) #paranoia
    return text


def warning(val, max_options, text='WARNING'):
    max_options = min(len(val), max_options)
    options = ', '.join(["{} ({})".format(*i) for i in val[0:max_options]])
    }
    warn_message = "{}: {}.\n\tOptions: {}" \
                   .format( text, i, options )
    warn( warn_message )
