"""Simple module that fetches the newest post from Orange Mushroom's Blog

@author KOOKIIE
"""
import feedparser


def fetch_latest_post():
	"""Fetches relevant details from the latest OMB post

	Returns:
	Dictionary, representing relevant info. Contains keys 'title', 'link', and 'id'.
	Returns False on failure

	Raises:
	Generic error on failure
	"""
	try:
		feeder = feedparser.parse("https://orangemushroom.net/feed/")
		entry = feeder.entries[0]  # Newest post will be first element
		newest_post = {	 # Extract relevant info only
	        'title': entry.title,
	        'link': entry.link,
		}
		return newest_post
	except Exception as e:
		print(f"CRITICAL: Unable to fetch latest posts!:\n{e}")
		return False
