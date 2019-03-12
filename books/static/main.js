$(document).ready(function(){
    $('select').material_select();
});


<script src="https://code.jquery.com/jquery-1.10.2.js"></script>
<script type="text/javascript">

goodRead('9382749004'); // not found
goodRead('0441172717'); // single author
goodRead('0552137030'); // multiple author

function goodRead(isbn) {

var key = "<3H6GDwms6FaFQpmFQHqNQ>"; // replace with your key

var url = "https://www.goodreads.com/book/isbn/" + isbn + "?key=" + key;

$.get("http://query.yahooapis.com/v1/public/yql",
{
q: "select * from xml where url=\""+url+"\"",
format: "json"
},
function(json){

if(json.query.results.error === "Page not found") {
console.log("no book found");
} else {

var book = json.query.results.GoodreadsResponse.book;

var title           = book.title;
var isbn10          = book.isbn;
var isbn13          = book.isbn13;
var country_code    = book.country_code;
var image_url       = book.image_url;
var small_image_url = book.small_image_url;
var publisher       = book.publisher;
var description     = book.description;

var all_authors = book.authors.author;



if(book.authors.author.length===undefined) { //single author

var authors = [all_authors.name];

} else { // multiple authors

var author_count = all_authors.length

var authors = [];

for( i=0 ; i<author_count ; i++) {
authors.push(all_authors[i].name)
}

}

var book_object = {
"title"           : title,
"isbn10"          : isbn10,
"isbn13"          : isbn13,
"country_code"    : country_code,
"image_url"       : image_url,
"small_image_url" : small_image_url,
"publisher"       : publisher,
"description"     : description,
"authors"         : authors,
}
console.log(book_object);

}
}
);
}

</script>