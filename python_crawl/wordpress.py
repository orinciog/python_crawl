from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from string import Template

class WordpressCrawl(object):
	def __init__(self,config):
		self.config=config
		self.wp = Client(config["wordpress"]["url"]+"/xmlrpc.php", config["wordpress"]["username"], config["wordpress"]["password"])
		
	def postCkan(self,ckanpost):
		post = WordPressPost()
		post.title = 'Dataset published '+ckanpost.getTitle()
		post.post_status = "publish"
		post.terms_names = {	
			'post_tag': ['python-autocrawl'],   'category': [self.config["wordpress"]["category"]]
		}
		post.content = ckanpost.expandDataset(False)
		return self.wp.call(NewPost(post))
		
	
class CkanPost(object):
	def __init__(self,dataset):
		self.dataset=dataset
		self.resources=[]
		rt = open( 'templates/wordpress_resource.template' )
		self.template_resource = Template(rt.read())
		dt = open( 'templates/wordpress_dataset.template' )
		self.template_dataset  = Template(dt.read())
		rt.close()
		dt.close()
		
	def addResource(self,resource):
		self.resources.append(resource)
		
	def expandDataset(self,safe=False):
		d = dict()
		d["dataset_time"]  = self.dataset["metadata_modified"]
		d["dataset_title"] = self.dataset["title"]
		d["dataset_author"]= self.dataset["author"]
		d["dataset_email"] = self.dataset["author_email"]
		d["dataset_notes"] = self.dataset["notes"]
		d["dataset_name"]  = self.dataset["name"]
		str_res=""
		for res in self.resources:
			str_res=str_res+self.expandResource(res,safe)
		d["resources"]=str_res
		if safe==False:
			return self.template_dataset.substitute(d)
		else:
			return self.template_dataset.safe_substitute(d)
	
	def getTitle(self):
		return self.dataset["title"]
	
	def expandResource(self,resource,safe=False):
		d = dict()
		d["resource_time"]=resource["created"]
		d["resource_name"]=resource["name"]
		d["resource_description"]=resource["description"]
		d["resource_url"]=resource["url"]
		d["resource_format"]=resource["format"]
		if safe==False:
			return self.template_resource.substitute(d)
		else:
			return self.template_resource.safe_substitute(d)

class CkanEmail(object):
	def __init__(self,day,datasets,error_datasets):
		self.datasets=datasets
		self.error_datasets=error_datasets
		self.day=day
		et = open( 'templates/email.template' )
		self.template_email    = Template(et.read())
		et.close()
		dt = open( 'templates/email_dataset.template' )
		self.template_dataset  = Template(dt.read())
		dt.close()
		
	def expand(self):
		d = dict()
		str_res=""
		i=0
		for res in self.datasets:
			i=i+1
			str_res=str_res+self.expand_dataset(res)
		d["datasets"]=str_res
		d["datasets_number"]=i

		i=0
		str_res=""
		for res in self.error_datasets:
			i=i+1
			str_res=str_res+self.expand_dataset(res)
		d["error_datasets"]=str_res
		d["error_datasets_number"]=i
		d["day"]=self.day

		return self.template_email.safe_substitute(d)
	
	def expand_dataset(self,dataset):
		d = dict()
		d["dataset_title"] = dataset["title"].encode('utf-8')
		d["dataset_content"]=dataset["content"].encode('utf-8')
		return self.template_dataset.safe_substitute(d)
