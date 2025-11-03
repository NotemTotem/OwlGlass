document.getElementsByClass('answer').style.display = 'none'

function toggleText() {
  var x = document.getElementById('answer1');
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } 
    else {
        x.style.display = 'none';
    }
}
