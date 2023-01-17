
function updatePreview() {
    var ec = document.getElementById('ellipsesContainer');
    json = ec.dataset.ellipses

    for (let i = 1; i < 4; i++) {
        document.getElementById('image-page-'+i).src = "/preview/?json=" + json + '&page=' + i
    }

    var btn = document.getElementById('genpdf');
    btn.href = "/getpdf/?json=" + json;

}


function refresh() {
    const n = document.querySelector('input[name="num-of-ellipses-radio"]:checked').value;
    // const n = document.getElementById('numOfEllipses').value;

    const req = new XMLHttpRequest();
    req.addEventListener("load", function() {
            var ec = document.getElementById('ellipsesContainer');
            ec.dataset.ellipses = this.responseText;

            updatePreview()
    });
    req.open("GET", "/ellipses/?n="+n);
    req.send();
}

btn = document.getElementById('num-of-ellipses');
btn.addEventListener("change", refresh);

refresh();