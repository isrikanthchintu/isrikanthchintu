"""
blocklist.copy()

This file just contains the blocklist of the JWTtokens. 
It will be imported by app and the loout resource so that tokens can be added to the 
blocklist when the user logs out
"""

BLOCKLIST = set()