$(document).ready(function () {
    $('#add-to-cart').submit(function (e) { // catch the form's submit event
        e.preventDefault();
        let button = $("#add-to-cart-button")
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call

            beforeSend: function () {
                setTimeout(() => button.html("&#x2713;️"), 700);
            },

            success: function (response) {
                if (response.bool === true) {
                    setTimeout(() => button.html("Added to Cart!"), 1000);
                    $("#home_cart_list").html(response.data)
                }
            }
        });
    });
});