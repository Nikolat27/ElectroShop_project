$('#delete-cart-form').submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: 'json',

        beforeSend: function () {
            console.log("Deleting Product...");
        },
        success: function (response) {
            console.log("Product Deleted successfully!");
            if (response.bool === true) {
                $("#cart-items-count").text(response.totalcartitems)
                $("#cart-view").html(response.data)
            }
        }
    })
})