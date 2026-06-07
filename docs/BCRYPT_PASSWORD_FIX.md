# Password Hashing Security Guide

## Problem Solved

Fixed bcrypt-related authentication errors by using a dual-scheme approach:

1. **Version Incompatibility**: `AttributeError: module 'bcrypt' has no attribute '__about__'`
   - bcrypt and passlib versions had compatibility issues

2. **Password Length Limit**: `ValueError: password cannot be longer than 72 bytes`
   - bcrypt has a fundamental 72-byte hard limit on password length

3. **Hash Identification Error**: `passlib.exc.UnknownHashError: hash could not be identified`
   - Occurred when existing bcrypt hashes couldn't be verified with argon2-only config

## Solution: Dual-Scheme Password Hashing

Use both argon2 and bcrypt for maximum compatibility:

### Implementation

Updated [src/astranotes/services.py](../src/astranotes/services.py):
```python
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)
```

### How It Works

1. **New passwords** → Hashed with argon2 (modern, no limits)
2. **Existing passwords** → Can still be verified with bcrypt hashes
3. **Password verification** → Passlib automatically identifies and verifies both types
4. **Transparent upgrade** → With `deprecated="auto"`, old bcrypt hashes can be re-hashed on next login

### Key Advantages

| Aspect | Single argon2 | Dual argon2+bcrypt |
|--------|---------------|-------------------|
| New passwords | ✓ Argon2 | ✓ Argon2 |
| Existing bcrypt hashes | ✗ Fails | ✓ Works |
| Password length limit | None | None |
| Security | Modern | Modern + Compatible |
| Migration path | Breaks existing data | Seamless upgrade |

## Files Modified

- [src/astranotes/services.py](../src/astranotes/services.py) - Updated CryptContext to support both schemes
- [requirements.txt](../requirements.txt) - Updated to `passlib[argon2]>=1.7.4`

## Testing

The fix ensures:
- ✅ Existing bcrypt-hashed passwords can be verified
- ✅ New passwords are hashed with argon2
- ✅ No more `UnknownHashError` when verifying existing accounts
- ✅ No password length limit for new registrations


