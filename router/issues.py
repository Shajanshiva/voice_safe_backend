from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Issue, User
from schemas import IssueBase
from sqlalchemy import func
from dependencies import get_current_user

router = APIRouter(prefix= "/issues")

@router.get("/")
def get_all_issues(db:Session = Depends(get_db)):
    return db.query(Issue).all()


@router.get("/category-count")
def category_count(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user) 
):
    result = (
        db.query(Issue.category_name, func.count(Issue.issue_id))
        .group_by(Issue.category_name)
        .all()
    )

    data = {
        "harassment": 0,
        "bullying": 0,
        "discrimination": 0,
        "favoritism": 0,
        "others": 0
    }

    for category, count in result:
        key = category.lower().replace(" ", "_")
        if key in data:
            data[key] = count
        else:
            data["others"] += count

    return data


@router.get("/{issue_id}")
def get_issue_by_id(issue_id:int, db:Session = Depends(get_db)):
    get_issue= db.query(Issue).filter(Issue.issue_id == issue_id).first()
    if get_issue:
        return get_issue
    else:
        return {"message":"Issue not found"}
    
@router.post("/")
def create_issue(
    detail: IssueBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    new_issue = Issue(
        user_id=current_user, 
        category_name=detail.category_name,
        title=detail.title,
        description=detail.description,
        evidence_url=detail.evidence_url
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return {
        "message": "Issue submitted successfully",
        "issue_id": new_issue.issue_id
    }


@router.put("/{issue_id}")
def update_issue(issue_id:int, detail:IssueBase, db:Session = Depends(get_db)):
    get_issue = db.query(Issue).filter(Issue.issue_id == issue_id).first()
    if get_issue:
        get_issue.category_name = detail.category_name
        get_issue.title = detail.title
        get_issue.description = detail.description
        get_issue.evidence_url = detail.evidence_url
        db.commit()
        return "Issue updated successfully"
    else:
        return {"message":"Issue not found"}
    
@router.delete("/{issue_id}")
def delete_issue(issue_id:int, db:Session = Depends(get_db)):
    get_issue = db.query(Issue).filter(Issue.issue_id == issue_id).first()
    if get_issue:
        db.delete(get_issue)
        db.commit()
        return "Issue deleted successfully"
    else:
        return {"message":"Issue not found"}
