from fastapi import FastAPI
from fastapi.responses import JSONResponse

import models
from database import engine, SessionLocal
from pydantic import BaseModel
from models import User

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class UserRequest(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    password: str
    new_password: str


@app.get("/user/{email}")
def get_user(email: str):
    try:
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "message": f"There is no account registered with this email: {email}"
                }
            )
        return JSONResponse(
            status_code=200,
            content=user
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@app.get("/users/all")
def get_all_users():
    try:
        db = SessionLocal()
        all_users = db.query(models.User).all()
        if not all_users:
            return JSONResponse(
                status_code=400,
                content={"message": "There are no accounts in database!"}
            )
        return JSONResponse(
            status_code=200,
            content=all_users
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@app.delete("/user/{email}")
def delete_user(email: str):
    try:
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "message": f"There is no account registered with this email: {email}"
                }
            )
        db.query(models.User).filter(models.User.email == email).delete()
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"message": "Account deleted successfully!"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )


@app.post("/user")
def create_user(user_request: UserRequest):
    try:
        db = SessionLocal()
        user = User()
        user.email = user_request.email
        user.password = user_request.password
        if user not in db:
            db.add(user)
            db.commit()
            return JSONResponse(
                status_code=200,
                content={"message": "Account created successfully!"}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"message": "There already exists an account registered with this email!"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message":str(e)
            }
        )


@app.put("/user/{email}")
def update_user(email: str, user_update: UserUpdate):
    try:
        db = SessionLocal()
        current_user = db.query(models.User).filter(models.User.email == email).first()
        if not current_user:
            return JSONResponse(
                status_code=400,
                content={"message": "There is no account registered with this email!"}
            )
        if current_user.password == user_update.password:
            if user_update.password != user_update.new_password:
                setattr(current_user, "password", user_update.new_password)
                db.commit()
                return JSONResponse(
                    status_code=200,
                    content={"message": "User updated successfully!"}
                )
            return JSONResponse(
                status_code=400,
                content={"message": "New password is same as the old one!"}
            )
        return JSONResponse(
            status_code=400,
            content={"message": "Password is wrong!"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )
