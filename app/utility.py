import random
import string
import hashlib

# User system Functions

def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(5))

def generate_hash(name, pw, salt):
	return hashlib.sha256(name + pw + salt).hexdigest()

def make_password_hash(name, pw):
	salt = make_salt()
	h = generate_hash(name, pw, salt)
	return ('%s,%s') % (h ,salt)

def valid_password(name, pw, h):
	obtain_salt = h.split(',')[1]
	tesh_h = generate_hash(name, pw, obtain_salt) + "," + obtain_salt
	if tesh_h == h :
		return True
	return False