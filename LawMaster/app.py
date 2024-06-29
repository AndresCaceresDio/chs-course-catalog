from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///law_master.db")


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/our-story")
def our_story():
    return render_template("our_story.html")

@app.route("/our-website")
def our_website():
    return render_template("our_website.html")

@app.route('/blog')
def blog():
    cards = [
        {
            "id": 1,
            "url": "https://www.hcpss.org",
            "article-date": "Jan 1, 2020",
            "article-tag": "Law",
            "article-title": "New Legislation",
            "article-author": "John Doe",
            "article-img-src": "https://static.wikia.nocookie.net/rimworld-bestiary/images/4/4d/VerySmallTeeth.png/revision/latest?cb=20210325131516",
            "author-bio-href": "https://www.google.com"
        },
        {
            "id": 2,
            "url": "https://www.xyz.xyz",
            "article-date": "Jan 2, 2020",
            "article-tag": "Tech",
            "article-title": "Tech Mergers",
            "article-author": "Jane Smith",
            "article-img-src": "https://static.wikia.nocookie.net/rimworld-bestiary/images/4/4d/VerySmallTeeth.png/revision/latest?cb=20210325131516",
            "author-bio-href": "https://www.internet.com"
        },
        {
            "id": 3,
            "url": "https://www.fiverr.com",
            "article-date": "Jan 3, 2020",
            "article-tag": "Business",
            "article-title": "Market Trends",
            "article-author": "Ann Brown",
            "article-img-src": "https://static.wikia.nocookie.net/rimworld-bestiary/images/4/4d/VerySmallTeeth.png/revision/latest?cb=20210325131516",
            "author-bio-href": "https://www.scam.com"
        },
        {
            "id": 4,
            "url": "https://www.cars.com",
            "article-date": "May 12, 2024",
            "article-tag": "Seba",
            "article-title": "Seba is Him",
            "article-author": "Sebastian Caceres-Dioverti",
            "article-img-src": "https://static.wikia.nocookie.net/rimworld-bestiary/images/4/4d/VerySmallTeeth.png/revision/latest?cb=20210325131516",
            "author-bio-href": "https://www.sackick.com"
        },
        {
            "id": 5,
            "url": "https://www.carrd.co",
            "article-date": "May 1000, 10000",
            "article-tag": "Code",
            "article-title": "No-Code Solutions for a Particular Use Case",
            "article-author": "Sebastian Caceres-Dioverti",
            "article-img-src": "https://static.wikia.nocookie.net/rimworld-bestiary/images/4/4d/VerySmallTeeth.png/revision/latest?cb=20210325131516",
            "author-bio-href": "https://www.facebook.com"
        }
    ]
    return render_template('blog.html', cards=cards)

@app.route("/explore")
def explore():
    modules = []
    for i in range(len(db.execute("SELECT DISTINCT module FROM contents"))):
        modules.append(db.execute("SELECT DISTINCT module FROM contents")[i]["module"])

    module_links = []
    for i in range(len(db.execute("SELECT DISTINCT module_link FROM contents"))):
        module_links.append(db.execute("SELECT DISTINCT module_link FROM contents")[i]["module_link"])

    module_descriptions = []
    for i in range(len(db.execute("SELECT DISTINCT module_description FROM contents"))):
        module_descriptions.append(db.execute("SELECT DISTINCT module_description FROM contents")[i]["module_description"])

    units = []
    for i in range(len(modules)):
        units.append(db.execute("SELECT DISTINCT unit FROM contents WHERE module = ?", modules[i]))

    return render_template(
        "explore.html",
        modules=modules,
        module_links=module_links,
        module_descriptions=module_descriptions,
        units=units,
        range=range,
        len=len,
    )


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """Register user"""
    session.clear()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirmed_password")
        if (
            not email
            or not password
            or not confirmed_password
        ):
            return render_template(
                "sign_up.html", error_text="ONE OR MORE ENTRIES MISSING"
            )
        if "@" not in email or "." not in email:
            return render_template("sign_up.html", error_text="INVALID EMAIL")
        if len(db.execute("SELECT * FROM users WHERE email = ?", email)) > 0:
            return render_template("sign_up.html", error_text="EMAIL ALREADY IN USE")
        if password != confirmed_password:
            return render_template("sign_up.html", error_text="PASSWORDS DO NOT MATCH")
        password_hash = generate_password_hash(password)
        id = int(db.execute("SELECT MAX(id) FROM users")[0]["MAX(id)"]) + 1
        db.execute(
            "INSERT INTO users (id, email, password_hash) VALUES (?, ?, ?)",
            id,
            email,
            password_hash
        )
        return redirect("/explore")
    elif request.method == "GET":
        return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("email"):
            return render_template(
                "login.html", error_text="EMAIL FIELD CANNOT BE BLANK"
            )
        elif not request.form.get("password"):
            return render_template(
                "login.html", error_text="PASSWORD FIELD CANNOT BE BLANK"
            )
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get("email")
        )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], request.form.get("password")
        ):
            return render_template(
                "login.html", error_text="INVALID USERNAME AND/OR PASSWORD"
            )
        session["user_id"] = rows[0]["email"]
        return redirect("/explore")
    else:
        return render_template("login.html")


@app.route("/log-out")
@login_required
def log_out():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/modules/civil-procedure")
@app.route("/modules/constitutional-law")
@app.route("/modules/contracts")
@app.route("/modules/criminal-law-and-procedure")
@app.route("/modules/evidence")
@app.route("/modules/real-property")
@app.route("/modules/torts")
def module():
    path = request.path

    module_link = path + "/overview"

    module = db.execute("SELECT DISTINCT module FROM contents WHERE module_link = ?", path)[0]["module"]

    units = []
    for i in range(len(db.execute("SELECT DISTINCT unit FROM contents WHERE module = ?", module))):
        units.append(db.execute("SELECT DISTINCT unit FROM contents WHERE module = ?", module)[i]["unit"])

    unit_descriptions = []
    for i in range(len(units)):
        unit_descriptions.append(db.execute("SELECT DISTINCT unit_description FROM contents WHERE unit = ?", units[i])[0]["unit_description"])

    unit_links = []
    for i in range(len(units)):
        unit_links.append(db.execute("SELECT DISTINCT unit_link FROM contents WHERE unit = ?", units[i])[0]["unit_link"])

    topics = []
    for i in range(len(units)):
        topics.append(db.execute("SELECT DISTINCT topic FROM contents WHERE unit = ?", units[i]))

    return render_template(
        "module_page.html",
        module=module,
        units=units,
        unit_descriptions=unit_descriptions,
        unit_links=unit_links,
        topics=topics,
        module_link=module_link,
        range=range,
        len=len,
    )


@app.route("/units/jurisdiction-and-venue")
@app.route("/units/pretrial-procedures")
@app.route("/units/motions")
@app.route("/units/law-applied-by-federal-courts")
@app.route("/units/jury-trials")
@app.route("/units/verdicts-and-judgements")
@app.route("/units/appealability-and-review")
@app.route("/units/individual-rights")
@app.route("/units/the-nature-of-judicial-review")
@app.route("/units/the-separation-of-powers")
@app.route("/units/the-relation-of-nation-and-states")
@app.route("/units/formation-of-contracts")
@app.route("/units/performance,-breach,-and-discharge")
@app.route("/units/defenses-to-enforceability")
@app.route("/units/contract-content-and-meaning")
@app.route("/units/remedies")
@app.route("/units/third-party-rights")
@app.route("/units/protection-of-accused-persons")
@app.route("/units/homicide")
@app.route("/units/other-crimes")
@app.route("/units/inchoate-crimes,-parties")
@app.route("/units/general-principles-of-criminal-law")
@app.route("/units/relevancy-and-reasons-for-excluding-relevant-evidence")
@app.route("/units/hearsay-and-its-circumstances-of-admissibility")
@app.route("/units/presentation-of-evidence")
@app.route("/units/privileges-and-other-policy-exclusions")
@app.route("/units/writings,-recordings,-and-photographs")
@app.route("/units/ownership-of-real-property")
@app.route("/units/rights-in-real-property")
@app.route("/units/real-estate-contracts")
@app.route("/units/mortgages,-security-devices")
@app.route("/units/titles")
@app.route("/units/negligence")
@app.route("/units/intentional-torts")
@app.route("/units/strict-liability-and-products-liability")
@app.route("/units/other-torts")
def unit():
    path = request.path

    unit_link = path + "/overview"

    unit = db.execute("SELECT DISTINCT unit FROM contents WHERE unit_link = ?", path)[0]["unit"]

    topics = []
    for i in range(len(db.execute("SELECT DISTINCT topic FROM contents WHERE unit = ?", unit))):
        topics.append(db.execute("SELECT DISTINCT topic FROM contents WHERE unit = ?", unit)[i]["topic"])

    topic_descriptions = []
    for i in range(len(topics)):
        topic_descriptions.append(db.execute("SELECT DISTINCT topic_description FROM contents WHERE topic = ?", topics[i])[0]["topic_description"])

    topic_links = []
    for i in range(len(topics)):
        topic_links.append(db.execute("SELECT DISTINCT topic_link FROM contents WHERE topic = ?", topics[i])[0]["topic_link"])

    return render_template(
        "unit_page.html",
        unit_link=unit_link,
        unit=unit,
        topics=topics,
        topic_descriptions=topic_descriptions,
        topic_links=topic_links,
        range=range,
        len=len,
    )


@app.route("/topics/federal-subject-matter-jurisdiction")
@app.route("/topics/personal-jurisdiction")
@app.route("/topics/service")
@app.route("/topics/venue")
@app.route("/topics/preliminary-injunctions-and-temporary-restraining-orders")
@app.route("/topics/amended-and-supplemental-pleadings")
@app.route("/topics/rule-11:-the-sanctions-rule")
@app.route("/topics/joinder")
@app.route("/topics/discovery,-disclosure,-and-sanctions")
@app.route("/topics/adjudication-without-trial")
@app.route("/topics/pretrial-conference-&-order")
@app.route("/topics/pretrial-motions")
@app.route("/topics/trial-and-posttrial-motions")
@app.route("/topics/erie-doctrine")
@app.route("/topics/federal-common-law")
@app.route("/topics/jury-trials")
@app.route("/topics/defaults-and-dismissals")
@app.route("/topics/jury-verdicts")
@app.route("/topics/judicial-findings-and-conclusions")
@app.route("/topics/res-judicata-and-collateral-estoppel")
@app.route("/topics/final-judgment-rule-and-the-availability-of-interlocutory-review")
@app.route("/topics/scope-of-review-for-judge-and-jury")
@app.route("/topics/state-action")
@app.route("/topics/due-process")
@app.route("/topics/equal-protection")
@app.route("/topics/takings")
@app.route("/topics/other-protections")
@app.route("/topics/first-amendment-freedoms")
@app.route("/topics/organization-and-relationship-of-state-and-federal-courts-in-a-federal-system")
@app.route("/topics/jurisdiction")
@app.route("/topics/judicial-review")
@app.route("/topics/the-powers-of-congress")
@app.route("/topics/the-powers-of-the-president")
@app.route("/topics/federal-interbranch-relationships")
@app.route("/topics/intergovernmental-immunities")
@app.route("/topics/federalism-based-limits-on-state-authority")
@app.route("/topics/authorization-of-otherwise-invalid-state-action")
@app.route("/topics/mutual-assent")
@app.route("/topics/indefiniteness-and-absence-of-terms")
@app.route("/topics/consideration")
@app.route("/topics/obligations-enforceable-without-a-bargained-for-exchange")
@app.route("/topics/modification-of-contracts")
@app.route("/topics/conditions")
@app.route("/topics/excuse-of-conditions")
@app.route("/topics/breach")
@app.route("/topics/obligations-of-good-faith-and-fair-dealing")
@app.route("/topics/express-and-implied-warranties-in-sale-of-goods-contracts")
@app.route("/topics/other-performance-matters")
@app.route("/topics/impossibility,-impracticability,-and-frustration-of-purpose")
@app.route("/topics/discharge-of-duties")
@app.route("/topics/incapacity-to-contract")
@app.route("/topics/duress-and-undue-influence")
@app.route("/topics/mistake-and-misunderstanding")
@app.route("/topics/fraud,-misrepresentation,-and-nondisclosure")
@app.route("/topics/illegality,-unconscionability,-and-public-policy")
@app.route("/topics/statute-of-frauds")
@app.route("/topics/parol-evidence")
@app.route("/topics/interpretation")
@app.route("/topics/omitted-and-implied-terms")
@app.route("/topics/expectation-interest")
@app.route("/topics/causation,-certainty,-and-foreseeability")
@app.route("/topics/liquidated-damages-and-penalties,-and-limitation-of-remedies")
@app.route("/topics/avoidable-consequences-and-mitigation-of-damages")
@app.route("/topics/rescission-and-reformation")
@app.route("/topics/specific-performance-and-injunction")
@app.route("/topics/reliance-and-restitution-interests")
@app.route("/topics/third-party-beneficiaries")
@app.route("/topics/assignment-of-rights-and-delegation-of-duties")
@app.route("/topics/arrest,-search-and-seizure")
@app.route("/topics/confessions-and-privilege-against-self-incrimination")
@app.route("/topics/lineups-and-other-forms-of-identification")
@app.route("/topics/right-to-counsel")
@app.route("/topics/fair-trial-and-guilty-pleas")
@app.route("/topics/double-jeopardy")
@app.route("/topics/cruel-and-unusual-punishment")
@app.route("/topics/burdens-of-proof-and-persuasion")
@app.route("/topics/appeal-and-error")
@app.route("/topics/intended-killings")
@app.route("/topics/unintended-killings")
@app.route("/topics/theft-and-receiving-stolen-goods")
@app.route("/topics/robbery")
@app.route("/topics/burglary")
@app.route("/topics/assault-and-battery")
@app.route("/topics/rape;-statutory-rape")
@app.route("/topics/kidnapping")
@app.route("/topics/arson")
@app.route("/topics/possession-offenses")
@app.route("/topics/inchoate-offenses")
@app.route("/topics/parties-to-crime")
@app.route("/topics/acts-and-omissions")
@app.route("/topics/state-of-mind")
@app.route("/topics/responsibility")
@app.route("/topics/causation")
@app.route("/topics/justification-and-excuse")
@app.route("/topics/jurisdiction")
@app.route("/topics/probative-value")
@app.route("/topics/authentication-and-identification")
@app.route("/topics/character-and-related-concepts")
@app.route("/topics/expert-testimony")
@app.route("/topics/real,-demonstrative,-and-experimental-evidence")
@app.route("/topics/definition-of-hearsay")
@app.route("/topics/present-sense-impressions-and-excited-utterances")
@app.route("/topics/statements-of-mental,-emotional,-or-physical-condition")
@app.route("/topics/statements-for-purposes-of-medical-diagnosis-and-treatment")
@app.route("/topics/past-recollection-recorded")
@app.route("/topics/business-records")
@app.route("/topics/public-records-and-reports")
@app.route("/topics/learned-treatises")
@app.route("/topics/former-testimony;-depositions")
@app.route("/topics/statements-against-interest")
@app.route("/topics/other-exceptions-to-the-hearsay-rule")
@app.route("/topics/right-to-confront-witnesses")
@app.route("/topics/introduction-of-evidence")
@app.route("/topics/presumptions")
@app.route("/topics/mode-and-order")
@app.route("/topics/impeachment,-contradiction,-and-rehabilitation")
@app.route("/topics/proceedings-to-which-evidence-rules-apply")
@app.route("/topics/spousal-immunity-and-marital-communications")
@app.route("/topics/attorney-client-and-work-product")
@app.route("/topics/physician/psychotherapist-patient")
@app.route("/topics/other-privileges")
@app.route("/topics/insurance-coverage")
@app.route("/topics/remedial-measures")
@app.route("/topics/compromise,-payment-of-medical-expenses,-and-plea-negotiations")
@app.route("/topics/past-sexual-conduct-of-a-victim")
@app.route("/topics/requirement-of-original")
@app.route("/topics/summaries")
@app.route("/topics/completeness-rule")
@app.route("/topics/present-estates-and-future-interests")
@app.route("/topics/cotenancy")
@app.route("/topics/landlord-tenant-law")
@app.route("/topics/special-problems")
@app.route("/topics/restrictive-covenants")
@app.route("/topics/easements,-profits,-and-licenses")
@app.route("/topics/fixtures")
@app.route("/topics/zoning")
@app.route("/topics/real-estate-brokerage")
@app.route("/topics/creation-and-construction")
@app.route("/topics/marketability-of-title")
@app.route("/topics/equitable-conversion")
@app.route("/topics/options-and-rights-of-first-refusal")
@app.route("/topics/fitness-and-suitability")
@app.route("/topics/merger")
@app.route("/topics/types-of-security-devices")
@app.route("/topics/security-relationships")
@app.route("/topics/transfers")
@app.route("/topics/discharge-of-the-mortgage")
@app.route("/topics/foreclosure")
@app.route("/topics/adverse-possession")
@app.route("/topics/transfer-by-deed")
@app.route("/topics/transfer-by-operation-of-law-and-by-will")
@app.route("/topics/title-assurance-systems")
@app.route("/topics/special-problems")
@app.route("/topics/the-duty-question")
@app.route("/topics/the-standard-of-care")
@app.route("/topics/problems-relating-to-proof-of-fault")
@app.route("/topics/problems-relating-to-causation")
@app.route("/topics/limitations-on-liability-and-special-rules-of-liability")
@app.route("/topics/liability-for-acts-of-others")
@app.route("/topics/defenses")
@app.route("/topics/harms-to-the-person")
@app.route("/topics/harms-to-property-interests")
@app.route("/topics/defenses-to-claims-for-physical-harms")
@app.route("/topics/common-law-strict-liability")
@app.route("/topics/claims-against-manufacturers-and-other-defendants")
@app.route("/topics/claims-based-on-nuisance")
@app.route("/topics/claims-based-on-defamation-and-invasion-of-privacy")
@app.route("/topics/claims-based-on-misrepresentations")
@app.route(
    "/topics/claims-based-on-intentional-interference-with-business-relations,-and-defenses"
)
def topic():
    path = request.path

    topic = db.execute("SELECT topic FROM contents WHERE topic_link = ?", path)[0]["topic"]

    unit = db.execute("SELECT unit FROM contents WHERE topic = ?", topic)[0]["unit"]

    topics = []
    for i in range(len(db.execute("SELECT DISTINCT topic FROM contents WHERE unit = ?", unit))):
        topics.append(db.execute("SELECT DISTINCT topic FROM contents WHERE unit = ?", unit)[i]["topic"])

    topic_links = []
    for i in range(len(topics)):
        for j in range(len(db.execute("SELECT DISTINCT topic_link FROM contents WHERE topic = ?", topics[i]))):
            topic_links.append(db.execute("SELECT DISTINCT topic_link FROM contents WHERE topic = ?", topics[i])[j]["topic_link"])

    lesson = db.execute("SELECT lesson FROM contents WHERE topic = ?", topic)[0]["lesson"]

    return render_template("topic_page.html", topic=topic, unit=unit, topics=topics, topic_links=topic_links, lesson=lesson, range=range, len=len)
