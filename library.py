import json
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

## Aşama 1
class Book:
    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True

    def borrow(self):
        if self.available:
            self.available = False
            print(f"{self.title} kitabı ödünç alındı.")
        else:
            print(f"{self.title} kitabı zaten ödünçte.")

    def return_book(self):
        if not self.available:
            self.available = True
            print(f"{self.title} kitabı iade edildi.")
        else:
            print(f"{self.title} kitabı zaten kütüphanede mevcut.")

    def __str__(self):
        durum = "Mevcut" if self.available else "Ödünç"
        return f"{self.title} - {(self.author)}  [{self.isbn}] - {durum}"


class Library:
    def __init__(self,filename="library.json"):
        self.filename = filename
        self.books = self.load_books()

    def save_books(self):
        data = []
        for b in self.books:
            data.append({"title": b.title, "author": b.author, "isbn": b.isbn, "available": b.available})
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def load_books(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                books = []
                for d in data:
                    books.append(Book(d["title"], d["author"], d["isbn"], d["available"]))
                return books
        except:
            return []
    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f"{book.title} kitap kütüphaneden silindi.")
                return
        print("Bu ISBN'e sahip kitap kütüphanede yok.")

    def list_books(self):
        if not self.books:
            print("Kütüphanede hiç kitap yok.")
        for book in self.books:
            print(book)

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.borrow()
                return
        print("Bu ISBN'e sahip kitap kütüphanede yok.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.return_book()
                return
        print("Bu ISBN'e sahip kitap kütüphanede yok.")
 ## Aşama 2
    def get_book_from_api(self, isbn):
        url = f"https://openlibrary.org/isbn/{isbn}.json"
        try:
            response = httpx.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                title = data.get("title", "Unknown Title")

                # Yazar bilgisi almak için
                authors = []
                for author in data.get("authors", []):
                    key = author.get("key")
                    if key:
                        author_resp = httpx.get(f"https://openlibrary.org{key}.json")
                        if author_resp.status_code == 200:
                            authors.append(author_resp.json().get("name", "Unknown Author"))
                author_str = ", ".join(authors) if authors else "Unknown Author"

                book = Book(title, author_str, isbn)
                self.add_book(book)
                return book
            else:
                return None
        except Exception:
            return None

app = FastAPI()
library = Library()

class ISBNRequest(BaseModel):
    isbn: str

class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str

@app.get("/books")
def get_books():
    return [b.to_dict() for b in library.list_books()]

@app.post("/books")
def add_book(req: ISBNRequest):
    book = library.add_book_from_api(req.isbn)
    if book:
        return {"message": "Kitap eklendi", "book": book.to_dict()}
    return {"error": "Kitap bulunamadı"}

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    book = library.find_book(isbn)
    if book:
        library.remove_book(isbn)
        return {"message": f"{isbn} silindi."}
    return {"error": "Kitap bulunamadı."}
def main():
    library = Library()

    while True:
        print("\n--- MENÜ ---")
        print("1. Kitap ekle (API ile)")
        print("2. Kitap sil")
        print("3. Kitapları listele")
        print("4. Kitap ödünç al")
        print("5. Kitap iade et")
        print("6. Çıkış")
        secim = input("Seçiminiz: ")

        if secim == "1":
            isbn = input("ISBN girin: ")
            book = library.get_book_from_api(isbn)
            if book:
                library.add_book(book)
                print(f"{book.title} kitap kütüphaneye eklendi.")
        elif secim == "2":
            isbn = input("Silmek istediğiniz kitabın ISBN'ini girin: ")
            library.remove_book(isbn)
        elif secim == "3":
            library.list_books()
        elif secim == "4":
            isbn = input("Ödünç almak istediğiniz kitabın ISBN'ini giriniz: ")
            library.borrow_book(isbn)
        elif secim == "5":
            isbn = input("İade etmek istediğiniz kitabın ISBN'ini giriniz: ")
            library.return_book(isbn)
        elif secim == "6":
            print("Çıkış yapılıyor.")
            break
        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    main()
