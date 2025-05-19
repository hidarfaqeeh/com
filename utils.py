def get_badge(rank: int):
    badges = {
        1: "🥇 ذهبي",
        2: "🥈 فضي",
        3: "🥉 برونزي"
    }
    return badges.get(rank, "")
