from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey,Text, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

 

class Issue(Base):
    __tablename__ = 'issues'

    issue_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    category_name = Column(String )
    title = Column(String)
    description = Column(Text)
    evidence_url = Column(String)


class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey('issues.issue_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    comment_text = Column(Text)
