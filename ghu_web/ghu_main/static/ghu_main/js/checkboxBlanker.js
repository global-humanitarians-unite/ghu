function emptyTitle() {
    $('#id_slug').value = '';
}

$(function () {
    if ($('#id_page_condition').checked) {
        emptyTitle;
    }
});
