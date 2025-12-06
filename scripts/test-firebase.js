(async () => {
  try {
    const mod = await import('firebase');
    console.log('firebase imported. exported keys:', Object.keys(mod).slice(0, 12));
    console.log('Node version:', process.version);
    process.exit(0);
  } catch (err) {
    console.error('firebase import failed:', err && err.message ? err.message : err);
    process.exit(1);
  }
})();
