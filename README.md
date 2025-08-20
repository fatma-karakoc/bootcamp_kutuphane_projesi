# bootcamp_kutuphane_projesi
Nesne yönelimli programlama (OOP) prensiplerini kullanarak oluşturulmuş basit bir kitap yönetim sistemidir. OpenLibrary API üzerinden ISBN numarasına göre kitap bilgisi getirir. 
Kullanıcılar kitap ekleyebilir, silebilir, listeleyebilir,ödünç alıp,iade edebilir. 

- Kitaplar library.json dosyasında saklanır. 
- ISBN numarası her kitap için benzersiz olmalıdır.

Ana Metodlar:
add_book(book): Kitap ekleme
remove_book(isbn): Kitap silme
list_books(): Kitapları listeleme
borrow_book(isbn): Ödünç alma
return_book(isbn): İade etme
get_book_from_api(isbn): API'den kitap bilgisi alma

