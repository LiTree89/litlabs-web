# ⚡ GLAMFLOW AI - QUICK START (15 MINUTES)

## What You Need Ready
- Firebase project: `studio-4627045237-a2fe9` ✅ (already created)
- 5 minutes to collect credentials
- Browser tabs for 3 consoles

---

## 🚀 STEP-BY-STEP (Do This Now)

### 1️⃣ GET FIREBASE KEYS (2 minutes)

Open: https://console.firebase.google.com/project/studio-4627045237-a2fe9/settings/general

Look for "Your apps" → "Web" config:
```javascript
{
  apiKey: "AIzaSy...",           // COPY THIS
  appId: "1:612847421952:web:..." // COPY THIS
}
```

**Where to paste them:**
Open file: `C:\Users\dying\public\firebase-config.js`

Replace these lines:
```javascript
apiKey: "AIzaSyD-placeholder-get-from-firebase-console",  // PASTE API KEY HERE
appId: "1:612847421952:web:your-app-id-here"            // PASTE APP ID HERE
```

Save the file.

---

### 2️⃣ ENABLE FIREBASE AUTH (1 minute)

Open: https://console.firebase.google.com/project/studio-4627045237-a2fe9/authentication/providers

**Enable Email/Password:**
- Click "Email/Password"
- Toggle ON
- Click Save

**Enable Google:**
- Click "Google"
- Toggle ON
- Need Google Client ID (see next step)
- Click Save

---

### 3️⃣ GET GOOGLE CLIENT ID (3 minutes)

Open: https://console.cloud.google.com/apis/credentials

**If you see credentials list:**
- Look for "Web application" type
- Copy the Client ID (ends with `.apps.googleusercontent.com`)

**If you don't see anything:**
- Click "Create Credentials" → "OAuth 2.0 Client ID"
- Choose "Web application"
- In "Authorized JavaScript origins" add:
  - `https://studio-4627045237-a2fe9.web.app`
  - `https://studio-4627045237-a2fe9.firebaseapp.com`
- In "Authorized redirect URIs" add:
  - `https://studio-4627045237-a2fe9.web.app/__/auth/handler`
  - `https://studio-4627045237-a2fe9.firebaseapp.com/__/auth/handler`
- Click Create
- Copy the Client ID

Back in Firebase Console (previous tab):
- Paste Client ID in Google sign-in settings
- Click Save

---

### 4️⃣ CREATE FIRESTORE DATABASE (2 minutes)

Open: https://console.firebase.google.com/project/studio-4627045237-a2fe9/firestore/databases

- Click "Create Database"
- Choose "Start in test mode"
- Select region: `us-central1`
- Click "Enable"

When it's created, click "Rules" tab and paste:

```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    match /transactions/{document=**} {
      allow read: if request.auth.uid == resource.data.userId;
      allow write: if false;
    }
    match /subscriptions/{document=**} {
      allow read: if request.auth.uid == resource.data.userId;
      allow write: if false;
    }
  }
}
```

Click "Publish"

---

### 5️⃣ GET STRIPE KEYS (3 minutes)

Open: https://stripe.com (create account if needed)

**Get API Keys:**
- Go to Dashboard → Developers → API keys
- Copy **Publishable Key** (starts with `pk_test_`)
- Copy **Secret Key** (starts with `sk_test_`) - SAVE FOR LATER

**Create Products:**
1. Go to Dashboard → Products
2. Click "Create product"
   - Name: `Pro Plan`
   - Price: `$29.00`
   - Billing period: `Monthly`
   - Click Create
   - **Copy the Price ID** (looks like `price_1ABC...XYZ`)

3. Click "Create product" again
   - Name: `Enterprise Plan`
   - Price: `Custom`
   - Billing period: `Monthly`
   - Click Create
   - **Copy the Price ID**

---

### 6️⃣ UPDATE STRIPE CONFIG (1 minute)

Open file: `C:\Users\dying\public\stripe-config.js`

Replace these lines:
```javascript
publishableKey: 'pk_test_YOUR_PUBLISHABLE_KEY_HERE',     // PASTE YOUR KEY
priceIds: {
    pro: 'price_YOUR_PRO_PRICE_ID_HERE',                 // PASTE PRICE ID
    enterprise: 'price_YOUR_ENTERPRISE_PRICE_ID_HERE'    // PASTE PRICE ID
}
```

Save the file.

---

### 7️⃣ COMMIT & DEPLOY (1 minute)

Open terminal and run:

```bash
cd C:\Users\dying
git add public/firebase-config.js public/stripe-config.js
git commit -m "config: update Firebase and Stripe credentials"
git push origin main
```

GitHub Actions will auto-deploy to Firebase! 🚀

---

## 🧪 TEST IT (5 minutes)

### Test Auth Page:
1. Open: https://studio-4627045237-a2fe9.web.app/auth.html
2. Try email signup:
   - Enter email: `test@example.com`
   - Enter password: `Test123!`
   - Click "Sign up"
   - You should see success message
3. Check Firestore:
   - Go to Firebase Console → Firestore
   - You should see user created in `users` collection
4. Try Google OAuth:
   - Go back to auth page
   - Click "Sign in with Google"
   - Should work now!

### Test Dashboard:
1. Open: https://studio-4627045237-a2fe9.web.app/dashboard.html
2. Should show your user data from Firestore
3. See the pricing tiers
4. Stats card should show your plan

---

## 💰 TEST STRIPE PAYMENT

1. From dashboard, click "Upgrade to Pro"
2. Stripe checkout opens
3. Use test card: `4242 4242 4242 4242`
4. Any future expiry date
5. Any 3 digits for CVC
6. Click "Pay"
7. Should redirect back to dashboard
8. Dashboard should show "Pro" plan now
9. Check Firestore → your user doc should show `subscription: "pro"`

---

## ✅ You're Done! 

If all tests pass:
- ✅ Authentication works (Email + Google)
- ✅ Firestore database working
- ✅ Dashboard displays user data
- ✅ Stripe payments working
- ✅ Subscriptions updating in database

## 🎉 You Have a Working SaaS Platform!

Users can now:
1. Sign up
2. View their dashboard
3. Upgrade to Pro
4. Pay with Stripe
5. Access their subscription tier

---

## 🆘 Stuck?

**Issue: "Firebase is not defined"**
- Check: firebase-config.js is loaded before auth.js
- In browser DevTools (F12), check Console for errors

**Issue: "Email signup not working"**
- Check: Email/Password is enabled in Firebase Authentication
- Check: Firestore database exists and rules are set

**Issue: "Google OAuth not working"**
- Check: Google Client ID is correct in Firebase Console
- Check: Authorized origins/redirect URIs are exactly correct

**Issue: "Stripe button not showing"**
- Check: Publishable key is added to stripe-config.js
- Check: Price IDs are correct

**Issue: "Payment not processing"**
- Check: Stripe Secret Key will be deployed next
- First test with credentials above

---

## 📱 Share Your Site!

Your site is live at:
**https://studio-4627045237-a2fe9.web.app**

Share this link with beta testers! ✨

---

## 🚀 Next Level: Cloud Functions for Payments

After testing works, deploy payment Cloud Functions:

```bash
firebase functions:config:set stripe.secret_key="sk_test_YOUR_SECRET_KEY"
firebase deploy --only functions
```

Then full payments will work end-to-end!

---

**15 minutes → Full SaaS Platform Live!** 🎯
