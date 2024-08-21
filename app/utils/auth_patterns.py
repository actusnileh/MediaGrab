import re

EMAIL_PATTERN = re.compile(r"^[\w.-]+@\w+\.[a-z]+(\.[a-z]+)*$")

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,30}$")

PASSWORD_PATTERN = re.compile(r"[A-Za-z\d@$!%*?&]{6,}")
