(function($) {
    // If the box is now checked, blank out the target field and disable it.
    // Otherwise, re-enable the field and restore its contents. If it was blank
    // before, trigger Django prepopulation from source→target.
    function emptyTarget(checkbox, target, source) {
        if (checkbox.prop('checked')) {
            target.prop('disabled', true);
            target.data('old_value', target.val());
            target.val('');
        } else {
            target.prop('disabled', false);
            // Trigger Django prepopulation when the value before checking the
            // box was blank
            if (target.data('old_value') === '') {
                source.change();
            } else {
                target.val(target.data('old_value'));
            }
        }
    }

    // Empty the target and check the box if the target is blank
    function emptyTargetIfBlank(checkbox, target, source) {
        if (target.val() === '') {
            checkbox.prop('checked', true);
            emptyTarget(checkbox, target, source);
        }
    }

    $(function () {
        // Set up events for every element with a `data-target-field'
        // attribute, which should be all of the blanker checkboxes in the page
        $('[data-blanker-target-field]').each(function (index, element) {
            var checkbox = $(element);
            var target = $(checkbox.data('blanker-target-field'));
            var source = $(checkbox.data('blanker-source-field'));

            // If the target field (the one to blank) is already empty, then
            // disable the field and check the box.
            emptyTargetIfBlank(checkbox, target, source);

            // When the checkbox changes checkedness, disable or re-enable the
            // target field
            checkbox.on('input', function () {
                emptyTarget(checkbox, target, source);
            });

            // If the user erases the target field by hand and then clicks
            // away, disable the field and check the box
            target.on('focusout', function () {
                emptyTargetIfBlank(checkbox, target, source);
            });
        });
    });
})(django.jQuery);
