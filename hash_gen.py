import streamlit_authenticator as stauth

# Use a list for your password
passwords = ['admin123'] # Change 'admin123' to your desired password

# In version 0.4.2, use this format
hashed_passwords = stauth.Hasher.hash(passwords)

# Print the hashed result
print(hashed_passwords[0])