# GLAMFLOW AI - Architecture & Configuration Flow

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  index.html      │  │  auth.html       │  │ dashboard.html
│  │  (Landing Page)  │  │  (Sign In/Up)    │  │ (Dashboard)  │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘  │
│           │                     │                    │          │
│           └─────────────────────┼────────────────────┘          │
│                                 │                               │
│                    ┌────────────┴────────────┐                 │
│                    │  Firebase SDK          │                 │
│                    │  (Auth + Firestore)    │                 │
│                    └────────────┬────────────┘                 │
│                                 │                               │
└─────────────────────────────────┼───────────────────────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
        ┌───────────▼──────────┐    ┌───────────▼──────────┐
        │                      │    │                      │
        │  FIREBASE BACKEND    │    │   STRIPE PAYMENT     │
        │  (Cloud Services)    │    │   PROCESSOR          │
        │                      │    │                      │
        │ ┌──────────────────┐ │    │ ┌──────────────────┐ │
        │ │ Authentication   │ │    │ │ Checkout Session │ │
        │ │ (Email + Google) │ │    │ │ Creation         │ │
        │ └──────────────────┘ │    │ └──────────────────┘ │
        │ ┌──────────────────┐ │    │ ┌──────────────────┐ │
        │ │ Firestore DB     │ │    │ │ Payment          │ │
        │ │ (Users, Subs)    │ │    │ │ Processing       │ │
        │ └──────────────────┘ │    │ └──────────────────┘ │
        │ ┌──────────────────┐ │    │ ┌──────────────────┐ │
        │ │ Cloud Functions  │ │    │ │ Webhook Handler  │ │
        │ │ (Payment Logic)  │ │    │ │ (Update Status)  │ │
        │ └──────────────────┘ │    │ └──────────────────┘ │
        │                      │    │                      │
        └──────────────────────┘    └──────────────────────┘
```

---

## 🔧 Configuration Requirements

### 1️⃣ Firebase Setup (Required for Auth + Database)

```
┌─────────────────────────────────────────┐
│     FIREBASE CONSOLE                    │
│     (console.firebase.google.com)       │
├─────────────────────────────────────────┤
│                                         │
│  Project: studio-4627045237-a2fe9      │
│                                         │
│  ✅ Settings → Get Config Keys         │
│     • apiKey                            │
│     • appId                             │
│                                         │
│  ✅ Authentication → Enable Providers   │
│     • Email/Password                    │
│     • Google OAuth                      │
│                                         │
│  ✅ Firestore → Create Database         │
│     • Add Security Rules                │
│                                         │
│  ✅ Cloud Functions → Deploy            │
│     • Stripe integration code           │
│                                         │
└─────────────────────────────────────────┘
         ⬇
   Firebase SDK in Browser
   (firebase-config.js)
```

### 2️⃣ Google OAuth Setup (For Google Sign-In)

```
┌──────────────────────────────────────┐
│  GOOGLE CLOUD CONSOLE                │
│  (console.cloud.google.com)          │
├──────────────────────────────────────┤
│                                      │
│  Create OAuth 2.0 Client ID:         │
│  • Type: Web Application             │
│  • Authorized Origins:               │
│    - https://studio-4627045237...    │
│  • Authorized Redirects:             │
│    - __/auth/handler paths           │
│                                      │
│  Copy: Client ID                     │
│    ⬇                                 │
│  Add to Firebase Console             │
│    ⬇                                 │
│  auth.html uses it                   │
│                                      │
└──────────────────────────────────────┘
```

### 3️⃣ Stripe Setup (For Payments)

```
┌────────────────────────────────────────┐
│  STRIPE DASHBOARD                      │
│  (dashboard.stripe.com)                │
├────────────────────────────────────────┤
│                                        │
│  1. API Keys                           │
│     • Publishable Key ⬇ (PUBLIC OK)   │
│       → stripe-config.js               │
│     • Secret Key ⬇ (PRIVATE!)         │
│       → Firebase Functions             │
│                                        │
│  2. Create Products                    │
│     • Pro Plan ($29/month)             │
│       → Get Price ID                   │
│     • Enterprise (Custom)              │
│       → Get Price ID                   │
│       → stripe-config.js               │
│                                        │
│  3. Setup Webhook                      │
│     • Point to Cloud Function URL      │
│     • Listen to payment events         │
│       → Updates Firestore              │
│                                        │
└────────────────────────────────────────┘
```

---

## 📊 User Journey with All Systems

```
1. User visits landing page
   ⬇
   https://studio-4627045237-a2fe9.web.app/
   
2. Clicks "Get Started" button
   ⬇
   Redirects to /auth.html
   
3. Chooses sign-in method
   ├─ Email/Password
   │  ⬇
   │  firebase.auth().createUserWithEmailAndPassword()
   │  
   └─ Google OAuth
      ⬇
      firebase.auth().signInWithPopup(googleProvider)
      
4. Firebase validates credentials
   ⬇
   Creates user in Firebase Auth
   
5. Cloud Function triggers
   ⬇
   Creates user profile in Firestore:
   {
     userId: "...",
     email: "user@example.com",
     subscription: "free",
     createdAt: "...",
     postsCreated: 0,
     totalRevenue: 0
   }
   
6. Redirects to dashboard.html
   ⬇
   Loads user data from Firestore
   Displays stats, billing options
   
7. User clicks "Upgrade to Pro"
   ⬇
   Calls Cloud Function: createCheckoutSession
   
8. Cloud Function processes:
   ├─ Create Stripe Customer (if new)
   ├─ Create Checkout Session
   └─ Returns session ID
   
9. Stripe Checkout modal opens
   ⬇
   User enters payment details (4242 4242 4242 4242)
   
10. Stripe processes payment
    ⬇
    Sends webhook to Cloud Function
    
11. Cloud Function receives webhook
    ⬇
    ├─ Verifies signature
    ├─ Updates Firestore:
    │  • subscription: "pro"
    │  • nextBillingDate: "..."
    │  • lastPaymentDate: "..."
    └─ Creates transaction record
    
12. Browser refreshes dashboard
    ⬇
    Shows updated plan: "Pro"
    New limits unlocked
    
13. User has paid subscription! 💰
```

---

## 🔑 Required Keys & Secrets

| Key | Where to Find | Use | Keep Secret? |
|-----|----------------|-----|------|
| Firebase API Key | Firebase Console → Settings | Auth identification | ❌ OK to show |
| Firebase App ID | Firebase Console → Settings | App initialization | ❌ OK to show |
| Google Client ID | Google Cloud Console → Credentials | OAuth flow | ❌ OK to show |
| Stripe Publishable Key | Stripe Dashboard → API Keys | Frontend payments | ❌ OK to show |
| Stripe Secret Key | Stripe Dashboard → API Keys | Backend payments | ✅ KEEP SECRET |
| Stripe Webhook Secret | Stripe Dashboard → Webhooks | Verify webhooks | ✅ KEEP SECRET |
| Stripe Price ID (Pro) | Stripe Dashboard → Products | Checkout pricing | ❌ OK to show |
| Stripe Price ID (Enterprise) | Stripe Dashboard → Products | Checkout pricing | ❌ OK to show |

---

## 📁 Files to Update

### After Gathering Credentials:

1. **public/firebase-config.js**
   ```javascript
   const firebaseConfig = {
       apiKey: "YOUR_KEY",     // ⬅ UPDATE THIS
       authDomain: "studio-4627045237-a2fe9.firebaseapp.com",
       projectId: "studio-4627045237-a2fe9",
       storageBucket: "studio-4627045237-a2fe9.appspot.com",
       messagingSenderId: "612847421952",
       appId: "YOUR_APP_ID"    // ⬅ UPDATE THIS
   };
   ```

2. **public/stripe-config.js**
   ```javascript
   const STRIPE_CONFIG = {
       publishableKey: 'pk_test_YOUR_KEY',      // ⬅ UPDATE THIS
       priceIds: {
           pro: 'price_YOUR_PRO_ID',            // ⬅ UPDATE THIS
           enterprise: 'price_YOUR_ENTERPRISE'  // ⬅ UPDATE THIS
       }
   };
   ```

3. **Firebase Cloud Functions** (via CLI)
   ```bash
   firebase functions:config:set stripe.secret_key="sk_test_YOUR_KEY"
   firebase functions:config:set stripe.webhook_secret="whsec_YOUR_SECRET"
   firebase deploy --only functions
   ```

---

## ✅ Configuration Verification Checklist

```
Firebase:
☐ API Key updated in firebase-config.js
☐ App ID updated in firebase-config.js
☐ Email/Password authentication enabled
☐ Google OAuth enabled with Client ID
☐ Firestore database created
☐ Security rules deployed
☐ Cloud Functions deployed

Google:
☐ OAuth 2.0 Client ID created
☐ Authorized origins configured
☐ Redirect URIs configured

Stripe:
☐ Account created
☐ Publishable key in stripe-config.js
☐ Secret key in Cloud Functions
☐ Pro product created with price
☐ Enterprise product created with price
☐ Webhook created and configured
☐ Webhook secret in Cloud Functions

Testing:
☐ Auth page loads
☐ Email signup works
☐ Google OAuth works
☐ Dashboard loads after auth
☐ Firestore user data appears
☐ Stripe checkout button works
☐ Test payment succeeds
☐ Subscription updates in Firestore
☐ Dashboard shows new tier
```

---

## 🚀 Next Steps

1. **Gather all required keys** from Firebase, Google Cloud, and Stripe
2. **Update configuration files** (firebase-config.js, stripe-config.js)
3. **Deploy Cloud Functions** with Stripe credentials
4. **Test the complete flow** with test payments
5. **Deploy to production** when ready

---

**You've got the UI ready. Now let's connect it to the payment system! 💪**
