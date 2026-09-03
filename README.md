# EduPoint AI v10.0 — Accounts, Admin and Multi-Network Payments

The public first page remains at `/`. Shared referral links such as `/ref/SHARE` and `/ref?ref=SHARE` return to the same first page and store the referral code for registration.

Student flow:
**First page → Create Account → Login/session → Dashboard → Choose plan → Airtel Money or T-Kash → provider confirmation → protected tools unlocked.**

Admin flow:
**Login page → Admin login → `/admin` → manage student accounts and payment records.**

M-PESA is not included.

Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in the hosting environment. Never place API secrets in HTML/JavaScript.

Run:
```bash
pip install -r requirements.txt
python app.py
```
