from flask_app.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask import flash
from datetime import datetime, timedelta
from flask_app.config.config import Config

bcrypt = Bcrypt()

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.programming_language = data['programming_language']
        self.interests = data['interests']

    @classmethod
    def save(cls, data):
        data['interests'] = ','.join(data.get('interests', []))
        query = """
            INSERT INTO users 
            (first_name, last_name, email, password, birthday, programming_language, interests) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(birthday)s, %(programming_language)s, %(interests)s);
        """
        return connectToMySQL('login_and_reg_schema').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_and_reg_schema').query_db(query, data)
        if not result:
            return None
        return cls(result[0]) if result else None

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        data = {'user_id': user_id}
        result = connectToMySQL('login_and_reg_schema').query_db(query, data)
        if result:
            user = result[0]
            user['interests'] = user['interests'].split(',')
            return cls(user)
        else:
            flash("User not found.", "error")
            return None


# Removed validation.py
# User validation

    @staticmethod
    def validate_user(user):
        is_valid = True

        if User.get_by_email({'email': user.get('email', '')}):
            flash("Email already exists.", 'register')
            is_valid = False
        if not User.validate_email(user.get('email', '')):
            flash("Invalid email address!", 'register')
            is_valid = False
        if not User.validate_first_name(user.get('first_name', '')):
            flash("First name must contain only letters and be at least 2 characters long.", 'register')
            is_valid = False
        if not User.validate_last_name(user.get('last_name', '')):
            flash("Last name must contain only letters and be at least 2 characters long.", 'register')
            is_valid = False
        if not User.validate_password(user.get('password', '')):
            flash("Invalid password! Password must be at least 8 characters long and contain at least one uppercase letter and one number.", 'register')
            is_valid = False
        if not User.validate_confirm_password(user.get('password', ''), user.get('confirm_password', '')):
            flash("Password confirmation does not match.", 'register')
            is_valid = False
        if not User.validate_date_of_birth(user.get('birthday', '')):
            flash("Invalid date of birth! You must be at least 10 years old and under 100 years old.", 'register')
            is_valid = False
        if not User.validate_interests(user.get('interests', [])):
            flash("Please select at least one interest.", 'register')
            is_valid = False
        if not User.validate_programming_language(user.get('programming_language', '')):
            flash("Please select a programming language.", 'register')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_email(email):
        return Config.EMAIL_REGEX.match(email) is not None

    @staticmethod
    def validate_first_name(first_name):
        return first_name.isalpha() and len(first_name) >= 2

    @staticmethod
    def validate_last_name(last_name):
        return last_name.isalpha() and len(last_name) >= 2

    @staticmethod
    def validate_password(password):
        return (
            len(password) >= 8 and
            Config.PASSWORD_REGEX_UPPERCASE.search(password) and
            Config.PASSWORD_REGEX_NUMBER.search(password)
        )

    @staticmethod
    def validate_date_of_birth(date_of_birth):
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
            age = (datetime.now() - dob) // timedelta(days=365.25)
            return 10 <= age < 100
        except ValueError:
            return False

    @staticmethod
    def validate_interests(interests):
        return bool(interests)

    @staticmethod
    def validate_programming_language(programming_language):
        return bool(programming_language)

    @staticmethod
    def validate_confirm_password(password, confirm_password):
        return password == confirm_password

# Login validation

    @staticmethod
    def validate_login_email(email):
        if not User.validate_email(email):
            flash("Invalid email address!", 'login')
            return False
        return True

    @staticmethod
    def validate_login_password(user, password):
        if not user or not bcrypt.check_password_hash(user.password, password):
            flash("Invalid password.", 'login')
            return False
        return True

    @staticmethod
    def validate_login(email, password):
        user = User.get_by_email({'email': email})
        if not user:
            flash("Email not found.", 'login')
            return False, None
        if not User.validate_login_password(user, password):
            return False, None
        return True, user
