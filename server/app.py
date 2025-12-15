from flask import Flask, request, jsonify
from datetime import datetime
import geoip2.database

app = Flask(__name__)

ANALYTICS = []

geo_reader = geoip2.database.Reader("GeoLite2-City.mmdb")


def get_client_ip():
    return (
        request.headers.get("X-Real-IP")
        or request.headers.get("X-Forwarded-For", "").split(",")[0]
        or request.remote_addr
    )


def detect_device(user_agent):
    ua = user_agent.lower()

    if "mobile" in ua:
        return "mobile"
    if "tablet" in ua:
        return "tablet"
    if "bot" in ua or "crawler" in ua:
        return "bot"
    return "desktop"


def detect_language(accept_language):
    if accept_language.startswith("fr"):
        return "fr"
    if accept_language.startswith("en"):
        return "en"
    if accept_language.startswith("es"):
        return "es"
    return "unknown"


def detect_source(referer):
    if not referer:
        return "direct"
    if "google" in referer:
        return "google"
    if "linkedin" in referer:
        return "linkedin"
    return "other"


def geo_from_ip(ip):
    try:
        response = geo_reader.city(ip)
        return {
            "country": response.country.name,
            "city": response.city.name
        }
    except Exception:
        return {
            "country": None,
            "city": None
        }


@app.route("/track", methods=["GET", "POST"])
def track():
    accept_language = request.headers.get("Accept-Language", "")
    user_agent = request.headers.get("User-Agent", "")
    referer = request.headers.get("Referer")
    dnt = request.headers.get("DNT")

    ip = get_client_ip()
    location = geo_from_ip(ip)
    
    if dnt == "1":
        return jsonify({
            "message": "Do Not Track enabled – event not stored"
        }), 200

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip,
        "country": location["country"],
        "city": location["city"],
        "language": detect_language(accept_language),
        "device": detect_device(user_agent),
        "source": detect_source(referer)
    }

    ANALYTICS.append(data)

    return jsonify({
        "message": "event tracked",
        "data": data
    })


@app.route("/stats")
def stats():
    return jsonify({
        "events": len(ANALYTICS),
        "data": ANALYTICS
    })


if __name__ == "__main__":
    app.run(debug=True)
