# Imports
# import uuid
# from flask import request
from xml.dom.minidom import Identified
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity

from db import db
from schemas import UserSchema
from models import UserModel
from blocklist import BLOCKLIST

# A blueprint is used to seperate the API in segments
blp = Blueprint("Users", __name__, description="Operations on users") # first arg is name, second arg import name, description 


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # User_data will be a dict containing the user and password
        if UserModel.query.filter(UserModel.username==user_data["username"]).first():
            abort(409, message = "A user with that username already exists.")
        
        # Create new user
        user = UserModel(
            username = user_data["username"],
            # Hashing password
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        # Add new user to database
        db.session.add(user)
        db.session.commit()

        return {"message": "User created succesfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
            
        abort(401, message="Invalid creditals")

# Refresh
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}


# Logout
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}



@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200