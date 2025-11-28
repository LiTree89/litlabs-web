# 🔧 GLAMFLOW AI - CONFIGURATION CHECKLIST

## ✅ STEP 1: Get Firebase Credentials

**Location**: https://console.firebase.google.com/project/studio-4627045237-a2fe9/settings/general

1. Open the link above (log in if needed)
2. Scroll down to "Your apps" section
3. Find "Web" app (or click "Add app" if missing)
4. You should see a config object that looks like:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "studio-4627045237-a2fe9.firebaseapp.com",
  projectId: "studio-4627045237-a2fe9",
  storageBucket: "studio-4627045237-a2fe9.appspot.com",
  messagingSenderId: "612847421952",
  appId: "1:612847421952:web:..."
};
```

**Copy these exact values:**
- [ ] `apiKey` - looks like "AIzaSy..." (long string)
- [ ] `appId` - looks like "1:612847421952:web:..." (keep the full value)

---

## ✅ STEP 2: Enable Firebase Authentication Methods

**Location**: https://console.firebase.google.com/project/studio-4627045237-a2fe9/authentication/providers

1. Click "Sign-in method" tab
2. Enable these sign-in providers:
   - [ ] **Email/Password** - Click, toggle ON, Save
   - [ ] **Google** - Click, toggle ON, add your OAuth client ID, Save

### For Google OAuth:

**In Firebase Console:**
1. Click on "Google" sign-in method
2. You need a Google OAuth 2.0 Client ID
3. Click the link to Google Cloud Console (it'll open in new tab)

**In Google Cloud Console** (https://console.cloud.google.com):
1. Select project (should auto-select your Firebase project)
2. Go to "APIs & Services" → "Credentials"
3. Create "OAuth 2.0 Client ID" (Web application type):
   - **Authorized JavaScript origins:**
     - `https://studio-4627045237-a2fe9.web.app`
     - `https://studio-4627045237-a2fe9.firebaseapp.com`
   - **Authorized redirect URIs:**
     - `https://studio-4627045237-a2fe9.web.app/__/auth/handler`
     - `https://studio-4627045237-a2fe9.firebaseapp.com/__/auth/handler`
4. Copy the **Client ID** (looks like: `...apps.googleusercontent.com`)
5. Go back to Firebase Console and paste it
6. Save

---

## ✅ STEP 3: Setup Firestore Database

**Location**: https://console.firebase.google.com/project/studio-4627045237-a2fe9/firestore

1. Click "Create database"
2. Choose "Start in test mode" (for development)
3. Select region (us-central1 is fine)
4. Click "Enable"

**Set Security Rules:**
1. Click the "Rules" tab
2. Replace the default with:

```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own document
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    
    // Transactions - only readable by owner, written by functions
    match /transactions/{document=**} {
      allow read: if request.auth.uid == resource.data.userId;
      allow write: if false;
    }
    
    // Subscriptions - similar to transactions
    match /subscriptions/{document=**} {
      allow read: if request.auth.uid == resource.data.userId;
      allow write: if false;
    }
  }
}
```

3. Click "Publish"

---

## ✅ STEP 4: Create Stripe Account & Get Keys

**Location**: https://stripe.com

1. Sign up for Stripe account
2. Go to Dashboard
3. Go to "Developers" → "API keys"
4. You'll see:
   - **Publishable key** (starts with `pk_test_` or `pk_live_`)
   - **Secret key** (starts with `sk_test_` or `sk_live_`)

**Copy:**
- [ ] Publishable Key (safe to show publicly)
- [ ] Secret Key (KEEP PRIVATE - never put in frontend)

---

## ✅ STEP 5: Create Stripe Products & Price IDs

**Location**: https://dashboard.stripe.com/products

1. Click "Create product"
2. Create 2 products:

### Product 1: PRO
- Name: `Pro Plan`
- Price: `$29/month`
- Recurring: Monthly
- **Copy the Price ID** (looks like: `price_1ABC...XYZ`)

### Product 2: ENTERPRISE
- Name: `Enterprise Plan`
- Price: `Custom` (don't set a fixed amount)
- Recurring: Monthly
- **Copy the Price ID** (looks like: `price_1ABC...ZYX`)

---

## ✅ STEP 6: Update Firebase Config Files

Once you have all the values, update these files in your project:

### File 1: `public/firebase-config.js`

Replace with your actual values:
```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",                    // From Firebase Console
    authDomain: "studio-4627045237-a2fe9.firebaseapp.com",
    projectId: "studio-4627045237-a2fe9",
    storageBucket: "studio-4627045237-a2fe9.appspot.com",
    messagingSenderId: "612847421952",
    appId: "YOUR_APP_ID_HERE"                       // From Firebase Console
};
```

### File 2: `public/stripe-config.js`

Replace with your Stripe keys:
```javascript
const STRIPE_CONFIG = {
    publishableKey: 'pk_test_YOUR_PUBLISHABLE_KEY_HERE',  // Your Stripe publishable key
    
    priceIds: {
        pro: 'price_YOUR_PRO_PRICE_ID_HERE',              // From Stripe Dashboard
        enterprise: 'price_YOUR_ENTERPRISE_PRICE_ID_HERE' // From Stripe Dashboard
    }
};
```

---

## ✅ STEP 7: Deploy Cloud Functions

Once you have Stripe keys, deploy the payment processing functions:

```bash
cd C:\Users\dying

# Set Stripe secret key
firebase functions:config:set stripe.secret_key="sk_test_YOUR_SECRET_KEY"

# Deploy functions
firebase deploy --only functions
```

---

## ✅ STEP 8: Setup Stripe Webhook

Once Cloud Functions are deployed:

1. Go to Stripe Dashboard → "Developers" → "Webhooks"
2. Click "Add endpoint"
3. **Endpoint URL:** 
   - Get from Firebase Console → Functions → stripeWebhook
   - Should look like: `https://REGION-PROJECT_ID.cloudfunctions.net/stripeWebhook`
4. **Events to listen to:**
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`
5. Copy the **Webhook Signing Secret** (starts with `whsec_`)
6. Add to Firebase:
```bash
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_SECRET"
firebase deploy --only functions
```

---

## 📝 SUMMARY: What You Need to Gather

| Item | Where to Find | Example Format |
|------|---------------|---|
| Firebase API Key | Firebase Console → Settings | `AIzaSy...` |
| Firebase App ID | Firebase Console → Settings | `1:612847421952:web:...` |
| Google OAuth Client ID | Google Cloud Console → APIs & Services | `...apps.googleusercontent.com` |
| Stripe Publishable Key | Stripe Dashboard → Developers → API Keys | `pk_test_...` |
| Stripe Secret Key | Stripe Dashboard → Developers → API Keys | `sk_test_...` |
| Stripe Pro Price ID | Stripe Dashboard → Products | `price_1ABC...XYZ` |
| Stripe Enterprise Price ID | Stripe Dashboard → Products | `price_1ABC...ZYX` |
| Stripe Webhook Secret | Stripe Dashboard → Webhooks | `whsec_...` |

---

## 🚀 Testing After Configuration

1. **Test Auth:**
   - Go to: https://studio-4627045237-a2fe9.web.app/auth.html
   - Try signing up with email
   - Try signing in with Google
   - Check Firestore to see user created

2. **Test Dashboard:**
   - After login, go to: https://studio-4627045237-a2fe9.web.app/dashboard.html
   - Should show your user info from Firestore

3. **Test Payments:**
   - Click "Upgrade to Pro"
   - Use Stripe test card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits
   - Check Firestore to see subscription updated

---

## 🆘 Need Help?

If you get stuck:
1. Check console errors: Open browser DevTools (F12) → Console tab
2. Check Firebase logs: `firebase functions:log`
3. Check Stripe webhook events: Stripe Dashboard → Webhooks → View events

---

**Next step: Start gathering the credentials from the console links above!** ✨
