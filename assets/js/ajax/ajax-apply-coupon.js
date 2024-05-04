function apply_coupon(id) {
    let coupon_code = document.getElementById("coupon_code").value
    let subtotal_field = document.getElementById("subtotal-price")
    $.ajax({
        url: `/cart/apply_coupon/${id}`,
        data: {
            coupon_code: coupon_code
        },
        dataType: 'json',

        success: function (response) {
            if (response.bool === true) {
                subtotal_field.innerText = response.subtotal;
            }
        }
    });
}
