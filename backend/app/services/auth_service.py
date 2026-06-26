from supabase import Client
from app.schemas.auth import UserLogin, UserRegister

class AuthService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    def register_user(self, user: UserRegister):
        res = self.supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "full_name": user.full_name
                }
            }
        })
        return res

    def login_user(self, user: UserLogin):
        res = self.supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return res
