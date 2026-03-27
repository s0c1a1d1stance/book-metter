from pydantic import BaseModel, computed_field
from typing import List, Optional
from datetime import datetime

# --- Progress (進捗ログ) ---
class ProgressBase(BaseModel):
    date: str
    start_page: int
    end_page: int
    memo: Optional[str] = None

class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: int
    book_id: int
    created_at: Optional[datetime] = None  # 🌟追加: いつ記録されたか

    class Config:
        from_attributes = True

# --- Book (本) ---
class BookBase(BaseModel):
    title: str
    total_pages: int
    target_date: Optional[str] = None  # 🌟変更: 目標日が未定の場合に備えてOptionalに

    # 🌟追加: API (国立国会図書館) から取得する情報など
    # （データが存在しない・取得できない場合も考慮してすべて Optional にしています）
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    ndl_link: Optional[str] = None
    cover_url: Optional[str] = None
    status: str = "未読"

class BookCreate(BookBase):
    user_id: int

class Book(BookBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None  # 🌟追加
    updated_at: Optional[datetime] = None  # 🌟追加: ホーム画面の「最近の5件」の並び替えに必須！
    progress_logs: List[Progress] = []

    # ★ 追加：APIがBookを返す時に、自動で「実質の合計ページ」を計算して含める
    @computed_field
    def total_read_pages(self) -> int:
        from .crud import calculate_total_progress
        # ログが空の場合の安全策
        if not self.progress_logs:
            return 0
        return calculate_total_progress(self.progress_logs)

    class Config:
        from_attributes = True

# --- User (ユーザー) ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: Optional[datetime] = None  # 🌟追加
    books: List[Book] = []

    class Config:
        from_attributes = True