import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client

from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_ANON_KEY"])
app = FastAPI(title="Task 6 API (Supabase)")


# Schemas

class UserIn(BaseModel):
    username: str


class PostIn(BaseModel):
    title: str
    text: str
    author_id: int


class PostUpdate(BaseModel):
    title: str
    text: str


class CommentIn(BaseModel):
    comment_text: str
    post_id: int
    author_id: int


class UserUpdate(BaseModel):
    username: str


class CommentUpdate(BaseModel):
    comment_text: str
    post_id: int
    author_id: int

# ------- Posts ------- 


# Add new post
@app.post("/posts", tags=["Posts"])
def create_post(payload: PostIn):
    response = supabase.table("post").insert({
        "title": payload.title,
        "text": payload.text,
        "author_id": payload.author_id
    }).execute()

    if not response.data:
        raise HTTPException(400, "Insert failed")
    return response.data[0]


# Get all posts
@app.get("/posts", tags=["Posts"])
def list_posts():
    response = supabase.table("post").select("*").order("created_at", desc=True).execute()
    return response.data


# Update post by post id
@app.patch("/posts/{post_id}", tags=["Posts"])
def update_post(post_id: int, payload: PostUpdate):
    patch = payload.model_dump(exclude_none=True)
    if not patch:
        raise HTTPException(400, "Nothing to update")
    response = supabase.table("post").update(patch).eq("post_id", post_id).execute()
    if not response.data:
        raise HTTPException(404, "Post not found")
    return response.data[0]


# Delete post by post id
@app.delete("/posts/{post_id}", tags=["Posts"])
def delete_post(post_id: int):
    response = supabase.table("post").delete().eq("post_id", post_id).execute()
    if response.count == 0 and not response.data:
        # в некоторых версиях count может не вернуться — проверяем data
        raise HTTPException(404, "Post not found")
    return {"ok": True}


# ------- Users ------- 


# Add new user
@app.post("/users", tags=["Users"])
def create_user(payload: UserIn):
    response = supabase.table("user").insert({"username": payload.username}).execute()
    if not response.data:
        raise HTTPException(400, "Insert failed")
    return response.data[0]


# Get all users
@app.get("/users", tags=["Users"])
def list_users():
    response = supabase.table("user").select("*").order("user_id", desc=True).execute()
    return response.data


# Update user by user_id
@app.patch("/users/{user_id}", tags=["Users"])
def update_user(user_id: int, payload: UserUpdate):
    patch = payload.model_dump(exclude_none=True)
    if not patch:
        raise HTTPException(400, "Nothing to update")
    response = supabase.table("user").update(patch).eq("user_id", user_id).execute()
    if not response.data:
        raise HTTPException(404, "User not found")
    return response.data[0]


# ------- Comments ------- 


# Add new comment
@app.post("/comments", tags=["Comments"])
def create_comment(payload: CommentIn):
    response = supabase.table("comment").insert({
        "comment_text": payload.comment_text,
        "post_id": payload.post_id,
        "author_id": payload.author_id
    }).execute()
    if not response.data:
        raise HTTPException(400, "Insert failed")
    return response.data[0]


# Get all comments
@app.get("/comments", tags=["Comments"])
def list_comments():
    response = supabase.table("comment").select("*").order("created_at", desc=True).execute()
    return response.data


# Update comment by comment_id
@app.patch("/comments/{comment_id}", tags=["Comments"])
def update_comment(comment_id: int, payload: CommentUpdate):
    patch = payload.model_dump(exclude_none=True)
    if not patch:
        raise HTTPException(400, "Nothing to update")
    response = supabase.table("comment").update(patch).eq("comment_id", comment_id).execute()
    if not response.data:
        raise HTTPException(404, "Comment not found")
    return response.data[0]


# Delete comment by comment_id
@app.delete("/comments/{comment_id}", tags=["Comments"])
def delete_comment(comment_id: int):
    response = supabase.table("comment").delete().eq("comment_id", comment_id).execute()
    return {"ok": True}