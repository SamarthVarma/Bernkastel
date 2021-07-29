import configparser

# config = configparser.ConfigParser()
# config.read('bot_config.ini')

class config():
    def __init__(self, config):
        self.token = config.get('secret','token')
        self.log_ch = config.getint('secret','log_ch')
        self.host = config.get('postgres','host')
        self.database = config.get('postgres','database')
        self.user = config.get('postgres','user')
        self.password = config.get('postgres','password')
