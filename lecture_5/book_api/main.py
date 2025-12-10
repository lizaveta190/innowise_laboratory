from typing import Optional
from sqlalchemy import create_engine, String, func
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
from fastapi import FastAPI, HTTPException

# Connect to database
engine = create_engine("sqlite:///books.db")

class Base(DeclarativeBase):
    pass

class BookBase(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())  
    author: Mapped[str] = mapped_column(String())  
    year: Mapped[Optional[int]] = mapped_column()

# Create table in database
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {
        "message":"Book API"
    }


@app.get("/books")
def get_all_books():
    """Get all books."""

    with Session(engine) as session:
        books = session.query(BookBase).all()
        result = []
        for book in books:
            result.append({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "year": book.year
            })
        return result


@app.post("/books")
def add_book(title: str, author: str, year: Optional[int] = None):
    """Add a new book."""

    with Session(engine) as session:
        book = BookBase(title=title, author=author, year=year)
        session.add(book)
        session.commit()
        return {"message": "The book has been added successfully"}


@app.get("/books/search")
def find_book(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None
):
    """Search for books by title, author or year."""

    with Session(engine) as session:
        main_query = session.query(BookBase)
        
        if title:
            main_query = main_query.filter(func.lower(BookBase.title).like(f"%{title.strip().lower()}%"))
        if author:
            main_query = main_query.filter(func.lower(BookBase.author).like(f"%{author.strip().lower()}%"))
        if year:
            main_query = main_query.filter(BookBase.year == year)
        
        books = main_query.all()

        if not books:
            return []
        
        result = []
        for book in books:
            result.append({
                "id": book.id,
                "title": book.title, 
                "author": book.author, 
                "year": book.year
            })
        return result
        

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """Delete a book by ID."""

    with Session(engine) as session:
        book = session.query(BookBase).filter(BookBase.id == book_id).first()

        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
    
        session.delete(book)
        session.commit()
        return {"message": "The book has been deleted successfully"}    


@app.put("/books/{book_id}")
def update_book(
    book_id: int, 
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None
    ):
    """Update book details."""

    with Session(engine) as session:
        book = session.query(BookBase).filter(BookBase.id == book_id).first()

        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if year is not None:
            book.year = year
        
        session.commit()
        session.refresh(book)
        return {"message": "The data has been updated successfully"} 
    