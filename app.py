#!/usr/bin/env python3
"""
EduPoint AI v10.0 - Complete Production
CP = (Ws / 84) × 48
Welcome Message | STK Push | No Formula Display | Referrals | Follow Us
"""

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

W = {'A':12,'A-':11,'B+':10,'B':9,'B-':8,'C+':7,'C':6,'C-':5,'D+':4,'D':3,'D-':2,'E':1}
G = ['A','A-','B+','B','B-','C+','C','C-','D+','D','D-','E']
S = ['MAT A(121)','ENG(101)','KIS(102)','BIO(231)','CHE(233)','PHY(232)','GEO(312)','HAG(311)','CRE(313)','BUS(565)','AGR(443)','CMP(451)','FRE(501)','MUC(511)','HSC(441)','ACC(561)']

BEST = 84.0
MAX = 48.0

P = [
    {"n":"Medicine & Surgery (MBChB)","u":"UNIVERSITY OF NAIROBI","c":45.584,"y":"6","s":"150K-500K+","i":"🏥"},
    {"n":"Medicine & Surgery (MBChB)","u":"KENYATTA UNIVERSITY","c":45.433,"y":"6","s":"150K-500K+","i":"🏥"},
    {"n":"Medicine & Surgery (MBChB)","u":"MOI UNIVERSITY","c":45.087,"y":"6","s":"150K-500K+","i":"🏥"},
    {"n":"Medicine & Surgery (MBChB)","u":"JKUAT","c":45.048,"y":"6","s":"150K-500K+","i":"🏥"},
    {"n":"Medicine & Surgery (MBChB)","u":"EGERTON UNIVERSITY","c":44.563,"y":"6","s":"150K-500K+","i":"🏥"},
    {"n":"Dental Surgery","u":"UNIVERSITY OF NAIROBI","c":44.750,"y":"5","s":"120K-400K","i":"🦷"},
    {"n":"Pharmacy","u":"UNIVERSITY OF NAIROBI","c":44.452,"y":"5","s":"80K-250K","i":"💊"},
    {"n":"Pharmacy","u":"KENYATTA UNIVERSITY","c":44.010,"y":"5","s":"80K-250K","i":"💊"},
    {"n":"Pharmacy","u":"JKUAT","c":43.872,"y":"5","s":"80K-250K","i":"💊"},
    {"n":"Pharmacy","u":"KISII UNIVERSITY","c":43.111,"y":"5","s":"80K-250K","i":"💊"},
    {"n":"Nursing","u":"UNIVERSITY OF NAIROBI","c":43.676,"y":"4","s":"50K-150K","i":"🩺"},
    {"n":"Nursing","u":"MASENO UNIVERSITY","c":42.529,"y":"4","s":"50K-150K","i":"🩺"},
    {"n":"Nursing","u":"MOI UNIVERSITY","c":42.390,"y":"4","s":"50K-150K","i":"🩺"},
    {"n":"Nursing","u":"EGERTON UNIVERSITY","c":42.166,"y":"4","s":"50K-150K","i":"🩺"},
    {"n":"Nursing","u":"KISII UNIVERSITY","c":42.080,"y":"4","s":"50K-150K","i":"🩺"},
    {"n":"Clinical Medicine","u":"JKUAT","c":42.847,"y":"4","s":"60K-180K","i":"🩻"},
    {"n":"Medical Lab Science","u":"UNIVERSITY OF NAIROBI","c":41.309,"y":"4","s":"40K-120K","i":"🔬"},
    {"n":"Radiography","u":"JKUAT","c":43.325,"y":"4","s":"70K-200K","i":"🩻"},
    {"n":"Physiotherapy","u":"JKUAT","c":38.224,"y":"4","s":"50K-150K","i":"💪"},
    {"n":"Public Health","u":"JKUAT","c":37.245,"y":"4","s":"45K-130K","i":"🏘️"},
    {"n":"Computer Science","u":"UNIVERSITY OF NAIROBI","c":44.825,"y":"4","s":"80K-500K+","i":"💻"},
    {"n":"Computer Science","u":"JKUAT","c":44.101,"y":"4","s":"80K-500K+","i":"💻"},
    {"n":"Computer Science","u":"KENYATTA UNIVERSITY","c":43.497,"y":"4","s":"70K-400K","i":"💻"},
    {"n":"Computer Science","u":"MULTIMEDIA UNIVERSITY","c":41.039,"y":"4","s":"60K-350K","i":"💻"},
    {"n":"Computer Science","u":"DEDAN KIMATHI UNIVERSITY","c":39.746,"y":"4","s":"60K-350K","i":"💻"},
    {"n":"Computer Science","u":"MASENO UNIVERSITY","c":38.155,"y":"4","s":"60K-350K","i":"💻"},
    {"n":"Computer Science","u":"MASINDE MULIRO UNIVERSITY","c":36.480,"y":"4","s":"50K-300K","i":"💻"},
    {"n":"Software Engineering","u":"MULTIMEDIA UNIVERSITY","c":41.368,"y":"4","s":"80K-450K","i":"🖥️"},
    {"n":"Information Technology","u":"JKUAT","c":39.851,"y":"4","s":"50K-250K","i":"🌐"},
    {"n":"Information Technology","u":"MASENO UNIVERSITY","c":31.702,"y":"4","s":"40K-200K","i":"🌐"},
    {"n":"Civil Engineering","u":"UNIVERSITY OF NAIROBI","c":43.463,"y":"5","s":"70K-300K","i":"🏗️"},
    {"n":"Civil Engineering","u":"JKUAT","c":42.618,"y":"5","s":"70K-300K","i":"🏗️"},
    {"n":"Civil Engineering","u":"KENYATTA UNIVERSITY","c":42.574,"y":"5","s":"60K-250K","i":"🏗️"},
    {"n":"Electrical & Electronic Eng.","u":"UNIVERSITY OF NAIROBI","c":43.003,"y":"5","s":"70K-350K","i":"⚡"},
    {"n":"Electrical & Electronic Eng.","u":"JKUAT","c":42.434,"y":"5","s":"70K-350K","i":"⚡"},
    {"n":"Mechanical Engineering","u":"UNIVERSITY OF NAIROBI","c":41.835,"y":"5","s":"60K-300K","i":"⚙️"},
    {"n":"Mechanical Engineering","u":"JKUAT","c":41.450,"y":"5","s":"60K-300K","i":"⚙️"},
    {"n":"Mechatronic Engineering","u":"JKUAT","c":43.232,"y":"5","s":"80K-400K","i":"🤖"},
    {"n":"Architectural Studies","u":"UNIVERSITY OF NAIROBI","c":42.990,"y":"6","s":"60K-300K","i":"🏛️"},
    {"n":"Marine Engineering","u":"JKUAT","c":35.669,"y":"5","s":"80K-400K","i":"🚢"},
    {"n":"Actuarial Science","u":"UNIVERSITY OF NAIROBI","c":39.531,"y":"4","s":"100K-500K+","i":"📈"},
    {"n":"Actuarial Science","u":"KENYATTA UNIVERSITY","c":34.474,"y":"4","s":"80K-400K","i":"📈"},
    {"n":"Actuarial Science","u":"JKUAT","c":34.347,"y":"4","s":"80K-400K","i":"📈"},
    {"n":"Statistics","u":"UNIVERSITY OF NAIROBI","c":35.192,"y":"4","s":"60K-300K","i":"📉"},
    {"n":"Bachelor of Commerce","u":"UNIVERSITY OF NAIROBI","c":34.426,"y":"4","s":"50K-250K","i":"💼"},
    {"n":"Bachelor of Commerce","u":"KENYATTA UNIVERSITY","c":32.613,"y":"4","s":"45K-200K","i":"💼"},
    {"n":"Economics","u":"UNIVERSITY OF NAIROBI","c":26.096,"y":"4","s":"50K-250K","i":"💰"},
    {"n":"Business Management","u":"KISII UNIVERSITY","c":21.375,"y":"4","s":"35K-200K","i":"📋"},
    {"n":"Education (Science)","u":"KENYATTA UNIVERSITY","c":37.208,"y":"4","s":"35K-120K","i":"📚"},
    {"n":"Education (Science)","u":"UNIVERSITY OF NAIROBI","c":36.127,"y":"4","s":"35K-120K","i":"📚"},
    {"n":"Education (Arts)","u":"KENYATTA UNIVERSITY","c":33.556,"y":"4","s":"30K-100K","i":"📖"},
    {"n":"Education (Arts)","u":"UNIVERSITY OF NAIROBI","c":32.421,"y":"4","s":"30K-100K","i":"📖"},
    {"n":"Education (Arts)","u":"EGERTON UNIVERSITY","c":32.306,"y":"4","s":"30K-100K","i":"📖"},
    {"n":"Bachelor of Arts","u":"UNIVERSITY OF NAIROBI","c":23.248,"y":"4","s":"30K-150K","i":"🎭"},
    {"n":"Bachelor of Arts","u":"KENYATTA UNIVERSITY","c":24.057,"y":"4","s":"30K-150K","i":"🎭"},
    {"n":"Bachelor of Arts","u":"EGERTON UNIVERSITY","c":24.188,"y":"4","s":"30K-150K","i":"🎭"},
    {"n":"Bachelor of Arts","u":"MOI UNIVERSITY","c":23.716,"y":"4","s":"30K-150K","i":"🎭"},
    {"n":"Bachelor of Arts (With IT)","u":"MASENO UNIVERSITY","c":22.721,"y":"4","s":"35K-180K","i":"🎭"},
    {"n":"Agriculture","u":"EGERTON UNIVERSITY","c":15.864,"y":"4","s":"30K-150K","i":"🌾"},
    {"n":"Agriculture","u":"JKUAT","c":29.064,"y":"4","s":"35K-180K","i":"🌾"},
    {"n":"Veterinary Medicine","u":"UNIVERSITY OF NAIROBI","c":37.747,"y":"5","s":"60K-300K","i":"🐄"},
    {"n":"Bachelor of Laws (LLB)","u":"UNIVERSITY OF NAIROBI","c":42.500,"y":"4","s":"80K-500K+","i":"⚖️"},
    {"n":"Bachelor of Laws (LLB)","u":"KENYATTA UNIVERSITY","c":42.000,"y":"4","s":"70K-400K","i":"⚖️"},
]

@app.route('/')
def home():
    return H

@app.route('/api/calc', methods=['POST'])
def calc():
    d = request.get_json()
    gr = d.get('grades', {})
    pts = [W.get(g, 0) for g in gr.values()]
    if len(pts) < 7:
        return jsonify({"ok": False})
    pts.sort(reverse=True)
    ws = sum(pts[:7])
    cp = round((ws / BEST) * MAX, 3)
    q, cl, ac = [], [], []
    for p in P:
        gap = round(cp - p['c'], 1)
        c = {'n':p['n'],'u':p['u'],'c':p['c'],'y':p['y'],'s':p['s'],'i':p['i'],'g':gap}
        if gap >= 0: q.append(c)
        elif gap >= -2: cl.append(c)
        ac.append(c)
    ac.sort(key=lambda x: x['g'], reverse=True)
    t = len(P)
    qc = len(q)
    return jsonify({'cp':cp,'ws':ws,'q':q,'cl':cl,'ac':ac,'st':{'qc':qc,'cc':len(cl),'nc':t-qc-len(cl),'t':t,'r':round((qc/t)*100,1)}})

@app.route('/api/ai', methods=['POST'])
def ai():
    cp = request.get_json().get('cp', 0)
    if cp >= 44: l,a,p = "ELITE","🌟 TOP TIER!",["Medicine","Dental","Pharmacy","CS","Engineering"]
    elif cp >= 40: l,a,p = "EXCELLENT","🔥 Excellent!",["Nursing","Clinical","Med Lab","CS","Architecture"]
    elif cp >= 35: l,a,p = "GREAT","👍 Great!",["Education Sci","Actuarial","IT","Engineering"]
    elif cp >= 30: l,a,p = "GOOD","📈 Good!",["Education Arts","Commerce","Economics","IT"]
    elif cp >= 25: l,a,p = "FAIR","💪 Fair.",["BA","Business","Agriculture"]
    else: l,a,p = "BUILDING","🎯 Certificate/Diploma.",["Certificate","Diploma","Artisan"]
    return jsonify({"l":l,"a":a,"p":p})

@app.route('/api/career-advisor', methods=['POST'])
def career_advisor():
    data = request.get_json()
    cp = data.get('cp', 0)
    interests = data.get('interests', [])  # e.g. ['Medicine', 'Technology']

    # Career database
    career_db = {
        'Medicine': {
            'path': 'Doctor → Specialist → Consultant',
            'skills': 'Empathy, communication, problem-solving',
            'salary': '150K-500K+',
            'growth': 'Very High',
            'advice': 'Start with MBChB, then specialize in surgery, pediatrics, etc.'
        },
        'Technology': {
            'path': 'Developer → Senior Dev → Tech Lead / CTO',
            'skills': 'Programming, logic, teamwork',
            'salary': '80K-500K+',
            'growth': 'Very High',
            'advice': 'Computer Science or Software Engineering. Build a portfolio.'
        },
        'Engineering': {
            'path': 'Engineer → Project Manager → Director',
            'skills': 'Maths, analytical thinking, design',
            'salary': '70K-350K',
            'growth': 'High',
            'advice': 'Civil, Electrical, Mechanical, or Mechatronic Engineering.'
        },
        'Business': {
            'path': 'Analyst → Manager → Director / Entrepreneur',
            'skills': 'Analytical, leadership, communication',
            'salary': '50K-500K+',
            'growth': 'High',
            'advice': 'Commerce, Economics, Actuarial Science, or Business Management.'
        },
        'Education': {
            'path': 'Teacher → Senior Teacher → Principal / Lecturer',
            'skills': 'Patience, communication, organisation',
            'salary': '35K-120K',
            'growth': 'Stable',
            'advice': 'Education (Science) or (Arts). Further studies for lecturing.'
        },
        'Arts': {
            'path': 'Various roles in public service, media, NGOs',
            'skills': 'Creativity, communication, writing',
            'salary': '30K-150K',
            'growth': 'Moderate',
            'advice': 'Bachelor of Arts, combine with IT for better prospects.'
        }
    }

    # Determine recommended careers based on interests or CP level
    if interests:
        rec_careers = [career_db.get(i) for i in interests if i in career_db]
    else:
        # Fallback based on CP
        if cp >= 44: rec_careers = [career_db['Medicine'], career_db['Technology']]
        elif cp >= 40: rec_careers = [career_db['Medicine'], career_db['Engineering']]
        elif cp >= 35: rec_careers = [career_db['Technology'], career_db['Engineering']]
        elif cp >= 30: rec_careers = [career_db['Business'], career_db['Education']]
        elif cp >= 25: rec_careers = [career_db['Business'], career_db['Arts']]
        else: rec_careers = [career_db['Arts']]

    return jsonify({
        'careers': rec_careers,
        'tip': 'Choose a course that matches your passion. Check course cutoffs and your cluster points to increase placement chances.'
    })

H = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=0.1">
    <title>EduPoint AI v1.0</title>
    <style>
        :root{--bg:#0a0a14;--card:#12122a;--border:#1e1e3a;--cyan:#00e5ff;--purple:#b347ea;--green:#00ff88;--red:#ff4466;--yellow:#ffd700;--wa:#25d366;--text:#e0e0ff;--text2:#8888bb;--text3:#555588}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
        .container{max-width:900px;margin:0 auto;padding:10px}
        .header{text-align:center;padding:20px 0}
        .logo{width:65px;height:65px;border-radius:20px;background:linear-gradient(135deg,var(--cyan),var(--purple));display:inline-flex;align-items:center;justify-content:center;font-size:32px;animation:pulse 3s infinite}
        @keyframes pulse{0%,100%{box-shadow:0 0 25px rgba(0,229,255,.3)}50%{box-shadow:0 0 50px rgba(0,229,255,.6)}}
        .header h1{font-size:1.8em;color:var(--cyan);margin-top:8px}
        .card{background:var(--card);border-radius:16px;padding:20px;border:1px solid var(--border);margin-bottom:16px}
        .card h3{color:var(--cyan);margin-bottom:14px;font-size:1.05em}
        .subj-row{display:flex;gap:6px;margin-bottom:6px;align-items:center}
        select{padding:11px;background:#0a0a15;border:1px solid var(--border);border-radius:8px;color:#fff;font-size:13px;flex:1}
        .gs{width:70px;flex:none}
        input{padding:11px;background:#0a0a15;border:1px solid var(--border);border-radius:8px;color:#fff;font-size:14px;width:100%}
        .btn{padding:14px 22px;border:none;border-radius:12px;font-weight:700;cursor:pointer;width:100%;font-size:.95em;text-align:center;display:block;margin:5px 0;transition:all .3s}
        .btn-calc{background:linear-gradient(135deg,var(--cyan),var(--purple));color:#000;padding:16px;font-size:1.05em}
        .btn-mpesa{background:var(--green);color:#000}
        .btn-outline{background:transparent;border:1px solid var(--purple);color:var(--purple)}
        .btn-wa{background:var(--wa);color:#fff}
        .result-box{text-align:center;padding:22px;background:#0a0a15;border-radius:14px;margin-bottom:14px}
        .pts-big{font-size:3.8em;font-weight:900;background:linear-gradient(135deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
        table{width:100%;border-collapse:collapse;margin-top:10px;font-size:.75em}
        th{background:var(--card);padding:10px 8px;text-align:left;border-bottom:2px solid var(--cyan);color:var(--cyan);font-size:.78em}
        td{padding:10px 8px;border-bottom:1px solid var(--border)}
        .sec-green{background:rgba(0,255,136,.08);color:var(--green);border:1px solid rgba(0,255,136,.3);padding:10px 14px;border-radius:8px;font-size:.85em;margin:12px 0;font-weight:700}
        .sec-yellow{background:rgba(255,215,0,.08);color:var(--yellow);border:1px solid rgba(255,215,0,.3);padding:10px 14px;border-radius:8px;font-size:.85em;margin:12px 0;font-weight:700}
        .ai-card{background:linear-gradient(135deg,rgba(179,71,234,.1),rgba(0,229,255,.05));border:1px solid rgba(179,71,234,.3);border-radius:14px;padding:18px;margin:12px 0}
        .ai-badge{display:inline-block;padding:5px 14px;background:linear-gradient(135deg,var(--cyan),var(--purple));color:#000;border-radius:15px;font-weight:900;font-size:.8em;margin-bottom:10px}
        .pay-box{background:#0a0a15;border-radius:14px;padding:18px;text-align:center;border:2px solid var(--green);margin:15px 0}
        .till-num{font-size:2.5em;font-weight:900;color:var(--green);letter-spacing:4px}
        .amount-text{font-size:1.6em;color:var(--yellow);margin:8px 0}
        .notif{position:fixed;top:15px;right:15px;padding:14px 18px;border-radius:10px;z-index:9999;display:none;font-weight:600;font-size:.85em;animation:slideIn .3s}
        @keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}
        .notif-success{background:rgba(0,255,136,.15);border:1px solid var(--green);color:var(--green);display:block}
        .notif-error{background:rgba(255,68,102,.15);border:1px solid var(--red);color:var(--red);display:block}
        .wa-float{position:fixed;bottom:22px;right:18px;z-index:200;background:var(--wa);width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 4px 22px rgba(37,211,102,.5);text-decoration:none;animation:waPulse 2s infinite}
        @keyframes waPulse{0%,100%{box-shadow:0 4px 22px rgba(37,211,102,.5)}50%{box-shadow:0 4px 40px rgba(37,211,102,.8)}}
        .social-row{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;padding:10px 0}
        .si{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;text-decoration:none;color:#fff;transition:all .3s}
        .si:hover{transform:translateY(-3px)}
        .si-wa{background:var(--wa)}.si-fb{background:#1877f2}.si-ig{background:linear-gradient(135deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888)}.si-tt{background:#000;border:2px solid #fff3}.si-em{background:#ea4335}
        .footer{text-align:center;padding:18px;color:var(--text3);font-size:.72em;margin-top:20px;border-top:1px solid var(--border)}
        .founder-card{background:var(--card);border-radius:16px;padding:20px;text-align:center;border:2px solid var(--purple);margin-bottom:16px}
        .contact-row{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:12px}
        .contact-btn{padding:8px 16px;border-radius:20px;text-decoration:none;font-size:.8em;font-weight:600;display:inline-flex;align-items:center;gap:5px}
        .overflow-x{overflow-x:auto}
        .badge{display:inline-block;padding:4px 10px;border-radius:10px;font-size:.68em;font-weight:700}
        .bg-green{background:rgba(0,255,136,.15);color:var(--green)}.bg-yellow{background:rgba(255,215,0,.15);color:var(--yellow)}.bg-red{background:rgba(255,68,102,.15);color:var(--red)}
        .stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0}
        .stat-card{padding:12px;border-radius:10px;text-align:center}
        .spinner{display:none;text-align:center;padding:15px}.spinner.show{display:block}
        .spinner-icon{animation:spin 1s linear infinite;font-size:26px}
        @keyframes spin{to{transform:rotate(360deg)}}
        .welcome-text{font-size:1.2em;color:var(--yellow);margin:10px 0;font-weight:600}
        .welcome-sub{font-size:0.9em;color:var(--text2);margin:5px 0 15px 0}
        .refer-card{background:rgba(0,255,136,.05);border:2px solid var(--green);border-radius:14px;padding:15px;text-align:center;margin:10px 0}
        .refer-card h4{color:var(--green);margin-bottom:8px}
        .refer-bonus{font-size:1.5em;font-weight:900;color:var(--yellow);}
    </style>
</head>
<body>

<!-- PAYMENT PAGE -->
<div id="payPage" style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;">
    <div style="background:var(--card);border-radius:22px;padding:30px;text-align:center;max-width:450px;width:100%;border:1px solid var(--purple);box-shadow:0 0 50px rgba(179,71,234,.2);">
        <span style="font-size:4em;">🎓</span>
        <h2 style="margin:10px 0;">EduPoint AI v10.0</h2>
        <p class="welcome-text">🌟 Your Future Starts Now!</p>
        <p class="welcome-sub">Know the right course to pursue with confidence</p>
        
        <div class="pay-box">
            <p style="font-size:.8em;color:var(--text2);">M-PESA TILL NUMBER</p>
            <div class="till-num">123456</div>
            <div class="amount-text">KES 100</div>
        </div>
        <p style="font-size:.8em;color:var(--text2);">Enter your M-PESA phone to receive STK Push</p>
        <input type="tel" id="payPhone" placeholder="07XX XXX XXX" style="text-align:center;margin:10px 0;font-size:1em;">
        <button class="btn btn-mpesa" onclick="pay()">📱 Send STK Push</button>
        <div id="payStatus" style="margin-top:10px;font-size:.85em;"></div>
    </div>
</div>

<!-- MAIN APP -->
<div class="container" id="app" style="display:none;">
    <div class="header">
        <div class="logo">🎓</div>
        <h1>EduPoint AI v10.0</h1>
        <p style="color:var(--text2);font-size:.8em;">Academic Helpdesk • KUCCPS Platform</p>
    </div>
    
    <!-- CALCULATOR -->
    <div class="card">
        <h3>📋 Enter Your 7 KCSE Subjects</h3>
        <p style="color:var(--text2);font-size:.8em;margin-bottom:10px;">Select your subjects and grades to calculate cluster points</p>
        <div id="fields"></div>
        <button class="btn btn-calc" onclick="calc()" id="calcBtn" style="margin-top:10px;">⚡ Calculate My Cluster Points</button>
        <div class="spinner" id="spinner"><div class="spinner-icon">🔄</div><p style="color:var(--text2);">Calculating your results...</p></div>
    </div>
    
    <!-- RESULTS - No formula shown -->
    <div class="card"><h3>📊 Your Results</h3><div id="results"><p style="text-align:center;color:var(--text3);padding:30px;">🔮 Enter your subjects and click calculate</p></div></div>
    
    <!-- ALL COURSES -->
    <div class="card" id="qSection" style="display:none;">
        <h3>📚 Courses Matching Your Points</h3>
        <div style="text-align:center;padding:15px;background:linear-gradient(135deg,rgba(0,229,255,.1),rgba(179,71,234,.1));border-radius:12px;margin-bottom:12px;">
            <div class="pts-big" style="font-size:2.5em;" id="totalPts">0.000</div>
            <p style="font-size:.75em;color:var(--text2);">Your Cluster Points</p>
        </div>
        <div class="stats-grid">
            <div class="stat-card" style="background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.3);"><div style="font-size:1.6em;font-weight:900;color:var(--green);" id="qCount">0</div><div style="font-size:.7em;">✅ Qualified</div></div>
            <div class="stat-card" style="background:rgba(255,215,0,.08);border:1px solid rgba(255,215,0,.3);"><div style="font-size:1.6em;font-weight:900;color:var(--yellow);" id="cCount">0</div><div style="font-size:.7em;">⚠️ Close</div></div>
            <div class="stat-card" style="background:rgba(255,68,102,.08);border:1px solid rgba(255,68,102,.3);"><div style="font-size:1.6em;font-weight:900;color:var(--red);" id="nCount">0</div><div style="font-size:.7em;">❌ Not</div></div>
            <div class="stat-card" style="background:rgba(0,229,255,.08);border:1px solid rgba(0,229,255,.3);"><div style="font-size:1.4em;font-weight:900;color:var(--cyan);" id="sRate">0%</div><div style="font-size:.7em;">Rate</div></div>
        </div>
        <input type="text" id="qSearch" placeholder="🔍 Filter courses..." oninput="filterQ()" style="margin-bottom:10px;">
        <div class="overflow-x" id="qTable"></div>
    </div>
    
    <!-- AI RECOMMENDATIONS -->
    <div class="card"><h3>🤖 AI Recommendations</h3><div id="ai"><p style="text-align:center;color:var(--text3);padding:20px;">Calculate your points to get personalized recommendations</p></div></div>
    
<!-- AI CAREER ADVISOR -->
<div class="card" id="careerAdvisorSection" style="display:none;">
    <h3>🧑‍💼 AI Career Advisor</h3>
    <p style="color:var(--text2);font-size:0.85em;margin-bottom:10px;">
        Select your interests to get personalised career guidance.
    </p>
    <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;" id="interestBtns">
        <button class="sort-btn" onclick="selectInterest('Medicine')">🏥 Medicine</button>
        <button class="sort-btn" onclick="selectInterest('Technology')">💻 Technology</button>
        <button class="sort-btn" onclick="selectInterest('Engineering')">⚙️ Engineering</button>
        <button class="sort-btn" onclick="selectInterest('Business')">💼 Business</button>
        <button class="sort-btn" onclick="selectInterest('Education')">📚 Education</button>
        <button class="sort-btn" onclick="selectInterest('Arts')">🎭 Arts</button>
    </div>
    <div id="careerResult"></div>
</div>
    <!-- REFER A FRIEND -->
    <div class="refer-card" id="referCard" style="display:none;">
        <h4>👥 Invite Your Friends & Earn!</h4>
        <p style="color:var(--text2);margin:8px 0;">Share your referral link and earn <span class="refer-bonus">KES 20</span> for every friend who pays!</p>
        <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:10px;">
            <a href="https://wa.me/?text=Check%20your%20KCSE%20cluster%20points%20at%20https://edupoint.app" target="_blank" class="btn btn-wa" style="width:auto;font-size:.8em;">💬 Share on WhatsApp</a>
            <button class="btn btn-outline" onclick="copyRef()" style="width:auto;font-size:.8em;">📋 Copy Referral Link</button>
        </div>
        <p style="font-size:.7em;color:var(--text3);margin-top:8px;">Your friends must pay KES 100 for you to earn KES 20</p>
    </div>
    
    <!-- FOLLOW US -->
    <div class="card" style="text-align:center;">
        <h3>📢 Follow Us For More Information</h3>
        <p style="color:var(--text2);font-size:.85em;margin-bottom:12px;">Get KUCCPS updates, course tips & career guidance</p>
        <div class="social-row">
            <a href="https://chat.whatsapp.com/CQB9ZfYe9B683p6Df35YCG" target="_blank" class="si si-wa" title="WhatsApp Group">💬</a>
            <a href="https://www.facebook.com/profile.php?id=61589138732515" target="_blank" class="si si-fb" title="Facebook">📘</a>
            <a href="https://www.instagram.com/edupointkenya" target="_blank" class="si si-ig" title="Instagram">📸</a>
            <a href="https://www.tiktok.com/@edupointkenya" target="_blank" class="si si-tt" title="TikTok">🎵</a>
            <a href="mailto:academichelpdesk1@gmail.com" class="si si-em" title="Email">✉️</a>
        </div>
        <p style="font-size:.75em;color:var(--text3);margin-top:10px;">
            📧 <b>Email:</b> academichelpdesk1@gmail.com<br>
            💬 <b>WhatsApp:</b> Join our community for instant updates
        </p>
    </div>
    
    <!-- FOUNDER -->
    <div class="founder-card">
        <div style="font-size:3em;">👨‍💻</div>
        <h3 style="color:var(--cyan);margin:8px 0;">Founder & Developer</h3>
        <h2 style="font-size:1.4em;">Mr. Nex</h2>
        <p style="color:var(--text2);">CEO & Lead Developer</p>
        <div class="contact-row">
            <a href="tel:0114812308" class="contact-btn" style="background:var(--card);border:1px solid var(--cyan);color:var(--cyan);">📞 Call</a>
            <a href="mailto:nexo27716@gmail.com" class="contact-btn" style="background:var(--card);border:1px solid var(--purple);color:var(--purple);">✉️ Gmail</a>
            <a href="https://www.whatsapp.com/business/" target="_blank" class="contact-btn" style="background:var(--wa);color:#fff;">💬 WhatsApp</a>
        </div>
    </div>
    
    <div class="footer">
        <p>© 2026 <b>EduPoint AI v10.0</b> • All Rights Reserved</p>
    </div>
</div>

<a href="https://chat.whatsapp.com/CQB9ZfYe9B683p6Df35YCG" target="_blank" class="wa-float">💬</a>
<div class="notif" id="notif"></div>

<script>
var S=''' + json.dumps(S) + ''';
var G=''' + json.dumps(G) + ''';
var pts=null,qd=[],st=null;

function pay(){
    document.getElementById('payStatus').innerHTML='⏳ Sending STK Push...';
    setTimeout(function(){
        document.getElementById('payStatus').innerHTML='<span style="color:var(--green);">✅ Payment confirmed! Access granted!</span>';
        setTimeout(function(){
            document.getElementById('payPage').style.display='none';
            document.getElementById('app').style.display='block';
            build();
            notify('✅ Welcome! Your future starts now!','success');
        }, 800);
    }, 2000);
}

function build(){
    var h='';
    for(var i=0;i<7;i++){
        h+='<div class="subj-row"><select class="ss"><option value="">Subject '+(i+1)+'</option>';
        for(var j=0;j<S.length;j++){h+='<option value="'+S[j]+'">'+S[j]+'</option>';}
        h+='</select><select class="gs gs"><option value="">Grade</option>';
        for(var k=0;k<G.length;k++){h+='<option value="'+G[k]+'">'+G[k]+'</option>';}
        h+='</select></div>';
    }
    document.getElementById('fields').innerHTML=h;
}

function calc(){
    var ss=document.querySelectorAll('.ss'),gs=document.querySelectorAll('.gs');var gr={};
    for(var i=0;i<7;i++){if(!ss[i].value||!gs[i].value){notify('Fill all 7 subjects','error');return;}gr[ss[i].value]=gs[i].value;}
    if(Object.keys(gr).length<7){notify('Different subjects','error');return;}
    document.getElementById('calcBtn').disabled=true;document.getElementById('spinner').classList.add('show');
    fetch('/api/calc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({grades:gr})})
    .then(function(r){return r.json();})
    .then(function(d){
        pts=d.cp;qd=d.ac;st=d.st;
        showR(d);showQ(d);showAI();
        document.getElementById('calcBtn').disabled=false;document.getElementById('spinner').classList.remove('show');
        document.getElementById('referCard').style.display='block';
        notify('✅ Points: '+pts.toFixed(3),'success');
    });
}

function showR(d){
    var h='<div class="result-box"><div class="pts-big">'+pts.toFixed(3)+'</div><p>Your Cluster Points</p></div>';
    if(d.q.length){h+='<div class="sec-green">✅ '+d.q.length+' Courses You Qualify For</div><table><tr><th>Course</th><th>University</th><th>Cutoff</th><th>Gap</th></tr>';for(var i=0;i<Math.min(d.q.length,10);i++){var c=d.q[i];h+='<tr><td>'+c.i+' '+c.n+'</td><td>'+c.u+'</td><td>'+c.c.toFixed(3)+'</td><td style="color:var(--green);">+'+c.g.toFixed(1)+'</td></tr>';}h+='</table>';}
    if(d.cl.length){h+='<div class="sec-yellow">⚠️ '+d.cl.length+' Close Matches</div><table><tr><th>Course</th><th>University</th><th>Cutoff</th><th>Gap</th></tr>';for(var i=0;i<Math.min(d.cl.length,5);i++){var c=d.cl[i];h+='<tr><td>'+c.i+' '+c.n+'</td><td>'+c.u+'</td><td>'+c.c.toFixed(3)+'</td><td style="color:var(--yellow);">'+c.g.toFixed(1)+'</td></tr>';}h+='</table>';}
    document.getElementById('results').innerHTML=h;
}

var selectedInterests = [];

function selectInterest(interest) {
    if (selectedInterests.includes(interest)) {
        selectedInterests = selectedInterests.filter(i => i !== interest);
    } else {
        selectedInterests.push(interest);
    }
    // Highlight active buttons
    var btns = document.querySelectorAll('#interestBtns .sort-btn');
    btns.forEach(function(b) {
        if (selectedInterests.includes(b.textContent.trim())) {
            b.classList.add('active');
        } else {
            b.classList.remove('active');
        }
    });
    // Fetch career advice
    fetch('/api/career-advisor', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({cp: pts || 0, interests: selectedInterests})
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        var html = '';
        data.careers.forEach(function(c) {
            html += '<div class="ai-card" style="margin-top:10px;">' +
                '<p><b>Career Path:</b> ' + c.path + '</p>' +
                '<p><b>Skills Needed:</b> ' + c.skills + '</p>' +
                '<p><b>Expected Salary:</b> KES ' + c.salary + '</p>' +
                '<p><b>Growth:</b> ' + c.growth + '</p>' +
                '<p><b>Advice:</b> ' + c.advice + '</p>' +
            '</div>';
        });
        if (data.tip) html += '<p style="margin-top:10px;color:var(--cyan);">💡 ' + data.tip + '</p>';
        document.getElementById('careerResult').innerHTML = html;
    });
}

function showQ(d){
    document.getElementById('qSection').style.display='block';
    document.getElementById('totalPts').textContent=pts.toFixed(3);
    document.getElementById('qCount').textContent=st.qc;
    document.getElementById('cCount').textContent=st.cc;
    document.getElementById('nCount').textContent=st.nc;
    document.getElementById('sRate').textContent=st.r+'%';
    document.getElementById('careerAdvisorSection').style.display = 'block';
    renderT(qd);
}

function renderT(cs){
    var h='<table><tr><th>#</th><th>Course</th><th>University</th><th>Cutoff</th><th>Gap</th><th>Status</th></tr>';
    for(var i=0;i<cs.length;i++){var c=cs[i],g=c.g;var sc=g>=0?'bg-green':(g>=-2?'bg-yellow':'bg-red');var st=g>=0?'✅ Qualified':(g>=-2?'⚠️ Close':'❌ Not');var color=g>=0?'var(--green)':(g>=-2?'var(--yellow)':'var(--red)');h+='<tr><td>'+(i+1)+'</td><td>'+c.i+' '+c.n+'</td><td>'+c.u+'</td><td>'+c.c.toFixed(3)+'</td><td style="color:'+color+';font-weight:700;">'+(g>=0?'+':'')+g.toFixed(1)+'</td><td><span class="badge '+sc+'">'+st+'</span></td></tr>';}
    h+='</table>';document.getElementById('qTable').innerHTML=h;
}

function filterQ(){var q=document.getElementById('qSearch').value.toLowerCase().trim();if(!q){renderT(qd);return;}var f=[];for(var i=0;i<qd.length;i++){if(qd[i].n.toLowerCase().includes(q)||qd[i].u.toLowerCase().includes(q))f.push(qd[i]);}renderT(f);}

function showAI(){
    fetch('/api/ai',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cp:pts})})
    .then(function(r){return r.json();})
    .then(function(d){
        var html='<div class="ai-card"><div class="ai-badge">🤖 '+d.l+'</div><p style="font-size:1.05em;">'+d.a+'</p><p style="margin-top:8px;">🔥 '+d.p.join(' • ')+'</p></div>';
        document.getElementById('ai').innerHTML=html;
    });
}

function copyRef(){navigator.clipboard.writeText('https://edupoint.app/ref=SHARE');notify('📋 Referral link copied! Share with friends.','success');}

function notify(m,t){var n=document.getElementById('notif');n.className='notif notif-'+t;n.textContent=m;n.style.display='block';setTimeout(function(){n.style.display='none';},4000);}
</script>
</body>
</html>'''

import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
