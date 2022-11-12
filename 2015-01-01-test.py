# Include the Dropbox SDK
import dropbox
import cPickle
import datetime
import random
import sys

pre_path = "Apps/scriptogram/posts/"

'''
# Get your app key and secret from the Dropbox developer website
app_key = '3inw1ji3nkpj8wh'
app_secret = 'pnvvb8bntbdlph8'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# Have the user sign in and authorize this token
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()

# This will fail if the user enters an invalid authorization code
access_token, user_id = flow.finish(code)

cPickle.dump(access_token, open("token", "wb"))
'''
def upload_md() :
	if len(sys.argv) != 2:
		print "param error %s" %len(sys.argv) 
		return
	file_name = sys.argv[1]

	access_token = cPickle.load(open("token", "rb"))

	client = dropbox.client.DropboxClient(access_token)
	print 'linked account: ', client.account_info()

	f = open(file_name)
	response = client.put_file(pre_path + str(datetime.date.today()) + "-" + str(random.randint(0,100)) + ".md", f)
	print 'uploaded: ', response


upload_md()
'''
folder_metadata = client.metadata('/')
print 'metadata: ', folder_metadata

f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
out = open('magnum-opus.txt', 'w')
out.write(f.read())
out.close()
print metadata
'''

