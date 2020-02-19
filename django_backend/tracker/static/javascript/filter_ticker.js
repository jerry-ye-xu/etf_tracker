document.getElementById("ticker_search_bar").addEventListener('click', function (event) {
    event.stopPropagation();
});

function filterSearch() {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('ticker_search_bar');
  filter = input.value.toUpperCase();
  ul = document.getElementById("ticker_list");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    console.log(a.textContent)
    console.log(a.innerText)
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}