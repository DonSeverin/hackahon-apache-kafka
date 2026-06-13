import time

def fetch_line_statuses(lines):
    line_ids = ",".join(lines)
    url = f"{TFL_BASE_URL}/Line/{line_ids}/Status"
    params = {"app_key": TFL_APP_KEY} if TFL_APP_KEY else None

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def calculate_risk(line_statuses):
    score = 0
    reasons = []

    for line in line_statuses:
        line_name = line.get("name", line.get("id", "Unknown line"))
        statuses = line.get("lineStatuses", [])

        if not statuses:
            reasons.append(f"{line_name} has no status information")
            score += 5
            continue

        for status in statuses:
            status_text = status.get("statusSeverityDescription", "Unknown status")
            status_lower = status_text.lower()

            if "part suspended" in status_lower:
                score += 30
                reasons.append(f"{line_name} is partly suspended")
            elif "suspended" in status_lower:
                score += 50
                reasons.append(f"{line_name} is suspended")
            elif "severe" in status_lower:
                score += 35
                reasons.append(f"{line_name} has severe delays")
            elif "minor" in status_lower:
                score += 15
                reasons.append(f"{line_name} has minor delays")
            elif "good service" in status_lower:
                reasons.append(f"{line_name} has good service")
            else:
                score += 10
                reasons.append(f"{line_name} status is {status_text}")

    score = min(score, 100)
    return score, risk_level(score), reasons

def risk_level(score):
    if score <= 20:
        return "low"
    if score <= 50:
        return "medium"
    if score <= 80:
        return "high"
    return "severe"

def build_commute_risk_event():
    line_statuses = fetch_line_statuses(COMMUTE_LINES)
    risk_score, level, reasons = calculate_risk(line_statuses)

    return {
        "source": "tfl-api",
        "event_type": "commute_risk_score",
        "fetched_at": time.time(),
        "from": FROM_LOCATION,
        "to": TO_LOCATION,
        "lines_checked": COMMUTE_LINES,
        "line_statuses": [
            {
                "id": line.get("id"),
                "name": line.get("name"),
                "statuses": [
                    status.get("statusSeverityDescription", "Unknown status")
                    for status in line.get("lineStatuses", [])
                ],
            }
            for line in line_statuses
        ],
        "risk_score": risk_score,
        "risk_level": level,
        "reasons": reasons,
    }

