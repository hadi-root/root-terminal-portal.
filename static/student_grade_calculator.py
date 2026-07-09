print("🎓 STUDENT GRADE CALCULATOR")

english = int(input("English: "))
maths = int(input("Maths: "))
science = int(input("Science: "))

total = english + maths + science

percentage = total / 3

print("\nTotal:", total)

print("Percentage:", round(percentage, 2), "%")

if percentage >= 90:
    grade = "A+"

elif percentage >= 80:
    grade = "A"

elif percentage >= 70:
    grade = "B"

elif percentage >= 60:
    grade = "C"

elif percentage >= 50:
    grade = "D"

else:
    grade = "F"

print("Grade:", grade)

if percentage >= 35:
    print("✅ PASS")

else:
    print("❌ FAIL")
