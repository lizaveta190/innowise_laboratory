def generate_profile(age):
    """Return the life stage based on the user's age."""

    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"


user_name = input("Hello! Enter your full name: ")
birth_year_str = input("Enter your birth year: ")
birth_year = int(birth_year_str)
current_age = 2025 - birth_year
hobbies = []
while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    if hobby.lower() == "stop":
        break
    else:
        hobbies.append(hobby)

life_stage = generate_profile(current_age)
user_profile = {"name": user_name, "age": current_age, "birth_year": birth_year, "stage": life_stage, "hobbies": hobbies}

if len(hobbies) == 0:
    print(f"""
---
Profile Summary:
Name: {user_profile["name"]}
Age: {user_profile["age"]}
Life Stage: {user_profile["stage"]}
You didn't mention any hobbies.
---""")
else:
    print(f"""
---
Profile Summary:
Name: {user_profile["name"]}
Age: {user_profile["age"]}
Life Stage: {user_profile["stage"]}
Favourite Hobbies ({len(hobbies)}):""")
    for i in user_profile["hobbies"]:
        print(f"- {i}")
    print("---")
