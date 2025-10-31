import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    print("WARNING: OPENAI_API_KEY not found. AI features will not work.")

# -----------------------------
# Flask App Setup
# -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_dev')
app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 10 minutes

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
# Main Pages
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
    return render_template('blog.html')

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

# -----------------------------
# Automation Section
# -----------------------------
@app.route('/automation')
@login_required
def automation_home():
    return render_template('automation/automation.html')

# -----------------------------
# Automation Levels
# -----------------------------
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
# Selenium Section
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
# Java Section
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
# Python Section
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
# Other Automation Tools
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
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

