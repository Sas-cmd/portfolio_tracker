
def score_to_badge(score: int) -> str:
    if score == 5:
        return "🟢"
    elif score == 4:
        return "🔵"
    elif score == 3:
        return "🟡"
    elif score == 2:
        return "🟠"
    elif score == 1:
        return "🔴"
    else:
        return "⚫"