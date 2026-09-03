import os,sqlite3,re,requests
from datetime import datetime

ALLOWED={"airtel","tkash"}
def normalize_phone(phone):
    p=re.sub(r"\D","",str(phone or ""))
    if p.startswith("254") and len(p)==12:return p
    if p.startswith("0") and len(p)==10:return "254"+p[1:]
    if len(p)==9 and p.startswith("7"):return "254"+p
    return None
def validate_provider(p):return p in ALLOWED

class PaymentService:
    def __init__(self,db_path):self.db_path=db_path;self.init_db()
    def conn(self):c=sqlite3.connect(self.db_path);c.row_factory=sqlite3.Row;return c
    def init_db(self):
        with self.conn() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS payments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,transaction_id TEXT UNIQUE NOT NULL,user_id INTEGER,
            provider_reference TEXT,phone TEXT NOT NULL,network TEXT NOT NULL,amount REAL NOT NULL,
            plan TEXT NOT NULL,status TEXT NOT NULL,message TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)""")
            cols=[r["name"] for r in db.execute("PRAGMA table_info(payments)").fetchall()]
            if "user_id" not in cols:db.execute("ALTER TABLE payments ADD COLUMN user_id INTEGER")
            db.commit()
    def create_pending(self,**kw):
        now=datetime.utcnow().isoformat()
        with self.conn() as db:
            db.execute("""INSERT INTO payments(transaction_id,user_id,phone,network,amount,plan,status,message,created_at,updated_at)
            VALUES(?,?,?,?,?,?, 'pending',?,?,?)""",(kw["transaction_id"],kw.get("user_id"),kw["phone"],kw["network"],kw["amount"],kw["plan"],"Waiting for payment",now,now));db.commit()
    def update(self,tx,status=None,provider_reference=None,message=None):
        fields=[];vals=[]
        if status is not None:fields+=["status=?"];vals+=[status]
        if provider_reference is not None:fields+=["provider_reference=?"];vals+=[provider_reference]
        if message is not None:fields+=["message=?"];vals+=[message]
        fields+=["updated_at=?"];vals+=[datetime.utcnow().isoformat(),tx]
        with self.conn() as db:db.execute("UPDATE payments SET "+",".join(fields)+" WHERE transaction_id=?",vals);db.commit()
    def get(self,tx):
        with self.conn() as db:
            r=db.execute("SELECT * FROM payments WHERE transaction_id=?",(tx,)).fetchone()
        return dict(r) if r else None
    def available_providers(self):
        return [{"id":"airtel","name":"Airtel Money","description":"Pay using an Airtel Money number."},{"id":"tkash","name":"T-Kash","description":"Pay using T-Kash."}]
    def initiate(self,provider,phone,amount,transaction_id,plan):
        if provider=="airtel":return self.airtel_collection(phone,amount,transaction_id)
        if provider=="tkash":return self.tkash_collection(phone,amount,transaction_id,plan)
        raise ValueError("Unsupported provider")
    def airtel_collection(self,phone,amount,tx):
        base=os.getenv("AIRTEL_BASE_URL","https://openapi.airtel.africa")
        token_url=os.getenv("AIRTEL_TOKEN_URL",base.rstrip("/")+"/auth/oauth2/token")
        pay_url=os.getenv("AIRTEL_PAYMENT_URL",base.rstrip("/")+"/merchant/v1/payments/")
        cid=os.getenv("AIRTEL_CLIENT_ID");secret=os.getenv("AIRTEL_CLIENT_SECRET")
        country=os.getenv("AIRTEL_COUNTRY","KE");currency=os.getenv("AIRTEL_CURRENCY","KES")
        if not cid or not secret:raise RuntimeError("Airtel API credentials are not configured.")
        tr=requests.post(token_url,json={"client_id":cid,"client_secret":secret,"grant_type":"client_credentials"},headers={"Content-Type":"application/json"},timeout=30)
        tr.raise_for_status();token=tr.json().get("access_token")
        if not token:raise RuntimeError("Airtel API did not return an access token.")
        payload={"reference":tx,"subscriber":{"country":country,"currency":currency,"msisdn":phone[-9:]},
                 "transaction":{"amount":amount,"country":country,"currency":currency,"id":tx}}
        r=requests.post(pay_url,json=payload,headers={"Authorization":"Bearer "+token,"Content-Type":"application/json","Accept":"application/json","X-Country":country,"X-Currency":currency},timeout=30)
        if not r.ok:raise RuntimeError(f"Airtel API error {r.status_code}: {r.text[:300]}")
        b=r.json()
        return {"status":"pending","provider_reference":b.get("data",{}).get("transaction",{}).get("id") or tx,
                "message":"Airtel Money payment request sent. Complete the payment on the customer's phone.",
                "instructions":["Check the Airtel Money prompt on the customer's phone.","Wait for payment confirmation."]}
    def tkash_collection(self,phone,amount,tx,plan):
        endpoint=os.getenv("TKASH_COLLECTION_URL");key=os.getenv("TKASH_API_KEY");merchant=os.getenv("TKASH_MERCHANT_ID")
        if not endpoint or not key or not merchant:
            return {"status":"pending_manual","provider_reference":tx,
                    "message":"T-Kash is enabled. Configure the official T-Kash business API endpoint and credentials for automatic collection.",
                    "instructions":["Use your official T-Kash Paybill/Till.","Use transaction reference: "+tx]}
        payload={"merchant_id":merchant,"reference":tx,"amount":amount,"phone":phone,"currency":"KES","plan":plan,
                 "callback_url":os.getenv("PUBLIC_BASE_URL","").rstrip("/")+"/api/payment/webhook/tkash"}
        r=requests.post(endpoint,json=payload,headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},timeout=30)
        if not r.ok:raise RuntimeError(f"T-Kash API error {r.status_code}: {r.text[:300]}")
        b=r.json()
        return {"status":"pending","provider_reference":b.get("transaction_id") or b.get("reference") or tx,
                "message":"T-Kash payment request created.","instructions":["Complete the T-Kash payment.","Wait for server confirmation."]}
    def check_status(self,row):return None
    def handle_webhook(self,provider,payload):
        tx=payload.get("transaction_id") or payload.get("transactionId") or payload.get("reference") or payload.get("external_reference")
        status=str(payload.get("status") or payload.get("transaction_status") or payload.get("state") or "").lower()
        if not tx:return {"ok":False,"error":"Missing transaction reference."}
        success={"success","successful","completed","paid","successful_payment"};fail={"failed","failure","cancelled","canceled","reversed"}
        final="paid" if status in success else ("failed" if status in fail else "pending")
        pref=payload.get("provider_reference") or payload.get("receipt") or payload.get("transaction_id")
        self.update(tx,status=final,provider_reference=pref,message=f"{provider} callback: {status or 'pending'}")
        return {"ok":True,"transaction_id":tx,"status":final}
