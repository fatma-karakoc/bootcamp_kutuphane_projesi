import pytest
from library import Book, Library


@pytest.fixture
def sample_library(tmp_path):
    """Geçici bir JSON dosyasıyla test için kütüphane"""
    filename = tmp_path / "test_library.json"
    return Library(str(filename))


def test_book_creation():
    book = Book("Test Kitap", "Yazar", "12345", 2024)
    assert book.title == "Test Kitap"
    assert book.author == "Yazar"
    assert book.isbn == "12345"
    assert book.year == 2024
    assert book.available is True


def test_borrow_and_return_book():
    book = Book("Deneme", "Yazar", "11111")
    assert book.available is True

    # Ödünç alma
    book.borrow()
    assert book.available is False

    # Tekrar ödünç alma (zaten ödünçte)
    book.borrow()
    assert book.available is False

    # İade etme
    book.return_book()
    assert book.available is True

    # Tekrar iade (zaten kütüphanede)
    book.return_book()
    assert book.available is True


def test_add_and_remove_book(sample_library):
    book = Book("Python 101", "Guido", "99999")
    sample_library.add_book(book)
    assert any(b.isbn == "99999" for b in sample_library.books)

    sample_library.remove_book("99999")
    assert not any(b.isbn == "99999" for b in sample_library.books)


def test_borrow_and_return_in_library(sample_library):
    book = Book("ML Kitabı", "Fatma", "22222")
    sample_library.add_book(book)

    # Ödünç alma
    sample_library.borrow_book("22222")
    assert sample_library.books[0].available is False

    # İade etme
    sample_library.return_book("22222")
    assert sample_library.books[0].available is True


def test_list_books_empty(capsys, sample_library):
    sample_library.list_books()
    captured = capsys.readouterr()
    assert "Kütüphanede hiç kitap yok." in captured.out
