document.getElementById('search-query').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearchBasedOnInput();
    }
});

function performSearchBasedOnInput() {
    const searchType = document.getElementById('search-type').value;
    const query = document.getElementById('search-query').value;
    performSearch(searchType, query);
}

document.getElementById('search-button').addEventListener('click', function() {
    const searchType = document.getElementById('search-type').value;
    const query = document.getElementById('search-query').value;
    performSearch(searchType, query);
});

function showData(e){
    const donde = document.querySelector("#results");
    const title = e._source.title.replace(/\"/g, '');
    const author = e._source.author.replace(/\"/g, '');
    const publisher = e._source.publisher.replace(/\"/g, '');
    // const message = e._source.message.replace(/\"/g, '');

    donde.innerHTML += `
    <div class="book-details">
        <h2>${title}</h2>
        <p><strong>ISBN:</strong> ${e._source.ISBN}</p>
        <p><strong>Author:</strong> ${author}</p>
        <p><strong>Date:</strong> ${e._source.YOP}</p>
        <p><strong>Publisher:</strong> ${publisher}</p>
        <p><strong>URL:</strong> <a href="${e._source.URLS}" target="_blank">Ver Imágenes</a></p>
    </div>
    `;
}
{/* <p><strong>Message:</strong> ${message}</p> */}

function performSearch(searchType, query) {
    fetch('http://localhost:9200/_search/template', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: searchType,
            params: { query: query }
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.hits.hits);
        document.querySelector("#results").innerHTML = '';
        data.hits.hits.forEach(element => {
            showData(element);
        });
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

