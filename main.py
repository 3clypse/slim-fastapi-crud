"""
Basic user CRUD, using Fastapi, async DB calls and Oauth login (Github SSO)
"""

import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, Cookie, HTTPException, status
from fastapi.responses import JSONResponse
from schemas import Token, User, UserCreate
from typing import Any, Annotated, List, Optional, Union
from jose import JWTError, jwt
from datetime import datetime, timedelta
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from config import sso
import json
from models import users
from database import engine, database, metadata
from sqlite3 import IntegrityError

##################################################################################
# Load ENV vars
load_dotenv()

# Init the DB
metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

##################################################################################


async def get_current_user(access_token: Optional[str] = Cookie(default=None)):
    """ Validate and return the current user"""
    if not access_token:
        raise HTTPException(
            401, "Not authorized. Please, go to /auth/login")
    try:
        return jwt.decode(access_token, os.environ.get('SECRET_KEY'), algorithms=[os.environ.get('ALGORITHM')])
    except JWTError:
        raise HTTPException(401, "Provided access_token is invalid or expired")


async def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.environ.get('SECRET_KEY'), algorithm=os.environ.get('ALGORITHM'))
    return encoded_jwt


# OAUTH LOGIN
@app.get("/auth/login")
async def auth_init():
    """Initialize oauth and redirect"""
    return await sso.get_login_redirect()


# OAUTH CALLBACK
@app.get("/auth/callback", response_model=Token)
async def auth_callback(request: Request):
    """Verify login, create auth cookie and return the value."""
    try:
        user = await sso.verify_and_process(request)
    except CustomOAuth2Error:
        return await auth_init()

    # Create access token and the cookie containing it
    token = await create_access_token(json.dumps(user.dict()))
    response = JSONResponse(
        content={"access_token": token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=token, httponly=True,
                        secure=False, expires=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))*60, samesite="lax")

    # If the user exists, continue. Else, create it
    try:
        user_create = UserCreate(username=user.display_name, gh_id=user.id)
        await create_user(user=user_create, token=token)
    except HTTPException:
        pass  # The user already exist, so continue
    except Exception:
        # @TODO log the error
        pass
    finally:
        # Also, return the token. Maybe you want to use the API directly with curl, Postman or so.
        return response


@app.get("/")
async def root(token: Annotated[str, Depends(get_current_user)]):
    return {"ok"}


# CRUD


# GET
@app.get("/users/all", response_model=List[User])
async def get_all_users(token: Annotated[str, Depends(get_current_user)]):
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/me", response_model=User)
async def show_me(token: Annotated[str, Depends(get_current_user)]):
    user_data = json.loads(token.get('sub'))
    u = UserCreate(username=user_data['display_name'], gh_id=user_data['id'])

    query = users.select().where(users.c.username ==
                                 u.username).where(users.c.gh_id == u.gh_id)
    return await database.fetch_one(query)


# POST
@app.post("/users/me", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: UserCreate, token: Annotated[str, Depends(get_current_user)]):
    try:
        query = users.insert().values(username=user.username, roles=user.roles, gh_id=user.gh_id,
                                      first_name=user.first_name, last_name=user.last_name, address=user.last_name)
        last_record_id = await database.execute(query)
        return {**user.dict(), "id": last_record_id}
    except IntegrityError:
        # @TODO log the error
        # logger.warn(f"DB query failed. Details: {e}")
        raise HTTPException(
            status_code=409, detail=f"Failed. Maybe the '{user.username}' already exists.")


# PUT
@app.put("/users/me", response_model=User)
async def update_user(user: UserCreate, token: Annotated[str, Depends(get_current_user)]):
    user_data = json.loads(token.get('sub'))
    u = UserCreate(username=user_data['display_name'], gh_id=user_data['id'])
    query = users.update().where(users.c.username == u.username).where(users.c.gh_id == u.gh_id).values(
        first_name=user.first_name, last_name=user.last_name, address=user.last_name)
    await database.execute(query)

    # Return the user with updated values
    query = users.select().where(users.c.username ==
                                 u.username).where(users.c.gh_id == u.gh_id)
    result = await database.fetch_one(query)

    if result is None:
        raise HTTPException(
            status_code=409, detail=f"Failed. Maybe the '{user.username}' doesnt exists.")

    return result


# DELETE
@app.delete("/users/me")
async def delete_me(token: Annotated[str, Depends(get_current_user)]):
    user_data = json.loads(token.get('sub'))
    u = UserCreate(username=user_data['display_name'], gh_id=user_data['id'])

    query = users.delete().where(users.c.username ==
                                 u.username).where(users.c.gh_id == u.gh_id)
    await database.fetch_one(query)
    return None
