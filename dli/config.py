import os

class Configuration:
    '''Configuration object

    Stores all informations related to the configuration file.
    `expected_path` is a list of paths where pw should look to find a
    configuration file.  The first element has priority and overrides the
    others.  If none of them exists, a file will be created in
    expected_path[0]. That path must be writable by the user!
    '''
    def __init__(self, conffile):
        expected_path = ['~/.', '/etc/pw/']
        expected_path = [os.path.expanduser(p + conffile) for p in expected_path]

        self.file = expected_path[0]
        for path in expected_path:
            if os.path.exists(path):
                self.file = path
                break

        if not os.path.exists(self.file):
            print('Generating configuration file...')
            ip = input('IP address [http://192.168.0.100]: ') or 'http://192.168.0.100'
            user = input('username [admin]: ') or 'admin'
            passwd = input('password []: ') or ''

            with open(self.file, 'w') as f:
                f.write('# more information at: github.com/liambeguin/pw\n')
                f.write('USER=\"' + user + '\"\n')
                f.write('PASSWORD=\"' + passwd + '\"\n')
                f.write('POWER_SWITCH_IP=\"' + ip + '\"\n')

            os.chmod(self.file, 600)

        self.parse()

    def parse(self):
        '''Parse configuration file

        This parser understands bash like variable definitions and everything
        after a # is considered a comment.
        '''
        options = {}
        with open(self.file) as f:
            for line in f:
                if '#' in line:
                    line, comment = line.split('#', 1)
                if '=' in line:
                    option, value = line.split('=', 1)
                    option = option.strip()
                    value = value.strip(" \"\n")
                    options[option] = value

        self.url = options['POWER_SWITCH_IP']
        self.user = options['USER']
        self.password = options['PASSWORD']



