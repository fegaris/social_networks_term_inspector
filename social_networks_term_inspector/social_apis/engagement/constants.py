BASE_URL = 'https://www.instagram.com/'
LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
LOGOUT_URL = BASE_URL + 'accounts/logout/'
USER_URL = BASE_URL + '{0}/?__a=1'
USER_INFO = 'https://i.instagram.com/api/v1/users/{0}/info/'

CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'

CONNECT_TIMEOUT = 90
MAX_RETRIES = 5
RETRY_DELAY = 5
MAX_RETRY_DELAY = 60