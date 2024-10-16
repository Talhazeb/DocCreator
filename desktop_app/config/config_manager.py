import configparser

class ConfigManager:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section, key):
        return self.config[section][key]

    def get_templates_dir(self):
        return self.get('Paths', 'templates_dir')

    def get_signers_dir(self):
        return self.get('Paths', 'signers_dir')

    # Add more specific getter methods as needed