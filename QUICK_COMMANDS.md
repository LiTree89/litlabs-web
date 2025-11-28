# GLAMFLOW AI - QUICK COMMAND REFERENCE

## 🚀 Deploy Changes

```bash
# Stage and commit changes
git add .
git commit -m "your message here"

# Push to GitHub (auto-deploys to Firebase)
git push origin main

# Check deployment status
firebase hosting:channel:list
```

## 🔧 Local Testing

```bash
# Start Firebase local emulator
firebase emulators:start

# Deploy only hosting (no functions)
firebase deploy --only hosting

# Deploy only functions
firebase deploy --only functions

# View function logs
firebase functions:log
```

## 📋 Firebase Management

```bash
# Login to Firebase
firebase login

# List projects
firebase projects:list

# Set default project
firebase use studio-4627045237-a2fe9

# Check status
firebase status
```

## 🔐 Environment Variables

```bash
# Set Stripe secret key
firebase functions:config:set stripe.secret_key="sk_test_..."

# Set Stripe webhook secret
firebase functions:config:set stripe.webhook_secret="whsec_..."

# View all config
firebase functions:config:get
```

## 📱 URLs

| Page | URL |
|------|-----|
| **Landing** | https://studio-4627045237-a2fe9.web.app |
| **Auth** | https://studio-4627045237-a2fe9.web.app/auth.html |
| **Dashboard** | https://studio-4627045237-a2fe9.web.app/dashboard.html |
| **GitHub** | https://github.com/LiTree89/litlabs-web |

## 📊 File Locations

```
Configuration Files:
- public/firebase-config.js    ← Add Firebase credentials
- public/stripe-config.js      ← Add Stripe keys
- functions/index.js            ← Cloud Functions code

UI Files:
- public/index.html             ← Landing page
- public/auth.html              ← Sign in/up page
- public/dashboard.html         ← User dashboard

Styling:
- public/styles.css             ← Landing styles
- public/auth-styles.css        ← Auth styles
- public/dashboard-styles.css   ← Dashboard styles

JavaScript Logic:
- public/script.js              ← Landing interactivity
- public/auth.js                ← Firebase auth logic
- public/dashboard.js           ← Dashboard logic
- public/chatbot.js             ← Chatbot widget
- public/stripe-config.js       ← Stripe integration
```

## ✅ Checklist: What Works NOW

- [x] Landing page deployed
- [x] Chatbot widget working
- [x] Auth page created
- [x] Dashboard created
- [x] Firestore database ready
- [x] GitHub Actions auto-deploy working
- [x] Cloud Functions template ready

## ⚠️ Checklist: What Needs Config

- [ ] Firebase credentials in firebase-config.js
- [ ] Google OAuth setup
- [ ] Stripe account created
- [ ] Stripe keys added
- [ ] Cloud Functions deployed
- [ ] Stripe webhook configured
- [ ] Firestore security rules set

## 🐛 Common Issues

**Issue**: "Firebase is not defined"
```
Fix: Check that firebase-config.js is loaded BEFORE other scripts
in the HTML <head> section
```

**Issue**: "Cannot access dashboard"
```
Fix: Make sure you're signed in via auth.html first
```

**Issue**: "Stripe button not working"
```
Fix: Add Stripe publishable key to stripe-config.js
```

**Issue**: "Cloud Functions not deploying"
```
Fix: Run: firebase deploy --only functions --debug
```

## 🎯 ONE-CLICK DEPLOYS

Deploy everything:
```bash
cd C:\Users\dying && git add . && git commit -m "update" && git push origin main
```

Deploy only functions:
```bash
cd C:\Users\dying && firebase deploy --only functions
```

Check logs:
```bash
cd C:\Users\dying && firebase functions:log
```

## 💡 Pro Tips

1. Always test locally before pushing:
   ```bash
   firebase serve
   ```

2. Use Firebase Emulator for offline testing:
   ```bash
   firebase emulators:start
   ```

3. Monitor deployment in real-time:
   ```bash
   firebase hosting:channel:list
   ```

4. Never commit secrets - use Firebase Config:
   ```bash
   firebase functions:config:set your.secret="value"
   ```

5. Check GitHub Actions logs:
   - Go to: https://github.com/LiTree89/litlabs-web/actions
   - Click latest workflow
   - View build/deployment logs

---

**Last Updated**: November 28, 2025
**Status**: ✅ LIVE & READY FOR CONFIGURATION
