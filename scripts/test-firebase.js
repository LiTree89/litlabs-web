try {
  const pkgPath = require.resolve('firebase');
  console.log('firebase resolved at', pkgPath);
  console.log('Node version:', process.version);
  process.exit(0);
} catch (err) {
  console.error('firebase require failed:', err && err.message ? err.message : err);
  process.exit(1);
}
