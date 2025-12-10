from typing import Optional
from sqlalchemy import create_engine, String, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, Mapped, mapped_column
from fastapi import Depends, FastAPI, HTTPException


engine = create_engine("sqlite:///books.db")
SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())  
    author: Mapped[str] = mapped_column(String())  
    year: Mapped[Optional[int]] = mapped_column()

# Create table in database
Base.metadata.create_all(bind=engine)

# Create a dependency for getting a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def root():
    return {
        "message":"Book API"
    }


@app.get("/books")
def get_all_books(db: Session = Depends(get_db)):
    """Get all books."""

    books = db.query(Book).all()
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
def add_book(title: str, author: str, year: Optional[int] = None, db: Session = Depends(get_db)):
    """Add a new book."""

    book = Book(title=title, author=author, year=year)
    db.add(book)
    db.commit()
    return {"message": "The book has been added successfully"}


@app.get("/books/search")
def find_book(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Search for books by title, author or year."""

    main_query = db.query(Book)
    
    if title:
        main_query = main_query.filter(func.lower(Book.title).like(f"%{title.strip().lower()}%"))
    if author:
        main_query = main_query.filter(func.lower(Book.author).like(f"%{author.strip().lower()}%"))
    if year:
        main_query = main_query.filter(Book.year == year)
    
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
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book by ID."""

    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "The book has been deleted successfully"}    


@app.put("/books/{book_id}")
def update_book(
    book_id: int, 
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
    ):
    """Update book details."""

    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if title is not None:
        book.title = title
    if author is not None:
        book.author = author
    if year is not None:
        book.year = year
    
    db.commit()
    db.refresh(book)
    return {"message": "The data has been updated successfully"} 
