import yaml

def yaml_constructor(loader, node):
	return node.value

class ConfigCrawlYaml(object):
	def __init__(self):
		yaml.SafeLoader.add_constructor("tag:yaml.org,2002:python/unicode", yaml_constructor)
		self.config_file="config.yml"
		self.config = yaml.safe_load(open(self.config_file))
		
	def get_config(self):
		return self.config
	
	def set_config(self,config):
		self.config=config
		
	def publish_config(self):
		with open(self.config_file, 'w') as outfile:
			yaml.dump(self.config, outfile, default_flow_style=False)