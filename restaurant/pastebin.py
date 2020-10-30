import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

API_URL = "https://pastebin.com/api/api_post.php"

PUBLIC = 0
UNLISTED = 1
PRIVATE = 2  # only allowed in combination with api_user_key, as you have to be logged into your account to access the paste

EXPIRE_10_MINUTES = "10M"
EXPIRE_1_HOUR = "1H"
EXPIRE_1_DAY = "1D"
EXPIRE_1_WEEK = "1W"
EXPIRE_2_WEEKS = "2W"
EXPIRE_1_MONTH = "1M"
EXPIRE_6_MONTHS = "6M"
EXPIRE_1_YEAR = "1Y"
EXPIRE_NEVER = "N"


class PastebinError(Exception):
    pass


def create_paste(code, *, dev_key=None, user_key=None, name=None, format=None, private=None, expire=None):
    """
    Create paste on Pastebin.com
    :param code: this is the text that will be written inside your paste
    :param dev_key: which is your unique API Developers Key
    :param user_key: if an invalid or expired api_user_key is used, an error will spawn. 
                     If no api_user_key is used, a guest paste will be created 
    :param name: this will be the name / title of your paste
    :param format: this will be the syntax highlighting value, see https://pastebin.com/doc_api#5
    :param private: this makes a paste PUBLIC, UNLISTED or PRIVATE
    :param expire: this sets the expiration date of your paste
    :return: url of created paste
    """
    api_dev_key = settings.PASTEBIN_API_DEV_KEY if dev_key is None else dev_key

    # Required
    data = {
        "api_dev_key": api_dev_key,
        "api_option": "paste",
        "api_paste_code": code,
    }

    # Optional
    if user_key is not None:
        data["api_user_key"] = user_key
    if name is not None:
        data["api_paste_name"] = name
    if format is not None:
        data["api_paste_format"] = format
    if private is not None:
        data["api_paste_private"] = str(private)
    if expire is not None:
        data["api_paste_expire_date"] = expire

    response = requests.post(API_URL, data=data)

    if response.ok:
        url = response.text
        if _is_url(url):
            return url
        else:
            raise PastebinError(url)
    else:
        response.raise_for_status()


def _is_url(url):
    validate_url = URLValidator()
    try:
        validate_url(url)
    except ValidationError:
        return False
    else:
        return True


def test():
    # OK
    print(create_paste('id,name,foo,bar,baz\n1,"qwe",1,2,3\n', name='dishes.csv', private=UNLISTED,
                       expire=EXPIRE_10_MINUTES))
    # raises PastebinError
    print(create_paste('id,name,foo,bar,baz\n1,"qwe",1,2,3\n', name='dishes.csv', private=UNLISTED,
                       expire=EXPIRE_10_MINUTES, user_key="fjibfouwebf823fu23f82b3f8b328fb238fb"))
