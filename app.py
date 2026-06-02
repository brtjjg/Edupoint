#!/usr/bin/env python3
"""
EduPoint AI v10.0 - Complete Production
CP = (Ws / 84) × 48
Welcome Message | STK Push | No Formula Display | Referrals | Follow Us
"""

from flask import Flask, request, jsonify, render_template
import json, os
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

W = {'A':12,'A-':11,'B+':10,'B':9,'B-':8,'C+':7,'C':6,'C-':5,'D+':4,'D':3,'D-':2,'E':1}
G = ['A','A-','B+','B','B-','C+','C','C-','D+','D','D-','E']
S = ['MAT A(121)','ENG(101)','KIS(102)','BIO(231)','CHE(233)','PHY(232)','GEO(312)','HIS(311)','CRE(313)','BUS(565)','AGR(443)','CMP(451)','FRE(501)','MUC(511)','HSC(441)','ACC(561)']

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

# ---------- SCHOLARSHIPS DATA ----------
SCHOLARSHIPS = [
    {"name": "Equity Bank Wings to Fly", "amount": "Full tuition + stipend", "major": "Any", "min_gpa": 3.0, "income_req": "Low income", "deadline": "March 31", "link": "https://equitygroupfoundation.com"},
    {"name": "Kenya Government (HELB) Undergraduate", "amount": "Up to KES 60,000/yr", "major": "Any", "min_gpa": 2.5, "income_req": "Any", "deadline": "Rolling", "link": "https://helb.co.ke"},
    {"name": "Mastercard Foundation Scholars Program", "amount": "Full scholarship", "major": "STEM, Agriculture, Education", "min_gpa": 3.2, "income_req": "Low income", "deadline": "Dec 15", "link": "https://mastercardfdn.org"},
    {"name": "DAAD Kenya", "amount": "KES 150K–300K", "major": "Engineering, CS, Agriculture", "min_gpa": 3.0, "income_req": "Any", "deadline": "May 30", "link": "https://daad-kenya.org"},
    {"name": "KCB Foundation 2jiajiri", "amount": "KES 100,000", "major": "Technical", "min_gpa": 2.0, "income_req": "Youth 18-35", "deadline": "Ongoing", "link": "https://kcbgroup.com"},
    {"name": "Zawadi Africa", "amount": "KES 200,000/yr", "major": "STEM, Business", "min_gpa": 3.5, "income_req": "Low income girls", "deadline": "Feb 28", "link": "https://zawadiafrica.org"},
]

CHATBOT_QA = [
    # Cluster points calculation
    {"keywords": ["calculate cluster points", "how cluster points", "cluster points formula", "weighted cluster"], 
     "answer": "Cluster points = (sum of your best 7 subject points / 84) × 48. Grade points: A=12, A-=11, B+=10, B=9, B-=8, C+=7, C=6, C-=5, D+=4, D=3, D-=2, E=1."},
    
    # Nursing with B-
    {"keywords": ["nursing b-", "can i do nursing", "nursing requirements"], 
     "answer": "Minimum cluster points for Nursing: UoN 43.676, Maseno 42.529, Moi 42.390, Egerton 42.166, Kisii 42.080. A B- (8 points) can qualify if your overall cluster meets the cutoff."},
    
    # Computer Science cutoff
    {"keywords": ["computer science cutoff", "cs cutoff", "computer science points"], 
     "answer": "Computer Science cutoffs: UoN 44.825, JKUAT 44.101, Kenyatta 43.497, Multimedia 41.039, Dedan Kimathi 39.746, Maseno 38.155, Masinde Muliro 36.480."},
    
    # Best university for Engineering
    {"keywords": ["best university engineering", "engineering university kenya"], 
     "answer": "Top engineering universities: University of Nairobi, JKUAT, Kenyatta University, Moi University. UoN and JKUAT have the highest cutoffs."},
    
    # Revise KUCCPS application
    {"keywords": ["revise kuccps application", "change kuccps", "edit kuccps"], 
     "answer": "Yes, during the revision period (usually 2-3 weeks after results). You can log into the KUCCPS student portal and change your course/university choices. The exact dates are announced on the KUCCPS website."},
    
    # Missed deadlines
    {"keywords": ["missed kuccps deadline", "late application"], 
     "answer": "If you miss the deadline, you may not be placed. However, KUCCPS sometimes opens a second revision window or you can apply for 'inter-institution transfer' later. Contact KUCCPS directly for appeals."},
    
    # Marketable courses
    {"keywords": ["marketable courses kenya", "best courses for jobs"], 
     "answer": "Highly marketable courses: Medicine, Computer Science, Software Engineering, Nursing, Actuarial Science, Civil/Electrical/Mechanical Engineering, Pharmacy, and IT. These have strong job prospects in Kenya and abroad."},
    
    # Transfer between universities
    {"keywords": ["transfer university kuccps", "inter-institution transfer"], 
     "answer": "Yes, inter‑institution transfer is possible. You must apply through your current university's registrar after one academic year, subject to vacancies and meeting the target university's requirements."},
    
    # Medicine requirements
    {"keywords": ["medicine requirements", "mbchb requirements", "medicine subjects"], 
     "answer": "Medicine (MBChB) requires strong grades in Biology, Chemistry, and either Physics or Mathematics. Minimum cutoffs: UoN 45.584, Kenyatta 45.433, Moi 45.087, JKUAT 45.048. You need an A or A- in most sciences."},
    
    # Subject combination for Law
    {"keywords": ["law subjects", "requirements for law", "llb requirements"], 
     "answer": "Law (LLB) requires English (minimum B), and any other two subjects from Group 2 or 3. No specific science required. Cutoffs: UoN 42.500, Kenyatta 42.000."},
    
    # C+ mean grade
    {"keywords": ["c+ join university", "c+ mean grade"], 
     "answer": "A mean grade of C+ is the minimum for university admission in Kenya under the new system. However, competitive courses require much higher cluster points. You can also consider diploma or TVET courses."},
    
    # TVET courses
    {"keywords": ["tvet courses kuccps", "diploma through kuccps"], 
     "answer": "Yes, KUCCPS places students into TVET (Technical and Vocational Education and Training) institutes for diploma and certificate courses. Popular TVET options: ICT, Engineering, Hospitality, and Business."},
    
    # HELB application
    {"keywords": ["helb after kuccps", "apply for helb", "helb requirements"], 
     "answer": "After KUCCPS placement, apply for HELB (Higher Education Loans Board) online at helb.co.ke. You need your admission letter, national ID, and parents' details. Applications open after placement announcements."},
    
    # Software Engineering universities
    {"keywords": ["software engineering universities", "software engineering kenya"], 
     "answer": "Software Engineering is offered at Multimedia University (cutoff 41.368), JKUAT, and some private universities. Many students also do Computer Science and later specialize."},
    
    # CS vs IT
    {"keywords": ["difference between computer science and it", "cs vs it"], 
     "answer": "Computer Science focuses on theory, algorithms, programming, and software development. IT focuses on networks, databases, system administration, and user support. Both are marketable; choose CS if you like coding, IT if you prefer infrastructure."},
    
    # High employment courses
    {"keywords": ["highest employment courses", "courses with jobs"], 
     "answer": "Medicine, Pharmacy, Nursing, Computer Science, Civil Engineering, and Education (Science) have consistently high employment rates in Kenya. Actuarial Science also pays well but is competitive."},
    
    # Study abroad after KUCCPS
    {"keywords": ["study abroad after kuccps", "study overseas"], 
     "answer": "Yes, after completing first year, you can apply for transfer to a foreign university. Credits may be transferred. Also, some universities have exchange programmes. Contact your university's international office."},
    
    # Inter-institution transfer details
    {"keywords": ["inter institution transfer", "how to transfer university"], 
     "answer": "Steps: 1) Complete at least one academic year. 2) Get a release letter from your current university. 3) Apply to the target university. 4) KUCCPS approval. Not all courses/universities accept transfers."},
    
    # B plain courses
    {"keywords": ["b plain courses", "courses for b plain"], 
     "answer": "With B plain (about 9 points), you can aim for: Education (Science/Arts), Bachelor of Commerce, Actuarial Science (JKUAT/Kenyatta), IT, and some diploma programmes. Check cluster cutoffs for each."},
    
    # Pilot training requirements
    {"keywords": ["pilot training kenya", "pilot requirements"], 
     "answer": "Pilot training is not under KUCCPS. You need to apply directly to aviation schools (e.g., East African School of Aviation, 43 Air School). Requirements: C+ in KCSE with good grades in Maths, Physics, and English."},
    
    # Admission chances
    {"keywords": ["admission chances", "will i get admitted", "chances of placement"], 
     "answer": "Use the calculator above! Enter your 7 subjects and grades, click 'Calculate My Cluster Points'. The tool will show courses you qualify for (green), close matches (yellow), and not qualified (red). Your chances are high for green courses."},
    
    # Private universities under KUCCPS
    {"keywords": ["private universities kuccps", "private university list"], 
     "answer": "KUCCPS places students into some private universities, including: Strathmore, USIU, Daystar, Catholic University, Africa Nazarene, and others. Government sponsorship may be partial."},
    
    # Minimum grade for Education
    {"keywords": ["education minimum grade", "teaching courses requirements"], 
     "answer": "Education (Arts) cutoffs: Kenyatta 33.556, UoN 32.421, Egerton 32.306. Education (Science) cutoffs: Kenyatta 37.208, UoN 36.127. You need at least a C+ and cluster points above these."},
    
    # Change course after admission
    {"keywords": ["change course after admission", "change course kuccps"], 
     "answer": "You can apply for course change through your university's registrar, usually after first semester. It depends on availability and meeting the new course's minimum requirements. Not always guaranteed."},
    
    # Easiest engineering course
    {"keywords": ["easiest engineering", "lowest engineering cutoff"], 
     "answer": "Among engineering courses, Marine Engineering (JKUAT 35.669) and Mechanical Engineering (UoN 41.835, JKUAT 41.450) have relatively lower cutoffs. Civil/Electrical are higher."},
    
    # Download admission letter
    {"keywords": ["download admission letter", "kuccps admission letter"], 
     "answer": "After KUCCPS placement, log into the KUCCPS student portal (students.kuccps.net). Go to 'My Placement' and click 'Download Admission Letter'. You'll need to print it for university registration."},
    
    # Weighted cluster subjects
    {"keywords": ["weighted cluster subjects", "subject weighting"], 
     "answer": "Some courses weight certain subjects more (e.g., Medicine weights Biology, Chemistry, Physics/Mathematics). The system uses your best 7 subjects, but some courses require specific subjects. Always check individual course requirements."},
    
    # Courses without Mathematics
    {"keywords": ["courses no mathematics", "without maths"], 
     "answer": "Courses that don't require Math: Law, Journalism, Communication, Music, Art, History, Social Work, and many arts/humanities. However, some may require English or a language."},
    
    # Best technology courses
    {"keywords": ["best technology courses kenya", "tech courses"], 
     "answer": "Top technology courses: Computer Science (CS), Software Engineering, Information Technology (IT), Cybersecurity, Data Science, and Artificial Intelligence. CS and SE have the highest demand and salaries."},
    
    # Courses for coding lovers
    {"keywords": ["courses for coding", "love coding"], 
     "answer": "If you love coding, choose: Software Engineering (Multimedia 41.368), Computer Science (UoN, JKUAT, Kenyatta), or IT (JKUAT 39.851). These focus heavily on programming, algorithms, and system design."},
    
    # Compare JKUAT vs KU for CS
    {"keywords": ["jkuat vs ku computer science", "compare jkuat and ku"], 
     "answer": "JKUAT CS cutoff 44.101, KU CS 43.497. JKUAT is more engineering‑oriented, KU has a stronger theoretical base. Both are excellent. JKUAT is located in Juja (quieter), KU is in Kikuyu (near Nairobi). Job prospects are similar."},
    
    # Lowest cutoff universities
    {"keywords": ["lowest cutoff universities", "easy to get in"], 
     "answer": "Some universities with lower cutoffs: Masinde Muliro (CS 36.48), Kisii University (Pharmacy 43.111, Nursing 42.08), Maseno (IT 31.702), JKUAT (Marine Engineering 35.669). Consider these as backup choices."},
    
    # Architecture qualification
    {"keywords": ["architecture requirements", "architecture cutoff"], 
     "answer": "Architecture cutoffs: UoN 42.990. Requires Mathematics, Physics, and Art/Geography. Good drawing skills are an advantage. It's a highly competitive course."},
    
    # Mechatronics careers
    {"keywords": ["mechatronics careers", "mechatronics jobs"], 
     "answer": "Mechatronics Engineering (JKUAT cutoff 43.232) leads to careers in robotics, automation, automotive, manufacturing, and AI hardware. Work as an automation engineer, control systems engineer, or R&D specialist."},
    
    # Government sponsored courses
    {"keywords": ["fully government sponsored", "government sponsorship"], 
     "answer": "Most undergraduate courses at public universities are government‑sponsored (usually 80-90% of fees covered). Private universities have limited government sponsorship. Check your placement letter for 'Government Sponsored' status."},
    
    # Most competitive courses
    {"keywords": ["most competitive courses kenya", "hardest to get into"], 
     "answer": "Most competitive: Medicine (MBChB), Dental Surgery, Pharmacy, Law (LLB), Computer Science (UoN), Actuarial Science (UoN), and Engineering at UoN. They have the highest cluster point cutoffs."},
    
    # Universities offering scholarships
    {"keywords": ["universities with scholarships", "scholarship universities"], 
     "answer": "Many universities have scholarships. Use the Scholarship Finder tool above (enter your GPA and intended major). Also check equitygroupfoundation.com, mastercardfdn.org, and helb.co.ke for loans."},
    
    # Diploma through KUCCPS
    {"keywords": ["diploma kuccps", "apply for diploma"], 
     "answer": "Yes, KUCCPS handles placement for diploma courses (TVET). You can select diploma programmes in the same portal. Minimum grade is C- for most diplomas."},
    
    # Backup courses
    {"keywords": ["backup courses", "what to choose as backup"], 
     "answer": "Choose backup courses with cutoffs 2-5 points lower than your cluster. Examples: Education (Arts), Bachelor of Commerce (Kisii), IT (Maseno), Agriculture (JKUAT). The tool above shows 'Close Matches' – those are good backups."},
    
    # Default fallback
    {"keywords": ["default"], 
     "answer": "I'm not sure about that. Try asking about cluster points calculation, specific course cutoffs, KUCCPS procedures, or use the tools above (Calculator, Scholarship Finder, AI Career Advisor). You can also email academichelpdesk1@gmail.com for detailed help."}
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

@app.route('/terms')
def terms():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Terms & Conditions - EduPoint AI</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0a0a14;
                color: #e0e0ff;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: #12122a;
                padding: 30px;
                border-radius: 16px;
                border: 1px solid #1e1e3a;
            }
            h1, h2 {
                color: #00e5ff;
            }
            a {
                color: #00ff88;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #00e5ff;
                color: #000;
                border-radius: 8px;
                font-weight: bold;
           .chat-message {
    margin-bottom: 10px;
    padding: 8px 12px;
    border-radius: 18px;
    max-width: 85%;
    word-wrap: break-word;
}
.user-message {
    background: linear-gradient(135deg, var(--cyan), var(--purple));
    color: #000;
    margin-left: auto;
    text-align: right;
}
.bot-message {
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--text);
}
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Terms & Conditions</h1>
            <p><strong>Last updated:</strong> May 29, 2026</p>
            
            <h2>1. Acceptance of Terms</h2>
            <p>By accessing or using EduPoint AI ("the Service"), you agree to be bound by these Terms. If you disagree, please do not use the Service.</p>
            
            <h2>2. Description of Service</h2>
            <p>EduPoint AI provides KCSE cluster points calculation, course recommendations, AI career advice, and scholarship information. The results are estimates and not official KUCCPS placement guarantees.</p>
            
            <h2>3. Payments & Refunds</h2>
            <p>Access to premium features requires a one-time payment of KES 100 via M-PESA. All payments are non-refundable unless technical issues prevent access. In case of errors, contact us at <a href="mailto:academichelpdesk1@gmail.com">academichelpdesk1@gmail.com</a>.</p>
            
            <h2>4. User Responsibilities</h2>
            <p>You agree to provide accurate information. You are responsible for maintaining the confidentiality of your M-PESA transactions.</p>
            
            <h2>5. Intellectual Property</h2>
            <p>All content, logos, and code are owned by EduPoint AI. You may not reproduce or distribute without permission.</p>
            
            <h2>6. Limitation of Liability</h2>
            <p>EduPoint AI is not liable for any decisions made based on our calculations or recommendations. Always verify with official KUCCPS sources.</p>
            
            <h2>7. Changes to Terms</h2>
            <p>We may update these Terms. Continued use constitutes acceptance of the new Terms.</p>
            
            <h2>8. Contact Us</h2>
            <p>Email: <a href="mailto:academichelpdesk1@gmail.com">academichelpdesk1@gmail.com</a><br>
            WhatsApp: <a href="https://chat.whatsapp.com/CQB9ZfYe9B683p6Df35YCG" target="_blank">Join our WhatsApp Group</a></p>
            
            <a href="/" class="back-link">← Back to Home</a>
        </div>
    </body>
    </html
    '''
@app.route('/privacy')
def privacy():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Privacy Policy - EduPoint AI</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0a0a14;
                color: #e0e0ff;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: #12122a;
                padding: 30px;
                border-radius: 16px;
                border: 1px solid #1e1e3a;
            }
            h1, h2 {
                color: #00e5ff;
            }
            a {
                color: #00ff88;
                text-decoration: none;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #00e5ff;
                color: #000;
                border-radius: 8px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Privacy Policy</h1>
            <p><strong>Last updated:</strong> May 29, 2026</p>
            
            <h2>1. Information We Collect</h2>
            <p>We collect the KCSE subjects and grades you enter, your M-PESA phone number (only for payment processing), and any information you voluntarily provide (e.g., email, interests). We also collect anonymous usage data via Google Analytics.</p>
            
            <h2>2. How We Use Your Information</h2>
            <p>Your grades are used solely to calculate cluster points and recommend courses. Phone numbers are used only to send M-PESA STK push notifications (if you choose to pay). We do not sell or share your personal data with third parties.</p>
            
            <h2>3. Data Storage & Security</h2>
            <p>We do not permanently store your grades or results unless you create an account (future feature). M-PESA transactions are processed through Safaricom's API; we do not store your payment details. We take reasonable measures to protect your data.</p>
            
            <h2>4. Cookies & Tracking</h2>
            <p>We use Google Analytics to understand how visitors use our site. Google may set cookies. You can disable cookies in your browser settings.</p>
            
            <h2>5. Third-Party Links</h2>
            <p>Our site links to external websites (scholarships, WhatsApp, social media). We are not responsible for their privacy practices.</p>
            
            <h2>6. Your Rights</h2>
            <p>You may request deletion of any personal data we hold by contacting us below.</p>
            
            <h2>7. Changes to This Policy</h2>
            <p>We may update this policy. Continued use constitutes acceptance.</p>
            
            <h2>8. Contact Us</h2>
            <p>Email: <a href="mailto:academichelpdesk1@gmail.com">academichelpdesk1@gmail.com</a></p>
            
            <a href="/" class="back-link">← Back to Home</a>
        </div>
    </body>
    </html>
    '''
@app.route('/rules')
def rules():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rules & Regulations – EduPoint</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0a0a14;
            color: #e0e0ff;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 900px;
            margin: auto;
            background: #12122a;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #1e1e3a;
        }
        h1, h2 {
            color: #00e5ff;
        }
        h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        h2 {
            font-size: 1.4em;
            margin-top: 20px;
        }
        a {
            color: #00ff88;
            text-decoration: none;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #00e5ff;
            color: #000;
            border-radius: 8px;
            font-weight: bold;
        }
        hr {
            border-color: #1e1e3a;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>📜 EduPoint Rules & Regulations</h1>
    <p><strong>Last updated:</strong> June 2, 2026</p>
    <hr>

    <h2>1. Purpose of EduPoint</h2>
    <p>EduPoint is an educational and career guidance platform designed to help students understand KUCCPS requirements, calculate cluster points, explore university courses, and receive career guidance. The platform must be used strictly for educational purposes only.</p>

    <h2>2. User Eligibility</h2>
    <p>By using EduPoint, you confirm that you are a student or individual seeking educational guidance, you are at least 13 years old (or using under parental guidance), and all information provided is accurate. False or misleading information may lead to suspension.</p>

    <h2>3. Account Registration and Security</h2>
    <p>Users must create only one account per person, use valid contact details, keep credentials private, and not share accounts. Users are responsible for any activity under their account.</p>

    <h2>4. Acceptable Use Policy</h2>
    <p><strong>Allowed:</strong> Learning, using calculators, AI guidance, purchasing premium reports.<br>
    <strong>Prohibited:</strong> Illegal activities, hacking, bots, false data, spamming, or abuse of any system feature.</p>

    <h2>5. Content Accuracy and Responsibility</h2>
    <p>EduPoint provides guidance based on available data, but admission suggestions are not guarantees. Users must confirm final decisions with official KUCCPS and universities. EduPoint is not liable for user decisions.</p>

    <h2>6. Premium Services (KES 100)</h2>
    <p>Paid reports are non‑refundable once generated, for personal use only, and cannot be shared or resold. Fraudulent payment attempts will result in account termination.</p>

    <h2>7. Payment and Fraud Prevention</h2>
    <p>All payments must be via approved methods (e.g., M‑PESA). Fake transaction confirmations are prohibited. EduPoint may verify transactions before granting access.</p>

    <h2>8. Email and Phone Verification</h2>
    <p>Verification may be required for full access. Do not use fake or temporary contact details. Verified accounts may receive additional features.</p>

    <h2>9. Data Usage and Privacy</h2>
    <p>We collect limited data (email, grades, preferences) only for educational recommendations. Data is not sold. Users can request account deletion.</p>

    <h2>10. System Integrity and Security</h2>
    <p>No hacking, interference, or exploitation of bugs. EduPoint may log suspicious activity.</p>

    <h2>11. Fair Usage Policy</h2>
    <p>Excessive requests, abuse of AI tools, or data scraping may lead to throttling or restriction.</p>

    <h2>12. WhatsApp Community Rules</h2>
    <p>Be respectful, no spam, false info, or harassment. Violation may result in removal.</p>

    <h2>13. Intellectual Property</h2>
    <p>All content (software, AI systems, reports, branding) is owned by EduPoint. Do not copy or resell without permission.</p>

    <h2>14. Service Availability</h2>
    <p>We aim for continuous access, but downtime may occur for maintenance. Features may be modified without notice.</p>

    <h2>15. Account Suspension and Termination</h2>
    <p>EduPoint may suspend accounts that violate rules or engage in fraud, without prior notice if necessary.</p>

    <h2>16. Updates to Rules</h2>
    <p>These rules may be updated at any time. Continued use means acceptance of updated rules.</p>

    <hr>
    <p><strong>⚡ Final Note:</strong> EduPoint is built to support students in making informed career decisions. These rules ensure fairness, security, and trust for all users.</p>

    <a href="/" class="back-link">← Back to Home</a>
</div>
</body>
</html>'''

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

@app.route('/api/scholarships', methods=['POST'])
def scholarships():
    data = request.get_json()
    major = data.get('major', '').lower().strip()
    gpa = float(data.get('gpa', 0))
    
    filtered = []
    for s in SCHOLARSHIPS:
        # Check GPA
        if s["min_gpa"] > gpa:
            continue
        # Check major match (if major is specified)
        if major:
            major_ok = (major in s["major"].lower() or 
                        s["major"].lower() == "any")
            if not major_ok:
                continue
        filtered.append(s)
    
    # Sort by highest GPA requirement (most selective first)
    filtered.sort(key=lambda x: x["min_gpa"], reverse=True)
    return jsonify(filtered)

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
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
        # fallback to default
        for qa in CHATBOT_QA:
            if qa.get("keywords") == ["default"]:
                answer = qa["answer"]
                break
        else:
            answer = "I'm still learning. Please ask about cluster points, course cutoffs, scholarships, or use the calculator above."
    
    return jsonify({"response": answer})

@app.route('/about')
def about():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About EduPoint – Your Future, Guided by AI</title>
    <style>
        :root{--bg:#0a0a14;--card:#12122a;--border:#1e1e3a;--cyan:#00e5ff;--purple:#b347ea;--green:#00ff88;--yellow:#ffd700;--text:#e0e0ff;--text2:#8888bb}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--text);padding:20px;line-height:1.6}
        .container{max-width:900px;margin:0 auto}
        .card{background:var(--card);border-radius:16px;padding:30px;border:1px solid var(--border);margin-bottom:20px}
        h1,h2{color:var(--cyan);margin-bottom:15px}
        h1{font-size:2.2em}
        h2{font-size:1.5em;margin-top:20px}
        .founder-quote{background:rgba(0,229,255,0.05);border-left:4px solid var(--cyan);padding:15px;margin:20px 0}
        .stats{display:flex;justify-content:space-between;flex-wrap:wrap;gap:15px;margin:20px 0}
        .stat{background:rgba(0,255,136,0.05);padding:15px;border-radius:12px;flex:1;text-align:center}
        .stat-number{font-size:2em;color:var(--green);font-weight:bold}
        .btn{display:inline-block;background:linear-gradient(135deg,var(--cyan),var(--purple));color:#000;padding:12px 24px;border-radius:12px;text-decoration:none;font-weight:bold;margin-top:15px}
        a{color:var(--green)}
        .footer{text-align:center;margin-top:30px;color:var(--text2)}
    </style>
</head>
<body>
<div class="container">
    <div class="card">
        <h1>📘 About EduPoint</h1>
        <p style="font-size:1.2em; color:var(--yellow);">Your Future, Guided by AI</p>
        
        <h2>🌟 Our Mission</h2>
        <p>EduPoint is an education and career guidance platform designed to help students in Kenya make smarter decisions about their future. Our mission is to simplify KUCCPS selection, course discovery, and career planning using technology, data, and AI‑powered insights. We believe every student deserves clear, accurate, and accessible information when choosing their academic and professional path.</p>
        
        <h2>🚀 What EduPoint Does</h2>
        <p>EduPoint provides tools that help students:</p>
        <ul>
            <li>Calculate cluster points easily</li>
            <li>Discover suitable university courses</li>
            <li>Compare different career paths</li>
            <li>Check admission chances</li>
            <li>Explore universities in Kenya</li>
            <li>Get personalized AI career guidance</li>
        </ul>
        <p>We turn complex admission data into simple, understandable guidance.</p>
        
        <div class="founder-quote">
            <h3>👨‍💻 The Founder</h3>
            <p><strong>Brian Ondieki</strong> – Founder & Developer, EduPoint</p>
            <p><em>“I built EduPoint to help students see their future more clearly. By combining data and technology, we can make education decisions easier, faster, and more accurate.”</em></p>
            <p>EduPoint was created from a simple observation: many students struggle to understand KUCCPS requirements and end up choosing courses without clear guidance.</p>
        </div>
        
        <h2>🎯 Our Vision</h2>
        <p>To become the leading student career guidance platform in Africa, empowering learners to make informed decisions from secondary school to university and beyond.</p>
        
        <h2>💡 Why EduPoint Exists</h2>
        <p>Many students face challenges like confusion during KUCCPS applications, lack of career guidance, limited access to course information, and poor understanding of cluster points. EduPoint solves these problems by providing a centralized, intelligent system for academic planning.</p>
        
        <div class="stats">
            <div class="stat"><div class="stat-number">200+</div><div>Courses Analyzed</div></div>
            <div class="stat"><div class="stat-number">30+</div><div>Universities</div></div>
            <div class="stat"><div class="stat-number">AI-Powered</div><div>Recommendations</div></div>
        </div>
        
        <h2>📊 What Makes Us Different</h2>
        <ul>
            <li>AI-powered career recommendations</li>
            <li>Real‑time admission probability insights</li>
            <li>Simple and student‑friendly tools</li>
            <li>Kenya‑focused education data</li>
            <li>Affordable premium reports (KES 100)</li>
        </ul>
        
        <h2>🤝 Join Our Community</h2>
        <p>We are building a community of students, educators, and career explorers. Join us and take control of your academic future.</p>
        <a href="/" class="btn">🎓 Start Your Journey</a>
        
        <h2>📬 Contact Us</h2>
        <p>For support, feedback, or partnerships:<br>
        📧 <a href="mailto:support@edupoint.com">support@edupoint.com</a><br>
        (Replace with your real email – currently academichelpdesk1@gmail.com)</p>
    </div>
    <div class="footer">
        <a href="/" style="color:var(--cyan);">🏠 Home</a> | <a href="/terms" style="color:var(--cyan);">Terms</a> | <a href="/privacy" style="color:var(--cyan);">Privacy</a>
    </div>
</div>
</body>
</html>'''

H = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=0.5">
    <title>EduPoint AI v0.5</title>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EL5HEN57G3"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-EL5HEN57G3');
    </script>
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
        .refer-bonus{font-size:1.5em;font-weight:900;color:var(--yellow)}
        .trust-badge{display:inline-block;background:rgba(0,255,136,.1);border-radius:20px;padding:5px 12px;margin:5px;font-size:.75em;color:var(--green)}
        .sort-btn{background:rgba(0,229,255,.1);border:1px solid var(--cyan);border-radius:20px;padding:6px 12px;cursor:pointer;color:var(--cyan);margin:4px;transition:0.3s}
        .sort-btn:hover{background:var(--cyan);color:#000}
    </style>
</head>
<body>

<!-- LANDING PAGE (free preview) -->
<div id="landingPage" style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;">
    <div style="background:var(--card);border-radius:22px;padding:30px;max-width:550px;width:100%;text-align:center;">
        <span style="font-size:4em;">🎓</span>
        <h2 style="margin:10px 0;color:var(--cyan);">EduPoint AI v10.0</h2>
        <p style="color:var(--text2);">Your smart KCSE cluster points calculator & course advisor</p>
        
        <div class="card" style="margin:20px 0;text-align:left;">
            <h3>📋 Enter Your 7 Subjects</h3>
            <div id="previewFields"></div>
            <button class="btn btn-calc" onclick="previewCluster()" style="margin-top:10px;">⚡ Check My Cluster Points (Free)</button>
            <div id="previewResult" style="margin-top:15px;display:none;">
                <div class="sec-green" style="text-align:center;">
                    🎯 Estimated Cluster Points: <strong id="estPoints">0.000</strong>
                </div>
                <div style="text-align:center;margin-top:15px;">
                    <button class="btn btn-mpesa" onclick="showPaymentPage()">🔓 Unlock Full Analysis (KES 100)</button>
                </div>
            </div>
        </div>
        
        <div style="margin-top:20px;">
            <span class="trust-badge">✅ Secure M-PESA Payment</span>
            <span class="trust-badge">⚡ Instant Results</span>
            <span class="trust-badge">📚 Trusted by Students</span>
        </div>
    </div>
</div>
 
       <div class="footer">
    <p>© 2026 <b>EduPoint AI v10.0</b> • All Rights Reserved</p>
    <p style="margin-top:8px;">
        <a href="/about" style="color:var(--cyan); text-decoration:none;">About Us</a> | 
        <a href="/rules" style="color:var(--cyan); text-decoration:none;">Rules</a> |
        <a href="/terms" style="color:var(--cyan); text-decoration:none;">Terms</a> | 
        <a href="/privacy" style="color:var(--cyan); text-decoration:none;">Privacy</a>
    </p>
</div>

<!-- PAYMENT PAGE (premium features) -->
<div id="paymentPage" style="display:none; min-height:100vh; align-items:center; justify-content:center; padding:20px;">
    <div style="background:var(--card); border-radius:22px; padding:30px; max-width:450px; width:100%; text-align:center;">
        <span style="font-size:3em;">💰</span>
        <h2 style="color:var(--cyan); margin:10px 0;">Unlock Premium Features</h2>
        <ul style="text-align:left; margin:20px; color:var(--text2); line-height:1.8;">
            <li>✅ Full cluster point calculation (7 subjects)</li>
            <li>✅ Courses you qualify for with cutoff gaps</li>
            <li>✅ Universities you can join</li>
            <li>✅ Admission chances (qualified / close / not)</li>
            <li>✅ AI career recommendations</li>
            <li>✅ Scholarship finder (GPA + major)</li>
            <li>✅ Save your results & view history</li>
        </ul>
        <div class="pay-box">
            <p>M-PESA Till Number: <strong>123456</strong></p>
            <p>Amount: <strong>KES 100</strong></p>
        </div>
        <p style="font-size:.8em; color:var(--text2);">Enter your M-PESA phone number to receive STK Push</p>
        <input type="tel" id="payPhone" placeholder="07XX XXX XXX" style="width:100%; margin:10px 0;">
        
        <!-- Terms & Privacy checkbox -->
        <div style="margin:15px 0; text-align:left;">
            <label>
                <input type="checkbox" id="agreeTerms" required>
                I agree to the <a href="/terms" target="_blank" style="color:var(--cyan);">Terms & Conditions</a> and
                <a href="/privacy" target="_blank" style="color:var(--cyan);">Privacy Policy</a>
            </label>
        </div>
        
        <button class="btn btn-mpesa" onclick="processPayment()">📱 Pay with M-PESA</button>
        <div id="payStatus" style="margin-top:10px; font-size:.85em;"></div>
    </div>
</div>

<!-- MAIN APP (full features, hidden until payment) -->
<div class="container" id="app" style="display:none;">
    <div class="header">
        <div class="logo">🎓</div>
        <h1>EduPoint AI v10.0</h1>
        <p style="color:var(--text2);font-size:.8em;">Academic Helpdesk • KUCCPS Platform</p>
    </div>
    
    <!-- CALCULATOR -->
    <div class="card">
        <h3>📋 Enter Your 7 KCSE Subjects</h3>
        <div id="fields"></div>
        <button class="btn btn-calc" onclick="calc()" id="calcBtn" style="margin-top:10px;">⚡ Calculate My Cluster Points</button>
        <div class="spinner" id="spinner"><div class="spinner-icon">🔄</div><p>Calculating your results...</p></div>
    </div>
    
    <!-- RESULTS -->
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
    
    <!-- AI CAREER ADVISOR -->
    <div class="card">
        <h3>🧑‍💼 AI Career Advisor</h3>
        <p style="color:var(--text2);font-size:0.85em;margin-bottom:10px;">Select your interests to get personalised career guidance.</p>
        <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;">
            <button class="sort-btn" onclick="selectInterest('Medicine')">🏥 Medicine</button>
            <button class="sort-btn" onclick="selectInterest('Technology')">💻 Technology</button>
            <button class="sort-btn" onclick="selectInterest('Engineering')">⚙️ Engineering</button>
            <button class="sort-btn" onclick="selectInterest('Business')">💼 Business</button>
            <button class="sort-btn" onclick="selectInterest('Education')">📚 Education</button>
            <button class="sort-btn" onclick="selectInterest('Arts')">🎭 Arts</button>
        </div>
        <div id="careerResult"></div>
    </div>
    
    <!-- SCHOLARSHIP FINDER -->
    <div class="card">
        <h3>💰 Scholarship Finder</h3>
        <p style="color:var(--text2); font-size:0.85em;">Find scholarships that match your GPA and intended major</p>
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
            <input type="text" id="scholarMajor" placeholder="Your intended major (e.g., Computer Science)" style="flex:2;">
            <input type="number" id="scholarGpa" placeholder="Your GPA (0-4.0)" step="0.1" style="flex:1;">
        </div>
        <button class="btn btn-calc" onclick="searchScholarships()" style="background:linear-gradient(135deg, #ff8c00, #ff2e00);">🔍 Find Scholarships</button>
        <div id="scholarResults" style="margin-top:15px;"></div>
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
    
   <!-- CHATBOT CARD -->
<div class="card">
    <h3>💬 Ask EduBot (KUCCPS Assistant)</h3>
    <div id="chatMessages" style="height: 300px; overflow-y: auto; border: 1px solid var(--border); border-radius: 12px; padding: 10px; margin-bottom: 10px; background: rgba(0,0,0,0.2);">
        <div class="chat-message bot-message">👋 Hi! I'm EduBot. Ask me anything about KUCCPS – courses, cutoffs, requirements, transfers, or scholarships. Type a question or tap a quick button below.</div>
    </div>
    <div style="margin-bottom: 10px; display: flex; flex-wrap: wrap; gap: 5px;">
        <button class="sort-btn" onclick="quickQuestion('How are KUCCPS cluster points calculated?')">📐 Cluster Points</button>
        <button class="sort-btn" onclick="quickQuestion('Which courses can I qualify for with my grades?')">🎓 My Courses</button>
        <button class="sort-btn" onclick="quickQuestion('What is the cutoff for Computer Science?')">💻 CS Cutoff</button>
        <button class="sort-btn" onclick="quickQuestion('Can I do Nursing with a B-?')">🩺 Nursing B-</button>
        <button class="sort-btn" onclick="quickQuestion('Which courses are marketable in Kenya?')">💼 Marketable</button>
        <button class="sort-btn" onclick="quickQuestion('How do I apply for HELB?')">💰 HELB</button>
    </div>
    <div style="display: flex; gap: 10px;">
        <input type="text" id="chatInput" placeholder="Type your question here..." style="flex: 1;" onkeypress="if(event.key === 'Enter') sendChatMessage();">
        <button class="btn btn-calc" onclick="sendChatMessage()" style="width: auto; padding: 0 20px; margin: 0;">Send</button>
    </div>
</div>
    <!-- FOLLOW US -->
    <div class="card" style="text-align:center;">
        <h3>📢 Follow Us For More Information</h3>
        <p style="color:var(--text2);font-size:.85em;margin-bottom:12px;">Get KUCCPS updates, course tips & career guidance</p>
        <div class="social-row">
            <a href="https://chat.whatsapp.com/CQB9ZfYe9B683p6Df35YCG" target="_blank" class="si si-wa">💬</a>
            <a href="https://www.facebook.com/profile.php?id=61589138732515" target="_blank" class="si si-fb">📘</a>
            <a href="https://www.instagram.com/edupointkenya" target="_blank" class="si si-ig">📸</a>
            <a href="https://www.tiktok.com/@edupointkenya" target="_blank" class="si si-tt">🎵</a>
            <a href="mailto:academichelpdesk1@gmail.com" class="si si-em">✉️</a>
        </div>
        <p style="font-size:.75em;color:var(--text3);margin-top:10px;">
            📧 <b>Email:</b> academichelpdesk1@gmail.com<br>
            💬 <b>WhatsApp:</b> Join our community for instant updates
        </p>
    </div>
    
    <!-- FOUNDER -->
    <div class="founder-card">
        <div style="font-size:2.5em;">👨‍💻</div>
        <h3 style="color:var(--cyan);margin:8px 0;">Founder & CEO</h3>
        <h2 style="font-size:1.4em;">Mr. Nex</h2>
        <p style="color:var(--text2);">Full Stack Developer • AI Systems Engineer</p>
        <div class="contact-row">
            <a href="tel:0114812308" class="contact-btn" style="background:var(--card);border:1px solid var(--cyan);color:var(--cyan);">📞 Call</a>
            <a href="mailto:nexo27716@gmail.com" class="contact-btn" style="background:var(--card);border:1px solid var(--purple);color:var(--purple);">✉️ Email</a>
            <a href="https://wa.me/254114812308" target="_blank" class="contact-btn" style="background:var(--wa);color:#fff;">💬 WhatsApp</a>
        </div>
    </div>
    
    <div class="footer">
    <p>© 2026 <b>EduPoint AI v10.0</b> • All Rights Reserved</p>
    <p style="margin-top:8px;">
        <a href="/about" style="color:var(--cyan); text-decoration:none;">About Us</a> | 
        <a href="/rules" style="color:var(--cyan); text-decoration:none;">Rules</a> |
        <a href="/terms" style="color:var(--cyan); text-decoration:none;">Terms</a> | 
        <a href="/privacy" style="color:var(--cyan); text-decoration:none;">Privacy</a>
    </p>
</div>

<a href="https://chat.whatsapp.com/CQB9ZfYe9B683p6Df35YCG" target="_blank" class="wa-float">💬</a>
<div class="notif" id="notif"></div>

<script>
var S = ''' + json.dumps(S) + ''';
var G = ''' + json.dumps(G) + ''';
var pts = null, qd = [], st = null;
var previewGrades = {};

function buildPreview() {
    var h = '';
    for (var i = 0; i < 7; i++) {
        h += '<div class="subj-row"><select class="previewSubj" data-idx="'+i+'"><option value="">Subject '+(i+1)+'</option>';
        for (var j = 0; j < S.length; j++) { h += '<option value="'+S[j]+'">'+S[j]+'</option>'; }
        h += '</select><select class="previewGrade"><option value="">Grade</option>';
        for (var k = 0; k < G.length; k++) { h += '<option value="'+G[k]+'">'+G[k]+'</option>'; }
        h += '</select></div>';
    }
    document.getElementById('previewFields').innerHTML = h;
}

function previewCluster() {
    var subjSelects = document.querySelectorAll('.previewSubj');
    var gradeSelects = document.querySelectorAll('.previewGrade');
    var grades = {};
    for (var i = 0; i < 7; i++) {
        if (!subjSelects[i].value || !gradeSelects[i].value) {
            notify('Please fill all 7 subjects and grades', 'error');
            return;
        }
        grades[subjSelects[i].value] = gradeSelects[i].value;
    }
    previewGrades = grades;
    
    fetch('/api/calc', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({grades: grades})
    })
    .then(res => res.json())
    .then(data => {
        if (data.cp !== undefined) {
            document.getElementById('estPoints').innerText = data.cp.toFixed(3);
            document.getElementById('previewResult').style.display = 'block';
        } else {
            notify('Error calculating cluster points. Check subjects.', 'error');
        }
    })
    .catch(err => notify('Calculation failed. Try again.', 'error'));
}

function showPaymentPage() {
    document.getElementById('landingPage').style.display = 'none';
    document.getElementById('paymentPage').style.display = 'flex';
}

function processPayment() {
    var phone = document.getElementById('payPhone').value;
    var agreeCheckbox = document.getElementById('agreeTerms');
    
    if (!phone) { alert("Enter M-PESA phone number"); return; }
    if (!agreeCheckbox || !agreeCheckbox.checked) { alert("Agree to Terms & Privacy"); return; }
    
    document.getElementById('payStatus').innerHTML = '⏳ Sending STK Push...';
    
    setTimeout(function() {
        document.getElementById('payStatus').innerHTML = '<span style="color:var(--green);">✅ Payment successful! Redirecting...</span>';
        setTimeout(function() {
            // Switch to main app
            document.getElementById('paymentPage').style.display = 'none';
            document.getElementById('app').style.display = 'block';
            
            // Build the subject fields
            if (typeof build === 'function') {
                build();
                console.log("build() executed");
            } else {
                console.error("build() missing – creating fields manually");
                var fieldsDiv = document.getElementById('fields');
                if (fieldsDiv) {
                    var html = '';
                    for (var i = 0; i < 7; i++) {
                        html += '<div class="subj-row"><select class="ss"><option value="">Subject '+(i+1)+'</option>';
                        for (var j = 0; j < S.length; j++) html += '<option value="'+S[j]+'">'+S[j]+'</option>';
                        html += '</select><select class="gs"><option value="">Grade</option>';
                        for (var k = 0; k < G.length; k++) html += '<option value="'+G[k]+'">'+G[k]+'</option>';
                        html += '</select></div>';
                    }
                    fieldsDiv.innerHTML = html;
                }
            }
            
            // Optional: auto‑fill from preview grades if any
            if (typeof previewGrades !== 'undefined' && previewGrades && Object.keys(previewGrades).length > 0) {
                var mainSubj = document.querySelectorAll('#fields .ss');
                var mainGrade = document.querySelectorAll('#fields .gs');
                for (var i = 0; i < mainSubj.length; i++) {
                    var subj = mainSubj[i].value;
                    if (previewGrades[subj] && mainGrade[i]) {
                        mainGrade[i].value = previewGrades[subj];
                    }
                }
                if (typeof calc === 'function') setTimeout(calc, 300);
            }
            
            if (typeof notify === 'function') notify('✅ Welcome!', 'success');
        }, 1500);
    }, 2000);
}

function calc() {
    var ss = document.querySelectorAll('.ss'), gs = document.querySelectorAll('.gs');
    var gr = {};
    for (var i = 0; i < 7; i++) {
        if (!ss[i].value || !gs[i].value) { notify('Fill all 7 subjects', 'error'); return; }
        gr[ss[i].value] = gs[i].value;
    }
    document.getElementById('calcBtn').disabled = true;
    document.getElementById('spinner').classList.add('show');
    fetch('/api/calc', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({grades: gr})
    })
    .then(r => r.json())
    .then(d => {
        pts = d.cp; qd = d.ac; st = d.st;
        showR(d); showQ(d); showAI();
        document.getElementById('calcBtn').disabled = false;
        document.getElementById('spinner').classList.remove('show');
        document.getElementById('referCard').style.display = 'block';
        notify('✅ Points: '+pts.toFixed(3), 'success');
    });
}

function showR(d) {
    var h = '<div class="result-box"><div class="pts-big">'+pts.toFixed(3)+'</div><p>Your Cluster Points</p></div>';
    if (d.q.length) {
        h += '<div class="sec-green">✅ '+d.q.length+' Courses You Qualify For</div><div class="overflow-x"><table><tr><th>Course</th><th>University</th><th>Cutoff</th><th>Gap</th></tr>';
        for (var i=0;i<Math.min(d.q.length,10);i++) {
            var c = d.q[i];
            h += '<tr><td>'+c.i+' '+c.n+'</td><td>'+c.u+'</td><td>'+c.c.toFixed(3)+'</td><td style="color:var(--green);">+'+c.g.toFixed(1)+'</td></tr>';
        }
        h += '</table></div>';
    }
    if (d.cl.length) {
        h += '<div class="sec-yellow">⚠️ '+d.cl.length+' Close Matches</div><div class="overflow-x"><table><tr><th>Course</th><th>University</th><th>Cutoff</th><th>Gap</th></tr>';
        for (var i=0;i<Math.min(d.cl.length,5);i++) {
            var c = d.cl[i];
            h += '<tr><td>'+c.i+' '+c.n+'</td><td>'+c.u+'</td><td>'+c.c.toFixed(3)+'</td><td style="color:var(--yellow);">'+c.g.toFixed(1)+'</td></tr>';
        }
        h += '</table></div>';
    }
    document.getElementById('results').innerHTML = h;
}

function showQ(d) {
    document.getElementById('qSection').style.display = 'block';
    document.getElementById('totalPts').textContent = pts.toFixed(3);
    document.getElementById('qCount').textContent = st.qc;
    document.getElementById('cCount').textContent = st.cc;
    document.getElementById('nCount').textContent = st.nc;
    document.getElementById('sRate').textContent = st.r + '%';
    renderT(qd);
}

function renderT(cs) {
    var h = '<table><tr><th>#</th><th>Course</th><th>University</th><th>Cutoff</th><th>Gap</th><th>Status</th></tr>';
    for (var i=0;i<cs.length;i++) {
        var c = cs[i], g = c.g;
        var sc = g>=0?'bg-green':(g>=-2?'bg-yellow':'bg-red');
        var sts = g>=0?'✅ Qualified':(g>=-2?'⚠️ Close':'❌ Not');
        var color = g>=0?'var(--green)':(g>=-2?'var(--yellow)':'var(--red)');
        h += '<tr><td>'+(i+1)+'</td><td>'+c.i+' '+c.n+'</td><td>'+c.u+'</td><td>'+c.c.toFixed(3)+'</td><td style="color:'+color+';font-weight:700;">'+(g>=0?'+':'')+g.toFixed(1)+'</td><td><span class="badge '+sc+'">'+sts+'</span></td></tr>';
    }
    h += '</table>';
    document.getElementById('qTable').innerHTML = h;
}

function filterQ() {
    var q = document.getElementById('qSearch').value.toLowerCase().trim();
    if (!q) { renderT(qd); return; }
    var f = [];
    for (var i=0;i<qd.length;i++) {
        if (qd[i].n.toLowerCase().includes(q) || qd[i].u.toLowerCase().includes(q)) f.push(qd[i]);
    }
    renderT(f);
}

function showAI() {
    fetch('/api/ai', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({cp: pts})
    })
    .then(r => r.json())
    .then(d => {
        var html = '<div class="ai-card"><div class="ai-badge">🤖 '+d.l+'</div><p style="font-size:1.05em;">'+d.a+'</p><p style="margin-top:8px;">🔥 '+d.p.join(' • ')+'</p></div>';
        document.getElementById('ai').innerHTML = html;
    });
}

function selectInterest(interest) {
    var messages = {
        'Medicine': '🎓 Recommended courses: Medicine & Surgery, Nursing, Pharmacy, Clinical Medicine. High demand in Kenya.',
        'Technology': '💻 Recommended: Computer Science, IT, Software Engineering. Strong job market with high earning potential.',
        'Engineering': '⚙️ Recommended: Civil, Electrical, Mechanical, Mechatronic Engineering. Great career prospects.',
        'Business': '💼 Recommended: Commerce, Economics, Actuarial Science, Business Management. Versatile career options.',
        'Education': '📚 Recommended: Education (Science/Arts), Early Childhood. Stable career in teaching.',
        'Arts': '🎭 Recommended: BA, Journalism, Communication. Explore creative and social fields.'
    };
    document.getElementById('careerResult').innerHTML = '<div class="sec-green">✨ ' + messages[interest] + '</div>';
}

function searchScholarships() {
    var major = document.getElementById('scholarMajor').value;
    var gpa = parseFloat(document.getElementById('scholarGpa').value);
    if (isNaN(gpa)) {
        notify("Please enter a valid GPA (e.g., 3.2)", "error");
        return;
    }
    var resultsDiv = document.getElementById('scholarResults');
    resultsDiv.innerHTML = '<div class="spinner show"><div class="spinner-icon">🔄</div><p>Searching scholarships...</p></div>';
    fetch('/api/scholarships', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({major: major, gpa: gpa})
    })
    .then(res => res.json())
    .then(data => {
        if (data.length === 0) {
            resultsDiv.innerHTML = '<div class="sec-yellow">😞 No scholarships match your criteria. Try a lower GPA or broader major.</div>';
            return;
        }
        var html = '<div class="sec-green">✅ ' + data.length + ' scholarships found</div>';
        html += '<div class="overflow-x"><table><tr><th>Scholarship</th><th>Amount</th><th>Min GPA</th><th>Eligibility</th><th>Deadline</th><th>Link</th></tr>';
        data.forEach(s => {
            html += `<tr><td><strong>${s.name}</strong></td><td>${s.amount}</td><td>${s.min_gpa}</td><td>${s.income_req || s.major}</td><td>${s.deadline}</td><td><a href="${s.link}" target="_blank" style="color:var(--cyan);">Apply</a></td></tr>`;
        });
        html += '</table></div>';
        resultsDiv.innerHTML = html;
    })
    .catch(err => {
        resultsDiv.innerHTML = '<div class="sec-yellow">⚠️ Error loading scholarships. Try again.</div>';
        console.error(err);
    });
}

function copyRef() {
    navigator.clipboard.writeText('https://edupoint.app/ref=SHARE');
    notify('📋 Referral link copied! Share with friends.', 'success');
}

// Chatbot functions
function sendChatMessage() {
    let input = document.getElementById('chatInput');
    let message = input.value.trim();
    if (!message) return;
    
    let chatDiv = document.getElementById('chatMessages');
    // User message
    let userDiv = document.createElement('div');
    userDiv.className = 'chat-message user-message';
    userDiv.innerText = message;
    chatDiv.appendChild(userDiv);
    input.value = '';
    chatDiv.scrollTop = chatDiv.scrollHeight;
    
    // Typing indicator
    let typing = document.createElement('div');
    typing.className = 'chat-message bot-message';
    typing.innerText = 'EduBot is thinking...';
    typing.id = 'typingIndicator';
    chatDiv.appendChild(typing);
    chatDiv.scrollTop = chatDiv.scrollHeight;
    
    fetch('/api/chatbot', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('typingIndicator')?.remove();
        let botDiv = document.createElement('div');
        botDiv.className = 'chat-message bot-message';
        botDiv.innerText = data.response;
        chatDiv.appendChild(botDiv);
        chatDiv.scrollTop = chatDiv.scrollHeight;
    })
    .catch(err => {
        document.getElementById('typingIndicator')?.remove();
        let errDiv = document.createElement('div');
        errDiv.className = 'chat-message bot-message';
        errDiv.innerText = "Sorry, I'm having trouble. Please try again.";
        chatDiv.appendChild(errDiv);
        chatDiv.scrollTop = chatDiv.scrollHeight;
    });
}

function quickQuestion(question) {
    document.getElementById('chatInput').value = question;
    sendChatMessage();
}

function notify(m, t) {
    var n = document.getElementById('notif');
    n.className = 'notif notif-' + t;
    n.textContent = m;
    n.style.display = 'block';
    setTimeout(function() { n.style.display = 'none'; }, 4000);
}

// Initialize
buildPreview();
</script>
</body>
</html>'''

import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
