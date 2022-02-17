from itertools import count
import json
import logging.config
import os
import pickle
import sys
import time
import requests
from constants import * 
from response.EngagementResponse import EngagementResponse

class InstagramCrawler(object):
    def __init__(self, **kwargs):
        defaultAttr = dict(username = '', logger = None, maximum = 0,
                            loginUser = '', loginPass = '', mediaMetadata = False, interactive = False,
                            profileMetadata = False, cookiejar = 'cookies', filterLocation = None,
                            mediaTypes = ['image', 'video', 'story-image', 'story-video'],
                            tag = False, location = False, verbose = 0, includeLocation = False,
                            noCheckCertificate = False, logDestination = '')

        allowedAttr = list(defaultAttr.keys())
        defaultAttr.update(kwargs)

        for key in defaultAttr:
            if key in allowedAttr:
                self.__dict__[key] = defaultAttr.get(key)

        # story media type means story-image & story-video
        if 'story' in self.mediaTypes:
            self.mediaTypes.remove('story')
            if 'story-image' not in self.mediaTypes:
                self.mediaTypes.append('story-image')
            if 'story-video' not in self.mediaTypes:
                self.mediaTypes.append('story-video')

        # Set up a logger
        if self.logger is None:
            self.logger = InstagramCrawler.getLogger(level=logging.DEBUG, dest=defaultAttr.get('logDestination'), verbose=defaultAttr.get('verbose'))

        self.session = requests.Session()
        if self.noCheckCertificate:
            self.session.verify = False

        self.session.headers = {'user-agent': CHROME_WIN_UA}
        
        if self.cookiejar and os.path.exists(self.cookiejar):
            with open(self.cookiejar, 'rb') as f:
                self.session.cookies.update(pickle.load(f))

        self.session.cookies.set('ig_pr', '1')
        self.rhx_gis = ""

        self.posts = []
        self.stories = []
        
        self.cookies = None
        self.authenticated = False
        self.loggedIn = False
        self.quit = False        

    def getLogger(level=logging.DEBUG, dest='', verbose=0):
        # Creates a logger
        logger = logging.getLogger(__name__)

        dest +=  '/' if (dest !=  '') and dest[-1] != '/' else ''
        fh = logging.FileHandler(dest + 'instagram-scrapping.log', 'a')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        fh.setLevel(level)
        logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        sh_lvls = [logging.ERROR, logging.WARNING, logging.INFO]
        sh.setLevel(sh_lvls[verbose])
        
        logger.addHandler(sh)
        logger.setLevel(level)

        return logger

    def scrape(self):
        # Get users information
        self.session.headers.update({'user-agent': STORIES_UA})
        try:
            # Get the user metadata.
            user = self.getUserInfo(self.username)

            # TO DO -- Create test mode
            # Test mode will load json into a file for be more readable
            """
            f = open('test', 'w')
            f.write(json.dumps(user))
            """

            if not user:
                self.logger.error('Error getting user details for {0}. Please verify that user.'.format(self.username))
            elif user and user['user']['is_private']:
                self.logger.info('User {0} is private'.format(self.username))

        except ValueError:
            self.logger.error("Unable to scrape user - %s" % self.username)
        finally:
            self.quit = True
            self.logout()

        return user

    def getResponse(self, url):
        # Gets response from Instagram
        retry = 0
        retryDelay = RETRY_DELAY
        while True:
            if self.quit:
                return
            try:
                response = self.session.get(timeout = CONNECT_TIMEOUT, cookies = self.cookies, url = url)
                if response.status_code == 404:
                    return
                response.raise_for_status()
                content_length = response.headers.get('Content-Length')
                if content_length is not None and len(response.content) != int(content_length):
                    #raise PartialContentException('Partial response')
                    raise
                return response
            except (KeyboardInterrupt):
                raise
            #except (requests.exceptions.RequestException, PartialContentException) as e:
            except (requests.exceptions.RequestException) as e:
                if retry < MAX_RETRIES:
                    self.logger.warning('Retry after exception {0} on {1}'.format(repr(e), url))
                    time.sleep(retryDelay)
                    retryDelay = min(2 * retryDelay, MAX_RETRY_DELAY)
                    retry = retry + 1
                    continue
                   
                raise

    def getUserInfo(self, username=''):
        # Fetches user metadata
        resp = self.getJson(BASE_URL + username)
        return resp

    def getJson(self, url):
        # Retrieve text from URL. JSON as string
        resp = self.getResponse(url)

        if resp is not None:
            data = resp.text.split("window._sharedData = ")[1].split(";</script>")[0]
            return self.convertToJson(data)['entry_data']['ProfilePage'][0]['graphql']

    def convertToJson(self, text):
        # Convert text into JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            self.logger.error('Text is not json: ' + text)
            raise

    def saveCookies(self):
        # Saves cookies binary
        if self.cookiejar:
            with open(self.cookiejar, 'wb') as f:
                pickle.dump(self.session.cookies, f)

    def authenticate(self):
        # Log in into Instagram
        self.session.headers.update({'Referer': BASE_URL, 'user-agent': STORIES_UA})
        req = self.session.get(BASE_URL)

        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})

        loginData = {'username': self.loginUser, 'password': self.loginPass}
        login = self.session.post(LOGIN_URL, data = loginData, allow_redirects = True)
        self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.cookies = login.cookies
        loginText = self.convertToJson(login.text)

        if loginText.get('authenticated') and login.status_code == 200:
            self.authenticated = True
            self.loggedIn = True
            self.session.headers.update({'user-agent': CHROME_WIN_UA})
            self.rhx_gis = ""
        else:
            self.logger.error('Login failed for ' + self.loginUser)

            if 'checkpoint_url' in loginText:
                checkpoint_url = loginText.get('checkpoint_url')
                self.logger.error('Please verify your account at ' + BASE_URL[0:-1] + checkpoint_url)

                if self.interactive is True:
                    self.loginChallenge(checkpoint_url)
            elif 'errors' in loginText:
                for count, error in enumerate(loginText['errors'].get('error')):
                    count += 1
                    self.logger.debug('Session error %(count)s: "%(error)s"' % locals())
            else:
                self.logger.error(json.dumps(loginText))
            sys.exit(1)

    def loginChallenge(self, checkpoint_url):
        # 2FA Authentication, for command line executions.
        # If you aren't using command line, it's need it to log in before through web.
        # interactive parameter (enables this function) is False by default.
        self.session.headers.update({'Referer': BASE_URL})
        req = self.session.get(BASE_URL[:-1] + checkpoint_url)
        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken'], 'X-Instagram-AJAX': '1'})

        self.session.headers.update({'Referer': BASE_URL[:-1] + checkpoint_url})
        mode = int(input('Choose a challenge mode (0 - SMS, 1 - Email): '))
        challenge_data = {'choice': mode}
        challenge = self.session.post(BASE_URL[:-1] + checkpoint_url, data=challenge_data, allowRedirects=True)
        self.session.headers.update({'X-CSRFToken': challenge.cookies['csrftoken'], 'X-Instagram-AJAX': '1'})

        code = int(input('Enter code received: '))
        code_data = {'security_code': code}
        code = self.session.post(BASE_URL[:-1] + checkpoint_url, data=code_data, allowRedirects=True)
        self.session.headers.update({'X-CSRFToken': code.cookies['csrftoken']})
        self.cookies = code.cookies
        code_text = self.convertToJson(code.text)

        if code_text.get('status') == 'ok':
            self.authenticated = True
            self.loggedIn = True
        elif 'errors' in code.text:
            for count, error in enumerate(code_text['challenge']['errors']):
                count += 1
                self.logger.error('Session error %(count)s: "%(error)s"' % locals())
        else:
            self.logger.error(json.dumps(code_text))

    def logout(self):
        # Log out
        if self.loggedIn:
            try:
                logout_data = {'csrfmiddlewaretoken': self.cookies['csrftoken']}
                self.session.post(LOGOUT_URL, data=logout_data)
                self.authenticated = False
                self.loggedIn = False
            except requests.exceptions.RequestException:
                self.logger.warning('Failed to log out ' + self.loginUser)

    def getFollowers(self):
        user = self.scrape()
        return user['user']['edge_followed_by']['count']

    def getEngagement(self):
        user = self.scrape()

        followers = user['user']['edge_followed_by']['count']
        timeline = user['user']['edge_owner_to_timeline_media']

        likes = 0
        comments = 0

        for i in range(0, timeline['count']):
            likes += timeline['edges'][i]['node']['edge_liked_by']['count']
            comments += timeline['edges'][i]['node']['edge_media_to_comment']['count']

            if i == 2:
                break
            
        return EngagementResponse(True, [], {'engagement': (likes + comments) / followers})