import pickle
import requests

COOKIE_FILE = './data/cookies.pkl'
API_ROOT = "https://cms.alevel.com.cn"


class CMSClient:
    def __init__(self):
        # Create a session
        self.session = requests.Session()
        # Load existing cookies if they exist
        self.load_cookies()

    # Method to save cookies to file
    def save_cookies(self):
        with open(COOKIE_FILE, 'wb') as file:
            pickle.dump(self.session.cookies, file)

    # Method to load cookies from file
    def load_cookies(self):
        try:
            with open(COOKIE_FILE, 'rb') as file:
                self.session.cookies.update(pickle.load(file))
        except FileNotFoundError:
            print(f"No cookie file found at {COOKIE_FILE}")

    # Method to do login
    def login(self, username, password, remember=False):
        resp = self.session.post(f"{API_ROOT}/api/token/", {'username': username, 'password': password})

        if resp.status_code == 200 and resp.json()['detail'] == 'Successfully logged in!':
            print('Successfully logged in!')
            if remember:
                self.save_cookies()
            return True, resp.text

        return False, resp.text

    # Method to get user's basic info
    def get_user_info(self):
        resp = self.session.get(f"{API_ROOT}/api/account/user/")
        if resp.status_code == 200:
            return resp.json()
        return None

    def get_assessments(self, year):
        resp = self.session.get(f"{API_ROOT}/api/legacy/students/my/assessments/?year={year}")
        if resp.status_code == 200:
            return True, resp.json()
        return False, resp.text
