#!/usr/bin/env node

/**
 * GLAMFLOW AI - Configuration Helper Script
 * 
 * This script helps you update Firebase and Stripe configuration
 * Usage: node config-setup.js
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(prompt) {
  return new Promise(resolve => {
    rl.question(prompt, resolve);
  });
}

async function main() {
  console.log('\n🔧 GLAMFLOW AI Configuration Setup\n');
  console.log('This will help you update your Firebase and Stripe configuration.\n');

  // Firebase Configuration
  console.log('=' .repeat(60));
  console.log('FIREBASE CONFIGURATION');
  console.log('=' .repeat(60));
  console.log('\nGo to: https://console.firebase.google.com/project/studio-4627045237-a2fe9/settings/general');
  console.log('Copy these values from "Your apps" section:\n');

  const apiKey = await question('1. Firebase API Key (AIzaSy...): ');
  const appId = await question('2. Firebase App ID (1:612847421952:web:...): ');

  // Stripe Configuration
  console.log('\n' + '='.repeat(60));
  console.log('STRIPE CONFIGURATION');
  console.log('='.repeat(60));
  console.log('\nGo to: https://dashboard.stripe.com/apikeys');
  console.log('And: https://dashboard.stripe.com/products\n');

  const publishableKey = await question('3. Stripe Publishable Key (pk_test_...): ');
  const proPriceId = await question('4. Stripe Pro Price ID (price_...): ');
  const enterprisePriceId = await question('5. Stripe Enterprise Price ID (price_...): ');

  // Update Firebase Config
  const firebaseConfigPath = path.join(__dirname, 'public', 'firebase-config.js');
  const firebaseConfig = `// Firebase Configuration & Initialization
// Get these from: https://console.firebase.google.com/project/studio-4627045237-a2fe9/settings/general

const firebaseConfig = {
    apiKey: "${apiKey}",
    authDomain: "studio-4627045237-a2fe9.firebaseapp.com",
    projectId: "studio-4627045237-a2fe9",
    storageBucket: "studio-4627045237-a2fe9.appspot.com",
    messagingSenderId: "612847421952",
    appId: "${appId}"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Get Firebase services
const auth = firebase.auth();
const db = firebase.firestore();

// Enable Google Sign-In
auth.useDeviceLanguage();

// Export for use in other scripts
window.firebaseAuth = auth;
window.firebaseDb = db;

console.log('Firebase initialized successfully!');`;

  fs.writeFileSync(firebaseConfigPath, firebaseConfig);
  console.log(`\n✅ Updated: ${firebaseConfigPath}`);

  // Update Stripe Config
  const stripeConfigPath = path.join(__dirname, 'public', 'stripe-config.js');
  const stripeConfig = `// Stripe Configuration
// Get your keys from https://dashboard.stripe.com/apikeys

const STRIPE_CONFIG = {
    // Publishable Key (safe to use in frontend)
    publishableKey: '${publishableKey}',
    
    // Price IDs from Stripe Dashboard
    priceIds: {
        pro: '${proPriceId}',
        enterprise: '${enterprisePriceId}'
    }
};

// Initialize Stripe
let stripe = null;

async function initStripe() {
    if (!stripe && STRIPE_CONFIG.publishableKey !== 'pk_test_YOUR_PUBLISHABLE_KEY_HERE') {
        stripe = Stripe(STRIPE_CONFIG.publishableKey);
    }
    return stripe;
}

// Create checkout session
async function createCheckoutSession(planType) {
    try {
        const priceId = STRIPE_CONFIG.priceIds[planType];
        
        if (!priceId || priceId.includes('YOUR_')) {
            alert('Stripe integration not yet configured. Please add your Stripe keys.');
            return;
        }

        // Call Cloud Function to create checkout session
        const response = await fetch('/.netlify/functions/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': \`Bearer \${await currentUser.getIdToken()}\`
            },
            body: JSON.stringify({
                priceId: priceId,
                userId: currentUser.uid,
                plan: planType
            })
        });

        const data = await response.json();
        
        if (data.sessionId) {
            const stripe = await initStripe();
            const { error } = await stripe.redirectToCheckout({
                sessionId: data.sessionId
            });
            
            if (error) {
                console.error('Stripe error:', error);
                alert('Error: ' + error.message);
            }
        }
    } catch (error) {
        console.error('Error creating checkout session:', error);
        alert('Error creating checkout session');
    }
}

// Manage customer's Stripe subscription
async function manageStripeSubscription() {
    try {
        const response = await fetch('/.netlify/functions/create-portal-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': \`Bearer \${await currentUser.getIdToken()}\`
            },
            body: JSON.stringify({
                userId: currentUser.uid
            })
        });

        const data = await response.json();
        
        if (data.url) {
            window.location.href = data.url;
        }
    } catch (error) {
        console.error('Error opening customer portal:', error);
        alert('Error opening billing portal');
    }
}`;

  fs.writeFileSync(stripeConfigPath, stripeConfig);
  console.log(`✅ Updated: ${stripeConfigPath}`);

  console.log('\n' + '='.repeat(60));
  console.log('✨ Configuration Updated Successfully!');
  console.log('='.repeat(60));
  console.log('\nNext steps:');
  console.log('1. Deploy Cloud Functions:');
  console.log('   firebase functions:config:set stripe.secret_key="sk_test_..."');
  console.log('   firebase deploy --only functions');
  console.log('\n2. Test authentication at:');
  console.log('   https://studio-4627045237-a2fe9.web.app/auth.html');
  console.log('\n3. Test dashboard at:');
  console.log('   https://studio-4627045237-a2fe9.web.app/dashboard.html\n');

  rl.close();
}

main().catch(console.error);
