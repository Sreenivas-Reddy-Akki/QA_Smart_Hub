import os
import requests  # Required for making HTTP requests to the Gemini API
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
from dotenv import load_dotenv
import openai
from google import genai

# from waitress import serve

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
gemini_api_key = os.environ.get("GEMINI_API_KEY")  # ✅ NEW: Load Gemini API Key

if not openai_api_key:
    print("WARNING: OPENAI_API_KEY not found. OpenAI features will not work.")
if not gemini_api_key:  # ✅ NEW: Check for Gemini Key
    print("WARNING: GEMINI_API_KEY not found. Gemini features will not work.")

# -----------------------------
# Flask App Setup
# -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_dev')
app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 10 minutes


# -----------------------------
# Favicon Route
# -----------------------------
@app.route('/favicon.ico')
def favicon():
    # Attempt to serve the favicon from a static images directory
    # If using this in a production environment, ensure 'static/images/favicon.ico' exists.
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


# -----------------------------
# Login Required Decorator
# -----------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# -----------------------------
# Authentication Routes
# -----------------------------
PLACEHOLDER_USER = 'qa-tester'
PLACEHOLDER_PASS = 'smartpass'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == PLACEHOLDER_USER and password == PLACEHOLDER_PASS:
            session['logged_in'] = True
            session['username'] = username
            next_page = request.args.get('next') or url_for('home')
            return redirect(next_page)
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# -----------------------------
# Main Pages (Routes omitted for brevity, no changes needed)
# -----------------------------
@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/manual')
@login_required
def manual():
    return render_template('manual.html')


@app.route('/ai-tools')
@login_required
def ai_tools():
    return render_template('ai_tools.html')


@app.route('/interview')
@login_required
def interview():
    return render_template('interview.html')


@app.route('/blog')
@login_required
def blog():
    return render_template('videos.html')


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


# -----------------------------
# Automation Section (Routes omitted for brevity, no changes needed)
# -----------------------------
@app.route('/automation')
@login_required
def automation_home():
    return render_template('automation/automation.html')


@app.route('/automation/beginners')
@login_required
def automation_beginners():
    return render_template('automation/levels/beginnerlevel.html')


@app.route('/automation/intermediate')
@login_required
def automation_intermediate():
    return render_template('automation/levels/intermediatelevel.html')


@app.route('/automation/professional')
@login_required
def automation_professional():
    return render_template('automation/levels/advancedlevel.html')


# -----------------------------
# Selenium Section (Routes omitted for brevity, no changes needed)
# -----------------------------
@app.route('/automation/selenium')
@login_required
def automation_selenium():
    return render_template('automation/tools/selenium/selenium.html')


@app.route('/automation/selenium/beginner')
@login_required
def selenium_beginner():
    return render_template('automation/tools/selenium/beginnerlevel.html')


@app.route('/automation/selenium/intermediate')
@login_required
def selenium_intermediate():
    return render_template('automation/tools/selenium/intermediatelevel.html')


@app.route('/automation/selenium/advanced')
@login_required
def selenium_advanced():
    return render_template('automation/tools/selenium/advancedlevel.html')


# -----------------------------
# Java Section (Routes omitted for brevity, no changes needed)
# -----------------------------
@app.route('/automation/java')
@login_required
def automation_java():
    return render_template('automation/tools/java/beginnerlevel.html')


@app.route('/automation/java/beginner')
@login_required
def java_beginner():
    return render_template('automation/tools/java/beginnerlevel.html')


@app.route('/automation/java/intermediate')
@login_required
def java_intermediate():
    return render_template('automation/tools/java/intermediatelevel.html')


@app.route('/automation/java/advanced')
@login_required
def java_advanced():
    return render_template('automation/tools/java/advancedlevel.html')


# -----------------------------
# Python Section (Routes omitted for brevity, no changes needed)
# -----------------------------
@app.route('/automation/python')
@login_required
def automation_python():
    return render_template('automation/tools/python/beginnerlevel.html')


@app.route('/automation/python/beginner')
@login_required
def python_beginner():
    return render_template('automation/tools/python/beginnerlevel.html')


@app.route('/automation/python/intermediate')
@login_required
def python_intermediate():
    return render_template('automation/tools/python/intermediatelevel.html')


@app.route('/automation/python/advanced')
@login_required
def python_advanced():
    return render_template('automation/tools/python/advancedlevel.html')


# -----------------------------
# Other Automation Tools (Routes omitted for brevity, no changes needed)
# -----------------------------
@app.route('/automation/xpath')
@login_required
def automation_xpath():
    return render_template('automation/tools/xpath.html')


@app.route('/automation/maven')
@login_required
def automation_maven():
    return render_template('automation/tools/maven.html')


@app.route('/automation/cucumber')
@login_required
def automation_cucumber():
    return render_template('automation/tools/cucumber.html')


@app.route('/automation/jenkins')
@login_required
def automation_jenkins():
    return render_template('automation/tools/jenkins.html')


@app.route('/automation/git')
@login_required
def automation_git():
    return render_template('automation/tools/git.html')


@app.route('/automation/docker')
@login_required
def automation_docker():
    return render_template('automation/tools/docker.html')


@app.route('/automation/ci_cd')
@login_required
def automation_ci_cd():
    return render_template('automation/tools/ci_cd.html')


@app.route('/automation/allure')
@login_required
def automation_allure():
    return render_template('automation/tools/allure.html')


@app.route('/automation/pytest')
@login_required
def automation_pytest():
    return render_template('automation/tools/pytest.html')


@app.route('/automation/testng')
@login_required
def automation_testng():
    return render_template('automation/tools/testng.html')


@app.route('/automation/frameworks')
@login_required
def automation_frameworks():
    return render_template('automation/tools/frameworks.html')


@app.route('/automation/postman')
@login_required
def automation_postman():
    return render_template('automation/tools/postman.html')


@app.route('/automation/appium')
@login_required
def automation_appium():
    return render_template('automation/tools/appium.html')


@app.route('/automation/rest-assured')
@login_required
def automation_rest_assured():
    return render_template('automation/tools/rest_assured.html')


@app.route('/automation/playwright')
@login_required
def automation_playwright():
    return render_template('automation/tools/playwright.html')


# -----------------------------
# Akki AI Chatbot
# -----------------------------
@app.route('/akki_ai')
@login_required
def akki_ai():
    # --- UPDATED: Pass key availability status to the template ---
    return render_template(
        'akki_ai.html',
        openai_available=bool(openai_api_key),
        gemini_available=bool(gemini_api_key)
    )


# -----------------------------
# Offline Akki AI (fallback)
# -----------------------------
@app.route('/akki_ai_api', methods=['POST'])
@login_required
def akki_ai_api():
    """Handles local/offline responses"""
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Please say something!"})

    msg = user_message.lower()
    if "hello" in msg or "hi" in msg:
        reply = f"Hello {session.get('username', 'there')}! How can I help you today?"
    elif "time" in msg:
        from datetime import datetime
        reply = "⏰ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif "date" in msg:
        from datetime import date
        reply = f"📅 {date.today().strftime('%B %d, %Y')}"
    elif "testing" in msg:
        reply = "Software testing ensures apps behave as expected — manual or automation."
    elif "automation" in msg:
        reply = "Automation testing uses scripts to reduce manual effort — e.g., Selenium or Pytest."
    else:
        reply = f"You said: {user_message}. (Offline response.)"

    return jsonify({"reply": reply})
# -----------------------------
# ✅ /generate endpoint (OpenAI + Gemini unified with enhanced safety)
# -----------------------------
@app.route("/generate", methods=["POST"])
@login_required
def generate():
    """
    Generate AI-based responses for Akki AI chatbot.
    Supports both OpenAI and Gemini APIs.
    """
    try:
        # -----------------------------
        # 1️⃣ Get and Validate Input
        # -----------------------------
        data = request.get_json(silent=True) or {}
        prompt = data.get("prompt", "").strip()
        model_choice = data.get("model_choice", "gemini").lower()
        use_grounding = bool(data.get("use_grounding", False))
        system_instruction = data.get("system_instruction", None)

        if not prompt:
            return jsonify({"message": "Please provide a prompt."}), 400

        # -----------------------------
        # 2️⃣ Context-Aware System Prompt
        # -----------------------------
        lang_map = {
            "python": "Python", "java": "Java", "c++": "C++", "cpp": "C++",
            "c program": "C", "javascript": "JavaScript", "js": "JavaScript",
            "html": "HTML", "sql": "SQL"
        }
        detected_lang = next((v for k, v in lang_map.items() if k in prompt.lower()), None)

        system_prompt = (
            "You are Akki AI — a professional QA and Programming Tutor.\n"
            "If the user requests a code example, provide **only runnable code first**, "
            "inside proper fenced markdown (like ```python``` or ```java```), "
            "then give a concise 2–4 line explanation.\n"
            "For QA or testing concepts, give a short practical summary with examples.\n"
        )

        if detected_lang:
            system_prompt += f"Focus on producing valid {detected_lang} code examples.\n"

        if system_instruction:
            system_prompt = system_instruction + "\n" + system_prompt

        # -----------------------------
        # 3️⃣ Dispatch to Model
        # -----------------------------
        if model_choice == "openai" and openai_api_key:
            openai.api_key = openai_api_key
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.6
            )

            result = response.choices[0].message.get("content", "").strip() or "⚠️ No response from OpenAI."
            return jsonify({"result": result, "model": "openai"})

        elif model_choice == "gemini" and gemini_api_key:
            GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={gemini_api_key}"

            payload = {
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"parts": [{"text": prompt}]}]
            }

            if use_grounding:
                payload["tools"] = [{"google_search": {}}]

            r = requests.post(url, json=payload, timeout=45)
            r.raise_for_status()
            j = r.json()

            text = (
                j.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )

            if not text:
                text = "⚠️ Gemini returned no content."

            # Extract optional grounding metadata
            sources = []
            grounding = j.get("candidates", [{}])[0].get("groundingMetadata", {})
            for g in grounding.get("groundingAttributions", []):
                uri = g.get("web", {}).get("uri")
                title = g.get("web", {}).get("title")
                if uri:
                    sources.append({"uri": uri, "title": title or uri})

            return jsonify({"result": text, "sources": sources, "model": "gemini"})

        # -----------------------------
        # 4️⃣ Fallback: Missing Keys
        # -----------------------------
        missing = []
        if model_choice == "openai" and not openai_api_key:
            missing.append("OpenAI key missing.")
        if model_choice == "gemini" and not gemini_api_key:
            missing.append("Gemini key missing.")
        msg = "Offline mode active. " + " ".join(missing or ["No valid model keys found."])
        return jsonify({"result": msg, "model": "local"})

    except requests.exceptions.Timeout:
        return jsonify({"message": "⚠️ Request timed out. Please try again."}), 504

    except requests.exceptions.RequestException as req_err:
        print("🌐 API Request Error:", req_err)
        return jsonify({"message": f"⚠️ External API request failed: {req_err}"}), 502

    except Exception as e:
        print("❌ Unexpected Error in /generate:", e)
        import traceback; traceback.print_exc()
        return jsonify({"message": f"⚠️ Unexpected server error: {e}"}), 500


# -----------------------------
# ✅ Debug Route for API Connectivity Check
# -----------------------------
@app.route("/debug_api")
def debug_api():
    try:
        if not gemini_api_key:
            return "❌ Gemini key missing in environment.", 500

        GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={gemini_api_key}"

        payload = {"contents": [{"parts": [{"text": "connection test"}]}]}
        r = requests.post(url, json=payload, timeout=8)

        status = "✅ Gemini reachable!" if r.ok else "⚠️ Gemini response not OK."
        return f"{status} Status: {r.status_code}<br><pre>{r.text[:400]}</pre>"

    except Exception as e:
        print("❌ Debug API failed:", e)
        return f"❌ Gemini API test failed: {e}", 500



# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    # Ensure all required packages are installed: flask, python-dotenv, requests, openai
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))