// Example Firebase initialization (replace values with your config)
// This file is an example only — do not commit real credentials.

// For modular SDK (v9+):
// import { initializeApp } from 'firebase/app';
// const firebaseConfig = { apiKey: 'YOUR_API_KEY', authDomain: 'YOUR_AUTH_DOMAIN' };
// const app = initializeApp(firebaseConfig);
// export default app;

// For CommonJS environments, you can require and inspect the package:
const firebasePkg = require('firebase');
module.exports = {
  note: 'This is an example file. Use the modular SDK in apps.',
  firebasePackage: typeof firebasePkg,
};
