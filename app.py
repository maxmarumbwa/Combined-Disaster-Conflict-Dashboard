from flask import Flask, jsonify, request
import requests
import socket

# Force IPv4 for all requests (avoids Starlink IPv6 ENOTFOUND issues)
original_getaddrinfo = socket.getaddrinfo
socket.getaddrinfo = lambda *args, **kwargs: original_getaddrinfo(
    args[0], args[1], socket.AF_INET
)

app = Flask(__name__)

# Your ACLED API key
ACLED_KEY = "YOUR_API_KEY"  # <-- replace with your real key


@app.route("/")
def acled_proxy():
    """
    Proxy endpoint to fetch ACLED data
    Example: /api/acled?country=Sudan&year=2023&limit=10
    """
    base_url = "https://api.acleddata.com/acled/read"

    # Get query parameters from request
    params = request.args.to_dict()  # e.g., {"country": "Sudan", "year": "2023"}
    params["key"] = ACLED_KEY  # always add API key

    try:
        r = requests.get(base_url, params=params, timeout=15)
        r.raise_for_status()
        return jsonify(r.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
