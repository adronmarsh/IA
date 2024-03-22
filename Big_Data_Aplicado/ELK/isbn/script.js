let isbnQuery = document.getElementById('isbn-query').value;
document.getElementById('search-isbn-button').addEventListener('click', function() {
    isbnQuery = document.getElementById('isbn-query').value;
    searchByISBN(isbnQuery);
});
let _id = null
function searchByISBN(isbnQuery) {
    fetch('http://localhost:9200/libros/_search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: {
                match: {
                    ISBN: isbnQuery
                }
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.hits.hits.length > 0) {
            const book = data.hits.hits[0]._source;
            _id = data.hits.hits[0]._id
            
            displayBookDetails(book);
        } else {
            alert("No se encontraron libros con ese ISBN");
        }
    })
    .catch(error => console.error('Error en la búsqueda:', error));
}

function displayBookDetails(book) {
    console.log(book);
    document.getElementById('edit-container').style.display = 'block';
    document.getElementById('edit-title').value = book['title'];
    document.getElementById('edit-isbn').value = book['ISBN'];
    document.getElementById('edit-author').value = book['author'];
    document.getElementById('edit-year').value = book['YOP'];
    document.getElementById('edit-publisher').value = book['publisher'];
    document.getElementById('edit-urlL').value = book['URL-L'];
    document.getElementById('edit-urlM').value = book['URL-M'];
    document.getElementById('edit-urlS').value = book['URL-S'];
}

document.getElementById('update-button').addEventListener('click', function() {
    const updatedData = {
        "title": document.getElementById('edit-title').value,
        "ISBN": document.getElementById('edit-isbn').value,
        "author": document.getElementById('edit-author').value,
        "YOP": document.getElementById('edit-year').value,
        "publisher": document.getElementById('edit-publisher').value,
        "URL-L": document.getElementById('edit-urlL').value,
        "URL-M": document.getElementById('edit-urlM').value,
        "URL-S": document.getElementById('edit-urlS').value,

    };
    updateBookData(updatedData);
});

function updateBookData(updatedData) {


    fetch(`http://localhost:9200/libros/_doc/${_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body:JSON.stringify(updatedData)
      })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data._shards.successful == 1);
        if(data._shards.successful == 1) {
            document.querySelector("body").innerHTML += ("Datos del libro actualizados con éxito");
        } else {
            document.querySelector("body").innerHTML += ("No se encontraron libros para actualizar con ese ISBN");
        }
    })
    .catch(error => console.error('Error al actualizar:', error));
}
