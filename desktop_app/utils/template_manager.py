import os
import configparser

class TemplateManager:
    def __init__(self, config):
        self.config = config
        self.templates_dir = config.get_templates_dir()

    def get_template_names(self):
        return [f for f in os.listdir(self.templates_dir) if f.endswith('.docx')]

    def get_template_variables(self, template_name):
        ini_file = os.path.join(self.templates_dir, f"{os.path.splitext(template_name)[0]}.ini")
        if os.path.exists(ini_file):
            config = configparser.ConfigParser()
            config.read(ini_file)
            return dict(config['Variables'])
        return {}