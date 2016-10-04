from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import DeletePost, GetPosts

import config

cfInst=config.ConfigCrawlYaml()
cf=cfInst.get_config()
wp = Client(cf["wordpress"]["url"]+"/xmlrpc.php", cf["wordpress"]["username"],cf["wordpress"]["password"])

for off in range(0,100):
	d={'number':100}
	posts = wp.call(GetPosts(d))
	for post in posts:
		if post.post_status == 'draft':
			print "Delete "+post.id
			wp.call(DeletePost(post.id))