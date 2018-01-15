$(function() {

    $("#delete-all").click(function() {
        $.ajax({
            method: "DELETE",
            url: "/web/grocery-list",
            contentType: "application/json"
        }).done(function() {
            window.location.reload();
        }).fail(function() {
            $("#error-panel").removeClass("hidden");
        });
    });

    $("#add-product").click(function() {
        $.ajax({
            method: "GET",
            url: "/web/template-product",
            dataType: "html"
        }).done(function(template) {
            $("table").append(template);
        });

    });
});

function deleteProduct(productId) {
    $.ajax({
        method: "DELETE",
        url: "/web/edit-product/"+productId,
        contentType: "application/json"
    }).done(function() {
        $("tr[data-id='"+productId+"']").remove();
    }).fail(function() {
        $("#error-panel").removeClass("hidden");
    });
}

function updateProduct(productId) {
    $product = $("tr[data-id='"+productId+"']");

    var data = {
        name: getValueOrNull($product.find(".name").val()),
        quantity: getValueOrNull($product.find(".quantity").val()),
        status: getValueOrNull($product.find(".status").val())
    }

    $.ajax({
        method: "PUT",
        url: "/web/edit-product/"+productId,
        contentType: "application/json",
        data: JSON.stringify(data)
    }).done(function() {
    }).fail(function() {
        $("#error-panel").removeClass("hidden");
    });
}

function addProduct(element) {
    $product = $(element).closest('tr');

    var data = {
        name: getValueOrNull($product.find(".name").val()),
        quantity: getValueOrNull($product.find(".quantity").val()),
        status: getValueOrNull($product.find(".status").val())
    }

    $.ajax({
        method: "POST",
        url: "/web/grocery-list",
        contentType: "application/json",
        data: JSON.stringify(data)
    }).done(function() {
        window.location.reload();
    }).fail(function() {
        $("#error-panel").removeClass("hidden");
    });
}