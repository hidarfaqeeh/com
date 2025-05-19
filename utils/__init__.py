def get_badge(rank):
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    return ""

def format_username(user_id, username):
    if username:
        return f"@{username}"
    return f"<a href='tg://user?id={user_id}'>{user_id}</a>"
