from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Comment
from schemas import commentBase

router = APIRouter(prefix= "/comments")

@router.get("/")
def get_all_comments(db:Session = Depends(get_db)):
    return db.query(Comment).all()

@router.get("/{comment_id}")
def get_comment_id(comment_id:int, db:Session = Depends(get_db)):
    get_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if get_comment:
        return get_comment
    else:
        return {"message":"Comment not found"}

@router.post("/")
def create_comment(detail:commentBase, db:Session = Depends(get_db)):
    new_comment = Comment(**detail.model_dump())
    db.add(new_comment)
    db.commit()
    return new_comment

@router.put("/{comment_id}")
def update_comment(comment_id:int, detail:commentBase, db:Session = Depends(get_db)):
    get_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if get_comment:
        get_comment.comment_text = detail.comment_text
        db.commit()
        return "Comment updated successfully"
    else:
        return {"message":"Comment not found"}
    
@router.delete("/{comment_id}")
def delete_comment(comment_id:int, db:Session = Depends(get_db)):
    get_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if get_comment:
        db.delete(get_comment)
        db.commit()
        return "Comment deleted successfully"
    else:
        return {"message":"Comment not found"}