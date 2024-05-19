$(document).ready(function () {
    $("#color-select").on('click', function () {
        let color = document.getElementById("color-select").value
        let product_id = document.getElementById("product_id_fieldd").value

        let data = {}

        data.color = color
        //Ajax Start
        $.ajax({
            method: "GET",
            url: `/products/filter_colors/${product_id}`,
            data: data,
            dataType: 'json',
            success: function (response) {
                if (response.bool === true) {
                    $("#quantity-available-field").val(response.data);
                    let quantityField = $("#quantity-buy-field");
                    quantityField.attr('max', response.data);


                }
            }
        });
        //End
    })
});