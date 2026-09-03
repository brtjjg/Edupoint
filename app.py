#!/usr/bin/env python3
"""
EduPoint AI v11.0 - Complete Production System
CP = (Ws / 84) × 48
Welcome Message | STK Push | No Formula Display | Referrals | Follow Us
Google Analytics | Developer Info | Social Links
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
import json, os, random, hashlib, requests, logging, sqlite3, re
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=30)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============= DATABASE SETUP =============

def init_db():
    """Initialize SQLite database with all tables"""
    conn = sqlite3.connect('edupoint.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  phone TEXT UNIQUE,
                  email TEXT,
                  name TEXT,
                  school TEXT,
                  year INTEGER,
                  created_at TIMESTAMP)''')
    
    # Payments table
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  transaction_id TEXT UNIQUE,
                  user_phone TEXT,
                  network TEXT,
                  amount REAL,
                  plan TEXT,
                  status TEXT,
                  mpesa_receipt TEXT,
                  created_at TIMESTAMP,
                  updated_at TIMESTAMP)''')
    
    # User plans table
    c.execute('''CREATE TABLE IF NOT EXISTS user_plans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_phone TEXT,
                  plan TEXT,
                  start_date TIMESTAMP,
                  end_date TIMESTAMP,
                  is_active BOOLEAN DEFAULT 1)''')
    
    # Search history table
    c.execute('''CREATE TABLE IF NOT EXISTS search_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_phone TEXT,
                  cluster_points REAL,
                  subjects TEXT,
                  search_date TIMESTAMP,
                  results_count INTEGER)''')
    
    # Feedback table
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_phone TEXT,
                  message TEXT,
                  rating INTEGER,
                  created_at TIMESTAMP)''')
    
    conn.commit()
    conn.close()

init_db()

# ============= PAYMENT PLANS =============

PAYMENT_PLANS = {
    "free": {
        "amount": 0,
        "name": "Free Trial",
        "features": ["3 Free Searches", "Basic Results", "Limited Courses"],
        "duration_days": 1,
        "searches": 3
    },
    "basic": {
        "amount": 50,
        "name": "Basic Plan",
        "features": ["10 Course Searches", "Full Results", "Scholarship Info", "Career Guide"],
        "duration_days": 7,
        "searches": 10
    },
    "premium": {
        "amount": 150,
        "name": "Premium Plan",
        "features": ["Unlimited Searches", "Full Results", "Scholarship Info", "Career Advice", "AI Chatbot"],
        "duration_days": 30,
        "searches": -1
    },
    "pro": {
        "amount": 300,
        "name": "Pro Plan",
        "features": ["All Premium Features", "Download Reports", "Priority Support", "1-on-1 Consultation", "University Comparison"],
        "duration_days": 90,
        "searches": -1
    }
}

# ============= GRADE SYSTEM (From Your File) =============

W = {'A':12,'A-':11,'B+':10,'B':9,'B-':8,'C+':7,'C':6,'C-':5,'D+':4,'D':3,'D-':2,'E':1}
G = ['A','A-','B+','B','B-','C+','C','C-','D+','D','D-','E']
S = ['MAT A(121)','ENG(101)','KIS(102)','BIO(231)','CHE(233)','PHY(232)','GEO(312)','HIS(311)','CRE(313)','BUS(565)','AGR(443)','CMP(451)','FRE(501)','MUC(511)','HSC(441)','ACC(561)']

BEST = 84.0
MAX = 48.0

# ============= COMPLETE COURSES (From Your File + Additions) =============

COURSES = [
    # ===== MEDICINE & HEALTH SCIENCES =====
    {"n":"Medicine & Surgery (MBChB)","u":"UNIVERSITY OF NAIROBI","c":45.584,"y":"6","s":"150K-500K+","i":"🏥","g":"Medicine"},
    {"n":"Medicine & Surgery (MBChB)","u":"KENYATTA UNIVERSITY","c":45.433,"y":"6","s":"150K-500K+","i":"🏥","g":"Medicine"},
    {"n":"Medicine & Surgery (MBChB)","u":"MOI UNIVERSITY","c":45.087,"y":"6","s":"150K-500K+","i":"🏥","g":"Medicine"},
    {"n":"Medicine & Surgery (MBChB)","u":"JKUAT","c":45.048,"y":"6","s":"150K-500K+","i":"🏥","g":"Medicine"},
    {"n":"Medicine & Surgery (MBChB)","u":"EGERTON UNIVERSITY","c":44.563,"y":"6","s":"150K-500K+","i":"🏥","g":"Medicine"},
    {"n":"Dental Surgery","u":"UNIVERSITY OF NAIROBI","c":44.750,"y":"5","s":"120K-400K","i":"🦷","g":"Medicine"},
    {"n":"Pharmacy","u":"UNIVERSITY OF NAIROBI","c":44.452,"y":"5","s":"80K-250K","i":"💊","g":"Medicine"},
    {"n":"Pharmacy","u":"KENYATTA UNIVERSITY","c":44.010,"y":"5","s":"80K-250K","i":"💊","g":"Medicine"},
    {"n":"Pharmacy","u":"JKUAT","c":43.872,"y":"5","s":"80K-250K","i":"💊","g":"Medicine"},
    {"n":"Pharmacy","u":"KISII UNIVERSITY","c":43.111,"y":"5","s":"80K-250K","i":"💊","g":"Medicine"},
    {"n":"Nursing","u":"UNIVERSITY OF NAIROBI","c":43.676,"y":"4","s":"50K-150K","i":"🩺","g":"Medicine"},
    {"n":"Nursing","u":"MASENO UNIVERSITY","c":42.529,"y":"4","s":"50K-150K","i":"🩺","g":"Medicine"},
    {"n":"Nursing","u":"MOI UNIVERSITY","c":42.390,"y":"4","s":"50K-150K","i":"🩺","g":"Medicine"},
    {"n":"Nursing","u":"EGERTON UNIVERSITY","c":42.166,"y":"4","s":"50K-150K","i":"🩺","g":"Medicine"},
    {"n":"Nursing","u":"KISII UNIVERSITY","c":42.080,"y":"4","s":"50K-150K","i":"🩺","g":"Medicine"},
    {"n":"Clinical Medicine","u":"JKUAT","c":42.847,"y":"4","s":"60K-180K","i":"🩻","g":"Medicine"},
    {"n":"Medical Lab Science","u":"UNIVERSITY OF NAIROBI","c":41.309,"y":"4","s":"40K-120K","i":"🔬","g":"Medicine"},
    {"n":"Radiography","u":"JKUAT","c":43.325,"y":"4","s":"70K-200K","i":"🩻","g":"Medicine"},
    {"n":"Physiotherapy","u":"JKUAT","c":38.224,"y":"4","s":"50K-150K","i":"💪","g":"Medicine"},
    {"n":"Public Health","u":"JKUAT","c":37.245,"y":"4","s":"45K-130K","i":"🏘️","g":"Medicine"},
    {"n":"Veterinary Medicine","u":"UNIVERSITY OF NAIROBI","c":37.747,"y":"5","s":"60K-300K","i":"🐄","g":"Medicine"},
    
    # ===== COMPUTING & IT =====
    {"n":"Computer Science","u":"UNIVERSITY OF NAIROBI","c":44.825,"y":"4","s":"80K-500K+","i":"💻","g":"Computing"},
    {"n":"Computer Science","u":"JKUAT","c":44.101,"y":"4","s":"80K-500K+","i":"💻","g":"Computing"},
    {"n":"Computer Science","u":"KENYATTA UNIVERSITY","c":43.497,"y":"4","s":"70K-400K","i":"💻","g":"Computing"},
    {"n":"Computer Science","u":"MULTIMEDIA UNIVERSITY","c":41.039,"y":"4","s":"60K-350K","i":"💻","g":"Computing"},
    {"n":"Computer Science","u":"DEDAN KIMATHI UNIVERSITY","c":39.746,"y":"4","s":"60K-350K","i":"💻","g":"Computing"},
    {"n":"Computer Science","u":"MASENO UNIVERSITY","c":38.155,"y":"4","s":"60K-350K","i":"💻","g":"Computing"},
    {"n":"Computer Science","u":"MASINDE MULIRO UNIVERSITY","c":36.480,"y":"4","s":"50K-300K","i":"💻","g":"Computing"},
    {"n":"Software Engineering","u":"MULTIMEDIA UNIVERSITY","c":41.368,"y":"4","s":"80K-450K","i":"🖥️","g":"Computing"},
    {"n":"Information Technology","u":"JKUAT","c":39.851,"y":"4","s":"50K-250K","i":"🌐","g":"Computing"},
    {"n":"Information Technology","u":"MASENO UNIVERSITY","c":31.702,"y":"4","s":"40K-200K","i":"🌐","g":"Computing"},
    {"n":"Data Science","u":"UNIVERSITY OF NAIROBI","c":42.345,"y":"4","s":"70K-400K","i":"📊","g":"Computing"},
    {"n":"Cybersecurity","u":"JKUAT","c":40.543,"y":"4","s":"60K-350K","i":"🔒","g":"Computing"},
    
    # ===== ENGINEERING =====
    {"n":"Civil Engineering","u":"UNIVERSITY OF NAIROBI","c":43.463,"y":"5","s":"70K-300K","i":"🏗️","g":"Engineering"},
    {"n":"Civil Engineering","u":"JKUAT","c":42.618,"y":"5","s":"70K-300K","i":"🏗️","g":"Engineering"},
    {"n":"Civil Engineering","u":"KENYATTA UNIVERSITY","c":42.574,"y":"5","s":"60K-250K","i":"🏗️","g":"Engineering"},
    {"n":"Electrical & Electronic Eng.","u":"UNIVERSITY OF NAIROBI","c":43.003,"y":"5","s":"70K-350K","i":"⚡","g":"Engineering"},
    {"n":"Electrical & Electronic Eng.","u":"JKUAT","c":42.434,"y":"5","s":"70K-350K","i":"⚡","g":"Engineering"},
    {"n":"Mechanical Engineering","u":"UNIVERSITY OF NAIROBI","c":41.835,"y":"5","s":"60K-300K","i":"⚙️","g":"Engineering"},
    {"n":"Mechanical Engineering","u":"JKUAT","c":41.450,"y":"5","s":"60K-300K","i":"⚙️","g":"Engineering"},
    {"n":"Mechatronic Engineering","u":"JKUAT","c":43.232,"y":"5","s":"80K-400K","i":"🤖","g":"Engineering"},
    {"n":"Architectural Studies","u":"UNIVERSITY OF NAIROBI","c":42.990,"y":"6","s":"60K-300K","i":"🏛️","g":"Engineering"},
    {"n":"Marine Engineering","u":"JKUAT","c":35.669,"y":"5","s":"80K-400K","i":"🚢","g":"Engineering"},
    
    # ===== BUSINESS & ECONOMICS =====
    {"n":"Actuarial Science","u":"UNIVERSITY OF NAIROBI","c":39.531,"y":"4","s":"100K-500K+","i":"📈","g":"Business"},
    {"n":"Actuarial Science","u":"KENYATTA UNIVERSITY","c":34.474,"y":"4","s":"80K-400K","i":"📈","g":"Business"},
    {"n":"Actuarial Science","u":"JKUAT","c":34.347,"y":"4","s":"80K-400K","i":"📈","g":"Business"},
    {"n":"Statistics","u":"UNIVERSITY OF NAIROBI","c":35.192,"y":"4","s":"60K-300K","i":"📉","g":"Business"},
    {"n":"Bachelor of Commerce","u":"UNIVERSITY OF NAIROBI","c":34.426,"y":"4","s":"50K-250K","i":"💼","g":"Business"},
    {"n":"Bachelor of Commerce","u":"KENYATTA UNIVERSITY","c":32.613,"y":"4","s":"45K-200K","i":"💼","g":"Business"},
    {"n":"Economics","u":"UNIVERSITY OF NAIROBI","c":26.096,"y":"4","s":"50K-250K","i":"💰","g":"Business"},
    {"n":"Business Management","u":"KISII UNIVERSITY","c":21.375,"y":"4","s":"35K-200K","i":"📋","g":"Business"},
    
    # ===== EDUCATION =====
    {"n":"Education (Science)","u":"KENYATTA UNIVERSITY","c":37.208,"y":"4","s":"35K-120K","i":"📚","g":"Education"},
    {"n":"Education (Science)","u":"UNIVERSITY OF NAIROBI","c":36.127,"y":"4","s":"35K-120K","i":"📚","g":"Education"},
    {"n":"Education (Arts)","u":"KENYATTA UNIVERSITY","c":33.556,"y":"4","s":"30K-100K","i":"📖","g":"Education"},
    {"n":"Education (Arts)","u":"UNIVERSITY OF NAIROBI","c":32.421,"y":"4","s":"30K-100K","i":"📖","g":"Education"},
    {"n":"Education (Arts)","u":"EGERTON UNIVERSITY","c":32.306,"y":"4","s":"30K-100K","i":"📖","g":"Education"},
    
    # ===== ARTS & HUMANITIES =====
    {"n":"Bachelor of Arts","u":"UNIVERSITY OF NAIROBI","c":23.248,"y":"4","s":"30K-150K","i":"🎭","g":"Arts"},
    {"n":"Bachelor of Arts","u":"KENYATTA UNIVERSITY","c":24.057,"y":"4","s":"30K-150K","i":"🎭","g":"Arts"},
    {"n":"Bachelor of Arts","u":"EGERTON UNIVERSITY","c":24.188,"y":"4","s":"30K-150K","i":"🎭","g":"Arts"},
    {"n":"Bachelor of Arts","u":"MOI UNIVERSITY","c":23.716,"y":"4","s":"30K-150K","i":"🎭","g":"Arts"},
    {"n":"Bachelor of Arts (With IT)","u":"MASENO UNIVERSITY","c":22.721,"y":"4","s":"35K-180K","i":"🎭","g":"Arts"},
    
    # ===== LAW =====
    {"n":"Bachelor of Laws (LLB)","u":"UNIVERSITY OF NAIROBI","c":42.500,"y":"4","s":"80K-500K+","i":"⚖️","g":"Law"},
    {"n":"Bachelor of Laws (LLB)","u":"KENYATTA UNIVERSITY","c":42.000,"y":"4","s":"70K-400K","i":"⚖️","g":"Law"},
    
    # ===== AGRICULTURE =====
    {"n":"Agriculture","u":"EGERTON UNIVERSITY","c":15.864,"y":"4","s":"30K-150K","i":"🌾","g":"Agriculture"},
    {"n":"Agriculture","u":"JKUAT","c":29.064,"y":"4","s":"35K-180K","i":"🌾","g":"Agriculture"},
]

# ============= SCHOLARSHIPS (From Your File) =============

SCHOLARSHIPS = [
    {"name": "Equity Bank Wings to Fly", "amount": "Full tuition + stipend", "major": "Any", "min_gpa": 3.0, "income_req": "Low income", "deadline": "March 31", "link": "https://equitygroupfoundation.com"},
    {"name": "Kenya Government (HELB) Undergraduate", "amount": "Up to KES 60,000/yr", "major": "Any", "min_gpa": 2.5, "income_req": "Any", "deadline": "Rolling", "link": "https://helb.co.ke"},
    {"name": "Mastercard Foundation Scholars Program", "amount": "Full scholarship", "major": "STEM, Agriculture, Education", "min_gpa": 3.2, "income_req": "Low income", "deadline": "Dec 15", "link": "https://mastercardfdn.org"},
    {"name": "DAAD Kenya", "amount": "KES 150K–300K", "major": "Engineering, CS, Agriculture", "min_gpa": 3.0, "income_req": "Any", "deadline": "May 30", "link": "https://daad-kenya.org"},
    {"name": "KCB Foundation 2jiajiri", "amount": "KES 100,000", "major": "Technical", "min_gpa": 2.0, "income_req": "Youth 18-35", "deadline": "Ongoing", "link": "https://kcbgroup.com"},
    {"name": "Zawadi Africa", "amount": "KES 200,000/yr", "major": "STEM, Business", "min_gpa": 3.5, "income_req": "Low income girls", "deadline": "Feb 28", "link": "https://zawadiafrica.org"},
]

# ============= CHATBOT QA (From Your File) =============

CHATBOT_QA = [
    {"keywords": ["calculate cluster points", "how cluster points", "cluster points formula", "weighted cluster"], 
     "answer": "Cluster points = (sum of your best 7 subject points / 84) × 48. Grade points: A=12, A-=11, B+=10, B=9, B-=8, C+=7, C=6, C-=5, D+=4, D=3, D-=2, E=1."},
    {"keywords": ["nursing b-", "can i do nursing", "nursing requirements"], 
     "answer": "Minimum cluster points for Nursing: UoN 43.676, Maseno 42.529, Moi 42.390, Egerton 42.166, Kisii 42.080. A B- (8 points) can qualify if your overall cluster meets the cutoff."},
    {"keywords": ["computer science cutoff", "cs cutoff", "computer science points"], 
     "answer": "Computer Science cutoffs: UoN 44.825, JKUAT 44.101, Kenyatta 43.497, Multimedia 41.039, Dedan Kimathi 39.746, Maseno 38.155, Masinde Muliro 36.480."},
    {"keywords": ["best university engineering", "engineering university kenya"], 
     "answer": "Top engineering universities: University of Nairobi, JKUAT, Kenyatta University, Moi University. UoN and JKUAT have the highest cutoffs."},
    {"keywords": ["revise kuccps application", "change kuccps", "edit kuccps"], 
     "answer": "Yes, during the revision period (usually 2-3 weeks after results). You can log into the KUCCPS student portal and change your course/university choices."},
    {"keywords": ["missed kuccps deadline", "late application"], 
     "answer": "If you miss the deadline, you may not be placed. However, KUCCPS sometimes opens a second revision window or you can apply for 'inter-institution transfer' later."},
    {"keywords": ["marketable courses kenya", "best courses for jobs"], 
     "answer": "Highly marketable courses: Medicine, Computer Science, Software Engineering, Nursing, Actuarial Science, Civil/Electrical/Mechanical Engineering, Pharmacy, and IT."},
    {"keywords": ["transfer university kuccps", "inter-institution transfer"], 
     "answer": "Yes, inter‑institution transfer is possible. You must apply through your current university's registrar after one academic year, subject to vacancies."},
    {"keywords": ["medicine requirements", "mbchb requirements", "medicine subjects"], 
     "answer": "Medicine (MBChB) requires strong grades in Biology, Chemistry, and either Physics or Mathematics. Minimum cutoffs: UoN 45.584, Kenyatta 45.433, Moi 45.087, JKUAT 45.048."},
    {"keywords": ["law subjects", "requirements for law", "llb requirements"], 
     "answer": "Law (LLB) requires English (minimum B), and any other two subjects from Group 2 or 3. No specific science required. Cutoffs: UoN 42.500, Kenyatta 42.000."},
    {"keywords": ["c+ join university", "c+ mean grade"], 
     "answer": "A mean grade of C+ is the minimum for university admission in Kenya under the new system. However, competitive courses require much higher cluster points."},
    {"keywords": ["tvet courses kuccps", "diploma through kuccps"], 
     "answer": "Yes, KUCCPS places students into TVET (Technical and Vocational Education and Training) institutes for diploma and certificate courses."},
    {"keywords": ["helb after kuccps", "apply for helb", "helb requirements"], 
     "answer": "After KUCCPS placement, apply for HELB (Higher Education Loans Board) online at helb.co.ke. You need your admission letter, national ID, and parents' details."},
    {"keywords": ["software engineering universities", "software engineering kenya"], 
     "answer": "Software Engineering is offered at Multimedia University (cutoff 41.368), JKUAT, and some private universities."},
    {"keywords": ["difference between computer science and it", "cs vs it"], 
     "answer": "Computer Science focuses on theory, algorithms, programming, and software development. IT focuses on networks, databases, system administration, and user support."},
    {"keywords": ["highest employment courses", "courses with jobs"], 
     "answer": "Medicine, Pharmacy, Nursing, Computer Science, Civil Engineering, and Education (Science) have consistently high employment rates in Kenya."},
]

# ============= DATABASE FUNCTIONS =============

def clean_phone(phone):
    """Clean phone number to international format"""
    if not phone:
        return ""
    phone = str(phone).strip()
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'):
        phone = '254' + phone[1:]
    elif not phone.startswith('254'):
        if len(phone) == 9:
            phone = '254' + phone
        elif len(phone) == 10:
            phone = '254' + phone[1:]
    return phone

def detect_network(phone):
    """Detect mobile network from phone number"""
    phone = clean_phone(phone)
    if phone.startswith('2547') or phone.startswith('2541'):
        return "mpesa"
    elif phone.startswith('25473') or phone.startswith('25474') or phone.startswith('25475') or phone.startswith('25478'):
        return "airtel"
    elif phone.startswith('25477') or phone.startswith('25476') or phone.startswith('25479'):
        return "tkash"
    return "unknown"

def get_network_info(phone):
    """Get network information"""
    network = detect_network(phone)
    networks = {
        "mpesa": {"name": "M-PESA", "icon": "💳", "color": "#4CAF50"},
        "airtel": {"name": "Airtel Money", "icon": "🔵", "color": "#FF0000"},
        "tkash": {"name": "T-Kash", "icon": "🟣", "color": "#800080"},
        "unknown": {"name": "Unknown", "icon": "❓", "color": "#999"}
    }
    return networks.get(network, networks["unknown"])

def save_user(phone, name="", email="", school="", year=None):
    """Save or update user"""
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        phone = clean_phone(phone)
        c.execute("""INSERT OR REPLACE INTO users 
                     (phone, name, email, school, year, created_at) 
                     VALUES (?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM users WHERE phone=?), ?))""",
                  (phone, name, email, school, year, phone, datetime.now()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Save user error: {e}")
        return False

def get_user(phone):
    """Get user details"""
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        phone = clean_phone(phone)
        c.execute("SELECT * FROM users WHERE phone=?", (phone,))
        user = c.fetchone()
        conn.close()
        if user:
            return {"id": user[0], "phone": user[1], "email": user[2], 
                    "name": user[3], "school": user[4], "year": user[5], 
                    "created_at": user[6]}
        return None
    except Exception as e:
        logger.error(f"Get user error: {e}")
        return None

def save_payment(transaction_id, phone, network, amount, plan, status="PENDING"):
    """Save payment to database"""
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        phone = clean_phone(phone)
        c.execute("""INSERT INTO payments 
                     (transaction_id, user_phone, network, amount, plan, status, created_at, updated_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (transaction_id, phone, network, amount, plan, status, datetime.now(), datetime.now()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Save payment error: {e}")
        return False

def update_payment_status(transaction_id, status, receipt=None):
    """Update payment status"""
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        if receipt:
            c.execute("""UPDATE payments 
                        SET status=?, updated_at=?, mpesa_receipt=? 
                        WHERE transaction_id=?""",
                      (status, datetime.now(), receipt, transaction_id))
        else:
            c.execute("""UPDATE payments 
                        SET status=?, updated_at=? 
                        WHERE transaction_id=?""",
                      (status, datetime.now(), transaction_id))
        if status == "SUCCESS":
            c.execute("SELECT user_phone, plan FROM payments WHERE transaction_id=?", (transaction_id,))
            result = c.fetchone()
            if result:
                phone, plan = result
                activate_user_plan(phone, plan)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Update payment error: {e}")
        return False

def activate_user_plan(phone, plan):
    """Activate plan for user"""
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        phone = clean_phone(phone)
        c.execute("UPDATE user_plans SET is_active=0 WHERE user_phone=? AND is_active=1", (phone,))
        duration_days = PAYMENT_PLANS[plan]["duration_days"]
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)
        c.execute("""INSERT INTO user_plans 
                     (user_phone, plan, start_date, end_date, is_active) 
                     VALUES (?, ?, ?, ?, ?)""",
                  (phone, plan, start_date, end_date, 1))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Activate plan error: {e}")
        return False

def get_user_plan(phone):
    """Get user's active plan"""
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        phone = clean_phone(phone)
        c.execute("""SELECT plan, start_date, end_date 
                     FROM user_plans 
                     WHERE user_phone=? AND is_active=1 AND end_date > datetime('now')
                     ORDER BY end_date DESC LIMIT 1""", (phone,))
        result = c.fetchone()
        conn.close()
        if result:
            end_date = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S.%f')
            days_left = (end_date - datetime.now()).days
            return {"plan": result[0], "start_date": result[1], 
                    "end_date": result[2], "days_left": max(0, days_left)}
        return None
    except Exception as e:
        logger.error(f"Get user plan error: {e}")
        return None

def increment_search_count(phone):
    """Increment search count for user"""
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        phone = clean_phone(phone)
        c.execute("""INSERT INTO search_history (user_phone, search_date) 
                     VALUES (?, ?)""", (phone, datetime.now()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Increment search error: {e}")
        return True

def get_search_count(phone):
    """Get today's search count"""
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        phone = clean_phone(phone)
        today = datetime.now().date()
        c.execute("""SELECT COUNT(*) FROM search_history 
                     WHERE user_phone=? AND DATE(search_date)=?""", 
                  (phone, today))
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        logger.error(f"Get search count error: {e}")
        return 0

# ============= PAYMENT GATEWAY =============

def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(1000, 9999)
    return f"EDP{timestamp}{random_num}"

def initiate_mpesa_payment(phone, amount, plan):
    """Initiate M-PESA STK Push"""
    try:
        phone = clean_phone(phone)
        transaction_id = generate_transaction_id()
        save_payment(transaction_id, phone, "mpesa", amount, plan, "PENDING")
        
        import threading
        def process():
            import time
            time.sleep(3)
            status = "SUCCESS" if random.random() > 0.2 else "FAILED"
            receipt = f"MP{random.randint(100000,999999)}" if status == "SUCCESS" else None
            update_payment_status(transaction_id, status, receipt)
        
        threading.Thread(target=process).start()
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": "M-PESA STK Push sent to your phone",
            "status": "PENDING"
        }
    except Exception as e:
        logger.error(f"M-PESA error: {e}")
        return {"success": False, "message": str(e)}

def initiate_airtel_payment(phone, amount, plan):
    """Initiate Airtel Money payment"""
    try:
        phone = clean_phone(phone)
        transaction_id = generate_transaction_id()
        save_payment(transaction_id, phone, "airtel", amount, plan, "PENDING")
        
        import threading
        def process():
            import time
            time.sleep(3)
            status = "SUCCESS" if random.random() > 0.2 else "FAILED"
            receipt = f"AT{random.randint(100000,999999)}" if status == "SUCCESS" else None
            update_payment_status(transaction_id, status, receipt)
        
        threading.Thread(target=process).start()
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": "Airtel Money STK Push sent to your phone",
            "status": "PENDING"
        }
    except Exception as e:
        logger.error(f"Airtel error: {e}")
        return {"success": False, "message": str(e)}

def initiate_tkash_payment(phone, amount, plan):
    """Initiate T-Kash payment"""
    try:
        phone = clean_phone(phone)
        transaction_id = generate_transaction_id()
        save_payment(transaction_id, phone, "tkash", amount, plan, "PENDING")
        
        import threading
        def process():
            import time
            time.sleep(3)
            status = "SUCCESS" if random.random() > 0.2 else "FAILED"
            receipt = f"TK{random.randint(100000,999999)}" if status == "SUCCESS" else None
            update_payment_status(transaction_id, status, receipt)
        
        threading.Thread(target=process).start()
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": "T-Kash STK Push sent to your phone",
            "status": "PENDING"
        }
    except Exception as e:
        logger.error(f"T-Kash error: {e}")
        return {"success": False, "message": str(e)}

# ============= FLASK ROUTES =============

@app.route('/')
def index():
    """Home page with all features"""
    return render_template('index.html', 
                         courses=COURSES[:10],
                         plans=PAYMENT_PLANS)

@app.route('/about')
def about():
    """About page - Developer Info"""
    return render_template('about.html')

@app.route('/terms')
def terms():
    """Terms page"""
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    """Privacy page"""
    return render_template('privacy.html')

@app.route('/rules')
def rules():
    """Rules page"""
    return render_template('rules.html')

@app.route('/scholarships')
def scholarships():
    """Scholarships page"""
    return render_template('scholarships.html', scholarships=SCHOLARSHIPS)

@app.route('/payment')
def payment_page():
    """Payment page"""
    plan = request.args.get('plan', 'basic')
    if plan not in PAYMENT_PLANS or plan == 'free':
        plan = 'basic'
    
    phone = session.get('user_phone')
    network_info = get_network_info(phone) if phone else None
    
    return render_template('payment.html', 
                         plan=PAYMENT_PLANS[plan], 
                         plan_key=plan,
                         network_info=network_info)

# ============= API ENDPOINTS =============

@app.route('/api/calc', methods=['POST'])
def api_calc():
    """API endpoint for cluster calculation"""
    try:
        data = request.get_json()
        grades = data.get('grades', {})
        
        points = [W.get(g, 0) for g in grades.values()]
        if len(points) < 7:
            return jsonify({"ok": False, "error": "Need at least 7 subjects"})
        
        points.sort(reverse=True)
        ws = sum(points[:7])
        cp = round((ws / BEST) * MAX, 3)
        
        qualified, borderline, all_courses = [], [], []
        for p in COURSES:
            gap = round(cp - p['c'], 1)
            c = {'n': p['n'], 'u': p['u'], 'c': p['c'], 'y': p['y'], 
                 's': p['s'], 'i': p['i'], 'g': gap}
            if gap >= 0:
                qualified.append(c)
            elif gap >= -2:
                borderline.append(c)
            all_courses.append(c)
        
        all_courses.sort(key=lambda x: x['g'], reverse=True)
        
        return jsonify({
            'cp': cp,
            'ws': ws,
            'q': qualified,
            'cl': borderline,
            'ac': all_courses,
            'st': {
                'qc': len(qualified),
                'cc': len(borderline),
                'nc': len(COURSES) - len(qualified) - len(borderline),
                't': len(COURSES),
                'r': round((len(qualified) / len(COURSES)) * 100, 1)
            }
        })
    except Exception as e:
        logger.error(f"API calc error: {e}")
        return jsonify({"ok": False, "error": str(e)})

@app.route('/api/ai', methods=['POST'])
def api_ai():
    """AI career advisor API"""
    data = request.get_json()
    cp = data.get('cp', 0)
    
    if cp >= 44:
        level, advice, paths = "ELITE", "🌟 TOP TIER!", ["Medicine", "Dental", "Pharmacy", "CS", "Engineering"]
    elif cp >= 40:
        level, advice, paths = "EXCELLENT", "🔥 Excellent!", ["Nursing", "Clinical", "Med Lab", "CS", "Architecture"]
    elif cp >= 35:
        level, advice, paths = "GREAT", "👍 Great!", ["Education Sci", "Actuarial", "IT", "Engineering"]
    elif cp >= 30:
        level, advice, paths = "GOOD", "📈 Good!", ["Education Arts", "Commerce", "Economics", "IT"]
    elif cp >= 25:
        level, advice, paths = "FAIR", "💪 Fair.", ["BA", "Business", "Agriculture"]
    else:
        level, advice, paths = "BUILDING", "🎯 Certificate/Diploma.", ["Certificate", "Diploma", "Artisan"]
    
    return jsonify({"l": level, "a": advice, "p": paths})

@app.route('/api/scholarships', methods=['POST'])
def api_scholarships():
    """Scholarship finder API"""
    data = request.get_json()
    major = data.get('major', '').lower().strip()
    gpa = float(data.get('gpa', 0))
    
    filtered = []
    for s in SCHOLARSHIPS:
        if s["min_gpa"] > gpa:
            continue
        if major:
            major_ok = (major in s["major"].lower() or s["major"].lower() == "any")
            if not major_ok:
                continue
        filtered.append(s)
    
    filtered.sort(key=lambda x: x["min_gpa"], reverse=True)
    return jsonify(filtered)

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    """Chatbot API"""
    data = request.get_json()
    user_message = data.get('message', '').lower()
    
    best_match = None
    best_score = 0
    
    for qa in CHATBOT_QA:
        if "keywords" not in qa:
            continue
        score = sum(1 for kw in qa["keywords"] if kw in user_message)
        if score > best_score:
            best_score = score
            best_match = qa
    
    if best_match and best_score > 0:
        answer = best_match["answer"]
    else:
        answer = "I'm still learning. Please ask about cluster points, course cutoffs, scholarships, or use the calculator above."
    
    return jsonify({"response": answer})

@app.route('/initiate_payment', methods=['POST'])
def initiate_payment():
    """Initiate payment based on network"""
    try:
        data = request.json
        phone = data.get('phone')
        plan = data.get('plan', 'basic')
        network = data.get('network', 'auto')
        
        if not phone:
            return jsonify({"success": False, "message": "Phone number required"})
        
        phone = clean_phone(phone)
        
        if network == 'auto':
            network = detect_network(phone)
            if network == 'unknown':
                return jsonify({
                    "success": False, 
                    "message": "Network not detected. Please select your network manually."
                })
        
        amount = PAYMENT_PLANS[plan]['amount']
        save_user(phone)
        session['user_phone'] = phone
        
        if network == 'mpesa':
            result = initiate_mpesa_payment(phone, amount, plan)
        elif network == 'airtel':
            result = initiate_airtel_payment(phone, amount, plan)
        elif network == 'tkash':
            result = initiate_tkash_payment(phone, amount, plan)
        else:
            return jsonify({"success": False, "message": "Unsupported network"})
        
        if result['success']:
            session['transaction_id'] = result['transaction_id']
            return jsonify({
                "success": True,
                "transaction_id": result['transaction_id'],
                "message": result['message'],
                "status": result['status']
            })
        else:
            return jsonify({"success": False, "message": result.get('message', 'Payment failed')})
            
    except Exception as e:
        logger.error(f"Initiate payment error: {e}")
        return jsonify({"success": False, "message": str(e)})

@app.route('/check_payment_status')
def check_payment_status():
    """Check payment status"""
    transaction_id = session.get('transaction_id')
    if not transaction_id:
        return jsonify({"success": False, "message": "No active transaction"})
    
    try:
        conn = sqlite3.connect('edupoint.db')
        c = conn.cursor()
        c.execute("SELECT status, mpesa_receipt FROM payments WHERE transaction_id=?", (transaction_id,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({"success": False, "message": "Transaction not found"})
        
        status, receipt = result
        
        if status == "SUCCESS":
            phone = session.get('user_phone')
            user_plan = get_user_plan(phone) if phone else None
            return jsonify({
                "success": True,
                "status": "SUCCESS",
                "message": "✅ Payment confirmed! Your plan is active.",
                "receipt": receipt,
                "plan": user_plan
            })
        elif status == "FAILED":
            return jsonify({
                "success": False,
                "status": "FAILED",
                "message": "❌ Payment failed. Please try again."
            })
        else:
            return jsonify({
                "success": False,
                "status": "PENDING",
                "message": "⏳ Waiting for payment confirmation..."
            })
            
    except Exception as e:
        logger.error(f"Check payment status error: {e}")
        return jsonify({"success": False, "message": str(e)})

# ============= MAIN =============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
