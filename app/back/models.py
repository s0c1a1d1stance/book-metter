from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    books = relationship("Book", back_populates="owner")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    total_pages = Column(Integer)
    target_date = Column(String, nullable=True)
    
    # ▼ API (国立国会図書館) から取得する情報 ▼
    author = Column(String, nullable=True)         # 著者 (dc:creator)
    publisher = Column(String, nullable=True)      # 出版社 (dc:publisher) - 🌟追加
    published_year = Column(String, nullable=True) # 出版年 (dc:date)
    isbn = Column(String, nullable=True)           # ISBN (dc:identifier) - 🌟追加 (書影取得の鍵)
    description = Column(Text, nullable=True)      # 概要/説明 (description) - 🌟追加 (Text型で長文対応)
    ndl_link = Column(String, nullable=True)       # 国会図書館のリンク (link) - 🌟追加
    cover_url = Column(String, nullable=True)      # 書影画像URL (ISBNをもとにフロント側やAPI側で生成)

    # ▼ アプリ独自の管理情報 ▼
    status = Column(String, default="未読")         # ステータス（未読, 読書中, 読了）

    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="books")
    progress_logs = relationship("ProgressLog", back_populates="book")

class ProgressLog(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))
    
    start_page = Column(Integer)  
    end_page = Column(Integer)    
    memo = Column(Text, nullable=True) # メモも長くなる可能性があるのでText型がおすすめ
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    book = relationship("Book", back_populates="progress_logs")