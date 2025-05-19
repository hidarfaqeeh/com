def get_badge(rank: int):
    badges = {
        1: "🥇 ذهبي",
        2: "🥈 فضي",
        3: "🥉 برونزي"
    }
    return badges.get(rank, "")

def format_username(user_id, username):
    if username:
        return f"@{username}"
    else:
        return f"ID:{user_id}"
