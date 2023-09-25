$('#product-filter-form').submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: 'json',

        beforeSend: function () {
            console.log("Filtering products...");
        },
        success: function (response) {
            console.log("Product have been filtered!");
            $("#filtered_products").html(response.data)
        }
    })
})
