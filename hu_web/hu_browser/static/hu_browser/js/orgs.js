function simulateSearch() {
    if ($('#org-search-field').val().trim()) {
        $('#results').children('li').addClass('result-hidden');
        $('#results').children('li:lt(3)').removeClass('result-hidden');
    } else {
        $('#results').children('li').removeClass('result-hidden');
    }
}

$(function () {
    $('#org-search-btn').on('click', simulateSearch);
    $('#org-search-field').on('keypress', function (e) {
        var enter = 13;
        if (e.which == enter) {
            simulateSearch();
        }
    });
});
