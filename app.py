#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from datetime import datetime
from functools import wraps
import sqlite3, os, uuid, logging, hashlib, hmac, secrets
from data import W,G,S,BEST,MAX,P,SCHOLARSHIPS,CHATBOT_QA,PAYMENT_PLANS
from services.payments import PaymentService, normalize_phone, validate_provider

app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY","change-this-in-production")
app.config["JSON_SORT_KEYS"]=False
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
DB_PATH=os.getenv("DATABASE_PATH","payments.db")
payments=PaymentService(DB_PATH)

def db():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c

def init_accounts():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,password_hash TEXT NOT NULL,referral_code TEXT,
            role TEXT NOT NULL DEFAULT 'student',active INTEGER NOT NULL DEFAULT 1,created_at TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS access(
            id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER UNIQUE NOT NULL,paid INTEGER NOT NULL DEFAULT 0,
            plan TEXT,transaction_id TEXT,updated_at TEXT NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id))""")
        cols=[r["name"] for r in c.execute("PRAGMA table_info(payments)").fetchall()]
        if "user_id" not in cols: c.execute("ALTER TABLE payments ADD COLUMN user_id INTEGER")
        c.commit()
init_accounts()

def hash_password(p):
    salt=secrets.token_hex(16)
    return salt+"$"+hashlib.pbkdf2_hmac("sha256",p.encode(),salt.encode(),200000).hex()
def verify_password(p,s):
    try:
        salt,digest=s.split("$",1)
        return hmac.compare_digest(hashlib.pbkdf2_hmac("sha256",p.encode(),salt.encode(),200000).hex(),digest)
    except: return False

def current_user():
    uid=session.get("user_id")
    if not uid:return None
    with db() as c:
        r=c.execute("SELECT * FROM users WHERE id=? AND active=1",(uid,)).fetchone()
    return dict(r) if r else None
def has_paid_access(uid):
    with db() as c:
        r=c.execute("SELECT paid FROM access WHERE user_id=?",(uid,)).fetchone()
    return bool(r and r["paid"])
def set_access(uid,paid,plan=None,tx=None):
    now=datetime.utcnow().isoformat()
    with db() as c:
        c.execute("""INSERT INTO access(user_id,paid,plan,transaction_id,updated_at) VALUES(?,?,?,?,?)
        ON CONFLICT(user_id) DO UPDATE SET paid=excluded.paid,plan=excluded.plan,
        transaction_id=excluded.transaction_id,updated_at=excluded.updated_at""",
        (uid,1 if paid else 0,plan,tx,now)); c.commit()

def login_required(f):
    @wraps(f)
    def w(*a,**k):
        if not current_user(): return redirect(url_for("login",next=request.path))
        return f(*a,**k)
    return w
def paid_required(f):
    @wraps(f)
    def w(*a,**k):
        u=current_user()
        if not u:return redirect(url_for("login",next=request.path))
        if not has_paid_access(u["id"]):return redirect(url_for("dashboard",payment="required"))
        return f(*a,**k)
    return w
def admin_required(f):
    @wraps(f)
    def w(*a,**k):
        u=current_user()
        if not u or u["role"]!="admin":return redirect(url_for("login",admin="1"))
        return f(*a,**k)
    return w

def ensure_admin():
    email=os.getenv("ADMIN_EMAIL","").strip().lower(); password=os.getenv("ADMIN_PASSWORD","")
    if not email or not password:return
    with db() as c:
        r=c.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone()
        if r:c.execute("UPDATE users SET role='admin',password_hash=? WHERE id=?",(hash_password(password),r["id"]))
        else:c.execute("""INSERT INTO users(name,email,phone,password_hash,referral_code,role,created_at)
        VALUES(?,?,?,?,?,?,?)""",("EduPoint Administrator",email,"",hash_password(password),"ADMIN","admin",datetime.utcnow().isoformat()))
        c.commit()
ensure_admin()

@app.get("/")
def home():
    u=current_user()
    return render_template("index.html",plans=PAYMENT_PLANS,providers=payments.available_providers(),
                           user=u,paid=bool(u and has_paid_access(u["id"])))

@app.get("/ref/<code>")
def referral(code):
    session["referral_code"]=code.upper(); return redirect(url_for("home"))
@app.get("/ref")
def referral_query():
    session["referral_code"]=(request.args.get("code") or request.args.get("ref") or "SHARE").upper()
    return redirect(url_for("home"))

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user():return redirect(url_for("dashboard"))
    if request.method=="GET":return render_template("auth.html",mode="register",admin=False)
    d=request.get_json(silent=True) or request.form
    name=str(d.get("name","")).strip(); email=str(d.get("email","")).strip().lower()
    phone=normalize_phone(d.get("phone","")); password=str(d.get("password",""))
    ref=str(d.get("referral_code") or session.get("referral_code") or "").strip().upper()
    if len(name)<2:return jsonify(ok=False,error="Enter your full name."),400
    if "@" not in email:return jsonify(ok=False,error="Enter a valid email address."),400
    if not phone:return jsonify(ok=False,error="Enter a valid Kenyan mobile number."),400
    if len(password)<6:return jsonify(ok=False,error="Password must contain at least 6 characters."),400
    try:
        with db() as c:
            r=c.execute("""INSERT INTO users(name,email,phone,password_hash,referral_code,role,created_at)
            VALUES(?,?,?,?,?,?,?)""",(name,email,phone,hash_password(password),ref or None,"student",datetime.utcnow().isoformat()))
            uid=r.lastrowid;c.commit()
        session["user_id"]=uid;session.pop("referral_code",None)
        return jsonify(ok=True,redirect=url_for("dashboard"))
    except sqlite3.IntegrityError:return jsonify(ok=False,error="An account with that email already exists. Please log in."),409

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user():return redirect(url_for("dashboard"))
    if request.method=="GET":return render_template("auth.html",mode="login",admin=request.args.get("admin")=="1")
    d=request.get_json(silent=True) or request.form
    email=str(d.get("email","")).strip().lower(); password=str(d.get("password",""))
    with db() as c:r=c.execute("SELECT * FROM users WHERE email=? AND active=1",(email,)).fetchone()
    if not r or not verify_password(password,r["password_hash"]):return jsonify(ok=False,error="Incorrect email or password."),401
    session["user_id"]=r["id"]
    return jsonify(ok=True,redirect=url_for("admin" if r["role"]=="admin" else "dashboard"))

@app.get("/logout")
def logout():session.clear();return redirect(url_for("home"))

@app.get("/dashboard")
@login_required
def dashboard():
    u=current_user()
    with db() as c:r=c.execute("SELECT * FROM access WHERE user_id=?",(u["id"],)).fetchone()
    return render_template("dashboard.html",user=u,access=dict(r) if r else None,paid=has_paid_access(u["id"]),
                           plans=PAYMENT_PLANS,providers=payments.available_providers())

@app.post("/api/payment/initiate")
@login_required
def initiate_payment():
    u=current_user();d=request.get_json(silent=True) or request.form
    provider=(d.get("provider") or "").strip().lower();phone=normalize_phone(d.get("phone") or u["phone"])
    plan=(d.get("plan") or "basic").strip().lower()
    if plan not in PAYMENT_PLANS:return jsonify(ok=False,error="Invalid payment plan."),400
    if not validate_provider(provider):return jsonify(ok=False,error="Unsupported payment network."),400
    if not phone:return jsonify(ok=False,error="Enter a valid Kenyan mobile number."),400
    amount=PAYMENT_PLANS[plan]["amount"];tx="EDU-"+uuid.uuid4().hex[:16].upper()
    payments.create_pending(transaction_id=tx,phone=phone,network=provider,amount=amount,plan=plan,user_id=u["id"])
    try:
        r=payments.initiate(provider=provider,phone=phone,amount=amount,transaction_id=tx,plan=plan)
        payments.update(tx,status=r.get("status","pending"),provider_reference=r.get("provider_reference"),message=r.get("message"))
        return jsonify(ok=True,transaction_id=tx,status=r.get("status","pending"),message=r.get("message","Payment request created."),instructions=r.get("instructions",[]))
    except Exception:
        logger.exception("Payment initiation failed");payments.update(tx,status="failed",message="Payment could not be started.")
        return jsonify(ok=False,transaction_id=tx,error="Payment could not be started. Check the API configuration."),502

@app.post("/api/payment/webhook/<provider>")
def payment_webhook(provider):
    if not validate_provider(provider):return jsonify(ok=False,error="Unsupported provider"),404
    payload=request.get_json(silent=True) or request.form.to_dict()
    r=payments.handle_webhook(provider,payload)
    if not r.get("ok"):return jsonify(r),400
    row=payments.get(r.get("transaction_id"))
    if row and r.get("status")=="paid" and row.get("user_id"):set_access(row["user_id"],True,row["plan"],row["transaction_id"])
    return jsonify(ok=True)

@app.get("/api/payment/status/<transaction_id>")
@login_required
def payment_status(transaction_id):
    u=current_user();row=payments.get(transaction_id)
    if not row or (row.get("user_id") and row["user_id"]!=u["id"] and u["role"]!="admin"):return jsonify(ok=False,error="Transaction not found."),404
    if row["status"]=="pending":
        try:
            rr=payments.check_status(row)
            if rr:payments.update(transaction_id,status=rr.get("status",row["status"]),message=rr.get("message"),provider_reference=rr.get("provider_reference"));row=payments.get(transaction_id)
        except Exception:logger.exception("Status check failed")
    if row["status"]=="paid" and row.get("user_id"):set_access(row["user_id"],True,row["plan"],transaction_id)
    return jsonify(ok=True,payment=row,paid=has_paid_access(u["id"]))

@app.get("/api/plans")
def plans():return jsonify(PAYMENT_PLANS)

@app.post("/api/calculate")
@paid_required
def calculate():
    d=request.get_json(silent=True) or {};grades=d.get("grades",{})
    try:
        vals=[W[str(v).strip().upper()] for v in grades.values() if str(v).strip().upper() in W]
        vals=sorted(vals,reverse=True)[:7]
        if len(vals)<7:return jsonify(ok=False,error="Enter at least 7 valid grades."),400
        cp=(sum(vals)/BEST)*MAX
        out=[]
        for course in P:
            diff=cp-course["c"];out.append({**course,"difference":round(diff,3),"match":"qualified" if diff>=0 else ("close" if diff>=-2 else "not_qualified")})
        return jsonify(ok=True,cluster_points=round(cp,3),results=out)
    except Exception as e:return jsonify(ok=False,error=f"Invalid grades: {e}"),400

@app.get("/api/scholarships")
@paid_required
def scholarships():return jsonify(SCHOLARSHIPS)

@app.post("/api/chat")
@paid_required
def chat():
    q=str((request.get_json(silent=True) or {}).get("question","")).lower().strip()
    if not q:return jsonify(answer="Ask me a KUCCPS, course, cluster-points or scholarship question.")
    for x in CHATBOT_QA:
        if any(k in q for k in x["keywords"]):return jsonify(answer=x["answer"])
    return jsonify(answer="I can help with cluster points, KUCCPS courses, admission chances, transfers, scholarships and university requirements.")

@app.get("/admin")
@admin_required
def admin():
    with db() as c:
        users=[dict(r) for r in c.execute("SELECT id,name,email,phone,role,active,referral_code,created_at FROM users ORDER BY id DESC").fetchall()]
        ps=[dict(r) for r in c.execute("SELECT id,transaction_id,user_id,phone,network,amount,plan,status,provider_reference,created_at FROM payments ORDER BY id DESC LIMIT 200").fetchall()]
    return render_template("admin.html",user=current_user(),users=users,payments=ps)

@app.post("/admin/user/<int:user_id>/toggle")
@admin_required
def admin_toggle_user(user_id):
    with db() as c:
        r=c.execute("SELECT active FROM users WHERE id=?",(user_id,)).fetchone()
        if not r:return jsonify(ok=False,error="User not found."),404
        c.execute("UPDATE users SET active=? WHERE id=?",(0 if r["active"] else 1,user_id));c.commit()
    return jsonify(ok=True)

@app.post("/admin/access/<int:user_id>")
@admin_required
def admin_access(user_id):
    d=request.get_json(silent=True) or request.form
    paid=str(d.get("paid","1")).lower() in {"1","true","yes"}
    set_access(user_id,paid,str(d.get("plan") or "admin-granted"),"ADMIN-GRANTED")
    return jsonify(ok=True,paid=paid)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")),debug=False)
