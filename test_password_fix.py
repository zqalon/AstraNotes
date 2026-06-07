"""Test password handling with argon2."""

import sys
sys.path.insert(0, '/Users/zacharyalon/Documents/Coding Projects/SCU Projects/CSEN 296/AstraNotes/src')

from astranotes.services import get_password_hash, verify_password


def test_short_password():
    """Test that short passwords work."""
    password = "short123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed), "Short password verification failed"
    print("✓ Short password test passed")


def test_long_password():
    """Test that long passwords work (argon2 has no limit)."""
    # Create a password longer than 72 bytes
    password = "a" * 100 + "special!@#$%"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed), "Long password verification failed"
    print("✓ Long password test passed")


def test_very_long_password():
    """Test very long passwords."""
    password = "x" * 500  # Very long
    hashed = get_password_hash(password)
    assert verify_password(password, hashed), "Very long password verification failed"
    print("✓ Very long password test passed")


def test_special_characters():
    """Test passwords with special characters."""
    password = "Very$pecial!@#$%^&*()_+-=[]{}|;:',.<>?/`~" * 2
    hashed = get_password_hash(password)
    assert verify_password(password, hashed), "Special character password verification failed"
    print("✓ Special character password test passed")


def test_unicode_password():
    """Test passwords with unicode characters."""
    password = "Contraseña123!🔐密码"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed), "Unicode password verification failed"
    print("✓ Unicode password test passed")


def test_password_roundtrip():
    """Test password creation and verification roundtrip."""
    passwords = [
        "simple",
        "Complex@Password123!",
        "x" * 80,  # Longer than old bcrypt limit
        "Very$pecial!@#$%^&*()_+-=[]{}|;:',.<>?/`~" * 2,  # Special chars
        "Contraseña123!🔐密码",  # Unicode
        "a" * 200,  # Very long
    ]
    
    for password in passwords:
        hashed = get_password_hash(password)
        assert verify_password(password, hashed), f"Failed for password: {password[:20]}..."
    
    print("✓ Password roundtrip test passed for all test cases")


def test_wrong_password():
    """Test that wrong passwords fail verification."""
    password = "correctPassword123"
    wrong_password = "wrongPassword456"
    hashed = get_password_hash(password)
    assert not verify_password(wrong_password, hashed), "Wrong password should fail"
    print("✓ Wrong password rejection test passed")


if __name__ == "__main__":
    try:
        test_short_password()
        test_long_password()
        test_very_long_password()
        test_special_characters()
        test_unicode_password()
        test_password_roundtrip()
        test_wrong_password()
        print("\n✅ All password handling tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
