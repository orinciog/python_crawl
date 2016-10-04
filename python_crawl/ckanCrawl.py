from ckanapi import RemoteCKAN
import dateutil.parser
from datetime import datetime

import wordpress



class CrawlCKAN(object):
	def __init__(self,config):
		self.config=config
		self.current_time = datetime.now()
		self.ckan_inst = RemoteCKAN(self.config["ckan"]["url"])
		self.ckan_time = self.config["ckan"]["last_modified"]
		self.wp = wordpress.WordpressCrawl(self.config)

		self.results=[]
		self.results_error=[]

	def do_process(self):
		offset=0;
		print "BEGIN PROCESSING "+str(self.current_time)
		while offset>=0:
			datasets = self.ckan_inst.action.current_package_list_with_resources(name='my-dataset', limit=10, offset=offset)
			for dataset in datasets:
				process_result=self.process_dataset(dataset)
				if process_result==False:
					offset=-1
					break;
				else:
					offset=offset+1
		print "END PROCESSING"+str(self.current_time)
		
	def process_dataset(self,dataset):
		print "PROCESS DATASET "+dataset["title"]
		dataset_date=dateutil.parser.parse(dataset["metadata_modified"])
		if dataset_date<self.ckan_time:
			return False
		if dataset_date>self.current_time:
			self.publish_dataset_error(dataset)
		else:	
			self.publish_dataset(dataset)
		return True
		
	def publish_dataset(self,dataset):
		print "PUBLISH DATASET " +dataset["title"]
		try:
			post=wordpress.CkanPost(dataset)
			for resource in dataset["resources"]:
				resource_date = dateutil.parser.parse(resource["created"])
				if resource_date<self.current_time and resource_date>self.ckan_time:
					post.addResource(resource)
			post_id=self.wp.postCkan(post)
			self.results.append({'title':dataset["title"],"content":post_id})
		except KeyError:
			self.publish_dataset_error(dataset)
		return	

	def update_config(self):
		self.config["ckan"]["last_modified"]=self.current_time
		return self.config

	def publish_dataset_error(self,dataset):
		if dataset["name"] in self.config["ckan"]["error_names"]:
			return
		self.config["ckan"]["error_names"].append(dataset["name"])
		print "PUBLISH ERROR DATASET " +dataset["title"] + " " + str(self.current_time)
		post=wordpress.CkanPost(dataset)
		for resource in dataset["resources"]:
			resource_date = dateutil.parser.parse(resource["created"])
			if resource_date>self.ckan_time:
				post.addResource(resource)
		post_content=post.expandDataset(True)
		self.results_error.append({'title':dataset["title"],"content":post_content})

	def get_day(self):
		return self.current_time.strftime("%Y-%m-%d")

	def get_results(self):
		em=wordpress.CkanEmail(self.get_day(),self.results,self.results_error)
		return em.expand()
	

