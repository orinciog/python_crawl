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
		self.wp.call(NewPost(post))
		
	
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