from settings import *
from database import *
from login import *

def profile(request):
    username = request.query_string.get("username", [""])[0]

    q = database.execute("""

    SELECT email, timestamp FROM users
    WHERE username = ?

    """, (username,))
    
    user = q.fetchone()
    print("test")
    if not user or not username:
        return request.redirect_response("/404.html")
    
    page = templates["profile"].format(
        username=username,
        email=user["email"],
        joined=user["timestamp"])

    return request.default_response(page)
    
