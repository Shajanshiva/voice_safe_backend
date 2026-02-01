from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, verify_password
from jwt_token import create_access_token
from dependencies import get_current_user
from schemas import UserBase, UserResponse, userLogin, UserUpdate

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

@router.get("/me/profile", response_model=UserResponse)
def get_current_user_profile(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.user_id == current_user).first()
    return user
    

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
def update_user(user_id: int, detail: UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Only allow users to update their own profile
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")
        
    valid_user = db.query(User).filter(User.user_id == user_id).first()
    if valid_user:
        valid_user.full_name = detail.full_name
        valid_user.email = detail.email
        
        # Only update password if provided
        if detail.password and detail.password.strip():
            valid_user.password = hash_password(detail.password)
            
        db.commit()
        return {"message": "Profile updated successfully"}
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
    user_credentials: userLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id
    }