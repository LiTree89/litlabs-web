# GLAMFLOW AI - Setup & Deployment Checklist

## ✅ Completed
- [x] Firebase project created and configured
- [x] Website deployed to Firebase Hosting
- [x] GitHub Actions CI/CD pipeline set up
- [x] Landing page with chatbot widget
- [x] Authentication system with Google OAuth
- [x] Firestore database structure
- [x] Dashboard with billing and settings pages
- [x] Cloud Functions infrastructure created

## 🔴 REQUIRED - Setup Steps

### Step 1: Get Firebase Credentials
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `studio-4627045237-a2fe9`
3. Click **Settings** → **Project Settings**
4. Under **Your apps**, click **Web** (or add new web app)
5. Copy the firebaseConfig object
6. Update `public/firebase-config.js`:
   ```javascript
   const firebaseConfig = {
       apiKey: "YOUR_API_KEY_HERE",
       authDomain: "studio-4627045237-a2fe9.firebaseapp.com",
       projectId: "studio-4627045237-a2fe9",
       storageBucket: "studio-4627045237-a2fe9.appspot.com",
       messagingSenderId: "YOUR_MESSAGING_SENDER_ID_HERE",
       appId: "YOUR_APP_ID_HERE"
   };
   ```

### Step 2: Enable Firebase Authentication
1. Go to Firebase Console → **Authentication**
2. Click **Sign-in method**
3. Enable:
   - ✅ Email/Password
   - ✅ Google (add your OAuth credentials)
4. Add authorized redirect URIs:
   - `https://studio-4627045237-a2fe9.web.app`
   - `https://studio-4627045237-a2fe9.firebaseapp.com`
   - `localhost:5000` (for local testing)

### Step 3: Create Firestore Security Rules
1. Go to Firebase Console → **Firestore Database**
2. Click **Rules** tab
3. Replace with:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Users collection - only readable by the user themselves
       match /users/{userId} {
         allow read, write: if request.auth.uid == userId;
       }
       
       // Transactions collection - only readable by the user
       match /transactions/{document=**} {
         allow read: if request.auth.uid == resource.data.userId;
         allow write: if false; // Only written by Cloud Functions
       }
       
       // Subscriptions collection
       match /subscriptions/{document=**} {
         allow read: if request.auth.uid == resource.data.userId;
         allow write: if false; // Only written by Cloud Functions
       }
     }
   }
   ```
4. Click **Publish**

### Step 4: Setup Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Go to **APIs & Services** → **Credentials**
4. Create **OAuth 2.0 Client ID** (Web application):
   - Authorized JavaScript origins:
     - `https://studio-4627045237-a2fe9.web.app`
     - `https://studio-4627045237-a2fe9.firebaseapp.com`
     - `http://localhost:5000`
   - Authorized redirect URIs:
     - `https://studio-4627045237-a2fe9.web.app/__/auth/handler`
     - `https://studio-4627045237-a2fe9.firebaseapp.com/__/auth/handler`
     - `http://localhost:5000/__/auth/handler`
5. Copy Client ID
6. Add to Firebase Console → Authentication → Google → Web SDK configuration

### Step 5: Setup Stripe Integration
1. Create [Stripe account](https://stripe.com)
2. Go to **Developers** → **API Keys**
3. Copy:
   - **Publishable Key** → `public/stripe-config.js` (STRIPE_CONFIG.publishableKey)
   - **Secret Key** → Keep secure, used only in Cloud Functions
4. Create products in Stripe Dashboard:
   - **Pro Plan**: $29/month
   - **Enterprise Plan**: Custom pricing
5. Get Price IDs from Stripe Dashboard
6. Update `public/stripe-config.js`:
   ```javascript
   priceIds: {
       pro: 'price_1ABC...XYZ',        // Replace with actual
       enterprise: 'price_1ABC...ZYX'  // Replace with actual
   }
   ```

### Step 6: Deploy Cloud Functions
1. Install Firebase Tools:
   ```bash
   npm install -g firebase-tools
   ```
2. Deploy functions:
   ```bash
   firebase deploy --only functions
   ```
3. Configure environment variables in Firebase:
   ```bash
   firebase functions:config:set stripe.secret_key="sk_test_..."
   firebase functions:config:set stripe.webhook_secret="whsec_..."
   ```

### Step 7: Setup Stripe Webhook
1. Go to Stripe Dashboard → **Developers** → **Webhooks**
2. Add endpoint:
   - URL: `https://REGION-PROJECT_ID.cloudfunctions.net/stripeWebhook`
   - Events to listen to:
     - `invoice.payment_succeeded`
     - `invoice.payment_failed`
     - `customer.subscription.deleted`
     - `customer.subscription.updated`
3. Copy webhook signing secret → Firebase functions config

### Step 8: Update Dashboard
1. Replace placeholder text in dashboard.html with actual branding
2. Add company logo to dashboard
3. Customize pricing plans

### Step 9: Test Authentication Flow
1. Visit: `https://studio-4627045237-a2fe9.web.app/auth.html`
2. Test sign-up with email/password
3. Test Google OAuth login
4. Verify dashboard loads correctly

### Step 10: Test Payment Flow
1. Use Stripe test card: `4242 4242 4242 4242`
2. Click "Upgrade to Pro" on dashboard
3. Complete Stripe checkout
4. Verify subscription updated in Firestore

## 📁 Project Structure

```
litlabs-web/
├── public/
│   ├── index.html              # Landing page
│   ├── auth.html               # Authentication page
│   ├── dashboard.html          # User dashboard
│   ├── styles.css              # Landing page styles
│   ├── auth-styles.css         # Auth page styles
│   ├── dashboard-styles.css    # Dashboard styles
│   ├── script.js               # Landing page JS
│   ├── auth.js                 # Firebase auth logic
│   ├── dashboard.js            # Dashboard logic
│   ├── chatbot.js              # Chatbot widget
│   ├── firebase-config.js      # Firebase config
│   └── stripe-config.js        # Stripe config
├── functions/
│   ├── index.js                # Cloud Functions
│   └── package.json
├── firebase.json               # Firebase hosting config
├── .firebaserc                 # Firebase project config
├── .github/workflows/
│   └── firebase-hosting.yml    # GitHub Actions workflow
└── README.md                   # This file
```

## 🔑 Environment Variables Needed

```
Firebase:
- API Key
- Auth Domain
- Project ID
- Storage Bucket
- Messaging Sender ID
- App ID

Stripe:
- Publishable Key (frontend)
- Secret Key (backend - Cloud Functions)
- Webhook Secret
- Pro Plan Price ID
- Enterprise Plan Price ID
```

## 🚀 Deployment Commands

```bash
# Test locally
firebase serve

# Deploy everything
firebase deploy

# Deploy only functions
firebase deploy --only functions

# Deploy only hosting
firebase deploy --only hosting

# View logs
firebase functions:log
```

## 📝 User Flow

1. User lands on landing page → `index.html`
2. Clicks "Get Started" → redirects to `auth.html`
3. Signs up with email/password or Google OAuth
4. Redirects to `dashboard.html` (protected)
5. Views stats, billing options
6. Clicks "Upgrade to Pro"
7. Redirects to Stripe checkout
8. After payment, subscription updated in Firestore
9. User can manage billing in dashboard

## 🐛 Testing Stripe Locally

```javascript
// Use test cards:
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
CVC: Any 3 digits
Expiry: Any future date
```

## 🆘 Troubleshooting

**Issue**: "Firebase is not defined"
- Solution: Verify Firebase scripts are loaded in correct order in HTML

**Issue**: "CORS error accessing Stripe"
- Solution: Stripe should be accessed via Cloud Functions, not directly

**Issue**: "Payment not reflecting in Firestore"
- Solution: Check Cloud Function logs and Stripe webhook events

**Issue**: "Google OAuth not working"
- Solution: Verify OAuth client ID is correct and redirect URIs match exactly

## 📞 Next Steps

1. ✅ Configure all credentials above
2. ✅ Deploy Cloud Functions
3. ✅ Test end-to-end payment flow
4. ✅ Setup email notifications
5. ✅ Add analytics tracking
6. ✅ Create admin dashboard
7. ✅ Setup customer support system

---

**GLAMFLOW AI - Beauty Business Automation Platform**
Live at: `https://studio-4627045237-a2fe9.web.app`
