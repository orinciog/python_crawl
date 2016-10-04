from python_crawl.ckanCrawl import CrawlCKAN
from python_utils.config import ConfigCrawlYaml 

configInst=ConfigCrawlYaml()
config=configInst.get_config()

cc=CrawlCKAN(config)
cc.do_process()
config=cc.update_config()
configInst.set_config(config)
configInst.publish_config()