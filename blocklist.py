"""
blocklist.py contains the blocklist of JWT tokens.
This list will be imported by the app and the logout resource so that tokens can be
added to the blocklist when the user logs out.
"""

# You need to create a database instead of a set.
BLOCKLIST = set()
