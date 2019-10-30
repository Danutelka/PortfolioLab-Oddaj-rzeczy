document.addEventListener("DOMContentLoaded", function() {
    //var kat = document.getElementById('kat');
    var ilosc = document.getElementById('ilosc');
    var org = document.getElementById('org');
    var adres = document.getElementById('adres');
    var miasto = document.getElementById('miasto');
    var kod = document.getElementById('kod');
    var tel = document.getElementById('tel');
    var data = document.getElementById('data');
    var godz = document.getElementById('godz');
    var uwagi = document.getElementById('uwagi');
    var gotowe = document.getElementById('gotowe');
    gotowe.addEventListener('click', function(event) {
        //event.preventDefault();
        var tr1 = document.createElement('tr');
        var tr2 = document.createElement('tr');
        var tr3 = document.createElement('tr');
        var tr4 = document.createElement('tr');
        var tr5 = document.createElement('tr');
        var tr6 = document.createElement('tr');
        var tr7 = document.createElement('tr');
        var tr8 = document.createElement('tr');
        var tr9 = document.createElement('tr');
        tr1.innerText = ilosc.value;
        tr2.innerText = org.checked;
        tr3.innerText = adres.value;
        tr4.innerText = miasto.value;
        tr5.innerText = kod.value;
        tr6.innerText = tel.value;
        tr7.innerText = data.value;
        tr8.innerText = godz.value;
        tr9.innerText = uwagi.value;
    })
});