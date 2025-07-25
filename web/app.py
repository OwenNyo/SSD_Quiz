from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

def is_xss_attack(input_str):
    # Check for common XSS patterns
    xss_patterns = [
        r"<script.*?>.*?</script.*?>",
        r"javascript:",
        r"<.*?on\w+=.*?>",
        r"document\.",
        r"window\.",
        r"alert\s*\(",
        r"eval\s*\(",
    ]
    return any(re.search(pattern, input_str, re.IGNORECASE) for pattern in xss_patterns)

def is_sql_injection(input_str):
    # Check for common SQLi keywords and patterns
    sql_patterns = [
        r"(--|\bOR\b|\bAND\b).*(=|>|<)",  # basic tautologies
        r"(?:')\s*?(?:OR|AND)\s*?.*?=.*?(?:')",
        r"(\bSELECT\b|\bUNION\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b)",
        r"(\bDROP\b|\bEXEC\b|\bEXECUTE\b|\bCREATE\b|\bALTER\b)",
        r"['\";]+",  # suspicious characters
    ]
    return any(re.search(pattern, input_str, re.IGNORECASE) for pattern in sql_patterns)

@app.route("/", methods=["GET", "POST"])
def home():
    search_term = ""
    error = None
    if request.method == "POST":
        search_term = request.form.get("search", "")

        if is_xss_attack(search_term):
            error = "Potential XSS attack detected. Please enter a valid search term."
            search_term = ""
        elif is_sql_injection(search_term):
            error = "Potential SQL injection detected. Please enter a valid search term."
            search_term = ""
        else:
            return redirect(url_for("result", term=search_term))
    
    return render_template("home.html", error=error, search_term=search_term)

@app.route("/result")
def result():
    term = request.args.get("term", "")
    return render_template("result.html", term=term)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
