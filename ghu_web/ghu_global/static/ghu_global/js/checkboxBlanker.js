(function () {
    var $ = django.jQuery;

    function emptyTitle() {
        $('#id_slug').value = '';
    }

    function testFunction() {
        var header = document.createElement('H1');
        var text = document.createTextNode('Hello, Peeps!');
        header.appendChild(text);
        document.body.appendChild(header);
    }

    $(function () {
        $('#id_make_home_page').on('click', testFunction);
    });

    var h = document.createElement('H1');
    var t = document.createTextNode('YO!!!!!');
    h.appendChild(t);
    document.body.appendChild(h);
})();
