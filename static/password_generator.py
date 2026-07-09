import random
import string

print("🔐 FORGE CODE INDIA - ADVANCED PASSWORD GENERATOR")

length = int(input("Enter password length: "))

if length < 4:
    print("⚠️ Password length should be at least 4.")
else:

    use_numbers = input("Include numbers? (y/n): ").lower()

    use_symbols = input("Include symbols? (y/n): ").lower()

    characters = string.ascii_letters

    if use_numbers == "y":
        characters += string.digits

    if use_symbols == "y":
        characters += "!@#$%^&*()"

    password = ""

    for i in range(length):
        password += random.choice(characters)

    print("\n✅ Generated Password:")
    print(password)

    print("\n🎉 Password generation completed!")