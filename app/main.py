from sign_in_window import SignInWindow
from users_database import initialize_database

if __name__ == "__main__":  
    initialize_database()
    sign_in_window = SignInWindow()
    sign_in_window.run()