from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from models import User
from schemas import UserBase
from auth import hash_password, verify_password
from jwt_token import create_access_token
from dependencies import get_current_user
from schemas import UserResponse
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users")

@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    return db.query(User).all()


@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    valid_user = db.query(User).filter(User.user_id == user_id).first()
    if valid_user:
        return valid_user
    else:
        return {"message": "User not found"}
    

@router.post("/", response_model=UserResponse)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    user_data = user.model_dump()
    user_data["password"] = hash_password(user_data["password"])

    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{user_id}")
def update_user(user_id: int, detail: UserBase, db: Session = Depends(get_db)):
    valid_user = db.query(User).filter(User.user_id == user_id).first()
    if valid_user:
        valid_user.full_name = detail.full_name
        valid_user.email = detail.email
        valid_user.password = detail.password
        db.commit()
        return "User updated successfully"
    else:
        return {"message": "User not found"}
    

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    valid_user = db.query(User).filter(User.user_id == user_id).first()
    if valid_user:
        db.delete(valid_user)
        db.commit()
        return "User deleted successfully"
    else:
        return {"message": "User not found"}


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }