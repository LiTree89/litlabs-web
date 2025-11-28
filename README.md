# Firebase install verification

Files added by the automated setup:

- `scripts/test-firebase.js` - small script that resolves `firebase` and prints its path.
- `src/firebase.example.js` - example snippet showing how to initialize Firebase (comments only).
- `.gitignore` - ignores `node_modules` and `.env`.

Quick commands

PowerShell:

```powershell
node scripts/test-firebase.js
Get-Content package.json
```

If you want this repository committed, the setup script will initialize Git and create a first commit.

Notes

- Replace the example config with real Firebase project settings when you integrate the SDK.
- Do not commit real credentials; use environment variables or secret management.
