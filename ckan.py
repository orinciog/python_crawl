from python_crawl.ckanCrawl import CrawlCKAN
from python_utils.config import ConfigCrawlYaml 
from python_utils.ckan_email import CkanEmail

#get config
configInst=ConfigCrawlYaml()
config=configInst.get_config()

#do work
em=CkanEmail(config)
cc=CrawlCKAN(config)
cc.do_process()

#email results
subject="[PythonCrawl]Results for "+cc.get_day()
em.send_email(subject,cc.get_results())

#collect results
config=cc.update_config()
configInst.set_config(config)
configInst.publish_config()

