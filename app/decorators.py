from threading import Thread 
""" implement other asynchronous functions with decorators"""
def async(f):
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		thr.start()
	return wrapper