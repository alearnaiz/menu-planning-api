$(function() {
    $("#start-date").datepicker(
        {
            firstDay: 1,
            dateFormat: 'yy-mm-dd'
        }
    );
    $("#end-date").datepicker(
        {
            firstDay: 1,
            dateFormat: 'yy-mm-dd'
        }
    );

    $("#create-menu").click(function() {
        var data = {
            start_date: $("#start-date").val(),
            end_date: $("#end-date").val(),
            start_lunch: $("#start-lunch").prop('checked'),
            end_dinner: $("#end-dinner").prop('checked')
        };

        if (!$("#more-options-panel").hasClass("hidden")) {
            data['name'] = getValueOrNull($("#name").val());
            data['favourite'] = $("#favourite").prop('checked');
        } else {
            data['name'] = null;
            data['favourite'] = false;
        }

        $.ajax({
            method: "POST",
            url: "/web/create-menu",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json"
        }).done(function(menu) {
            window.location.href = "/web/edit-menu/"+menu.id
        }).fail(function() {
            $("#error-panel").removeClass("hidden");
        });
    });

    $("#more-options").click(function() {
        if ($("#more-options-panel").hasClass("hidden")) {
            $("#more-options-panel").removeClass("hidden");
        } else {
            $("#more-options-panel").addClass("hidden");
        }
    });
});