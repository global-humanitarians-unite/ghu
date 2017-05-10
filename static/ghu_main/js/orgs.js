function simulateSearch() {
    // Hack to show only our example results when searching
    var examples_start = 32;
    var examples_count = 3;

    if ($('#org-search-field').val().trim()) {
        $('#results').children('li').addClass('result-hidden');
        $('#results').children('li').slice(examples_start, examples_start + examples_count).removeClass('result-hidden');
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
