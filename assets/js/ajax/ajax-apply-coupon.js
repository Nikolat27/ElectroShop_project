function apply_coupon() {
    let coupon_code = document.getElementById("coupon_code").value
    let subtotal_field = document.getElementById("subtotal-price")
    $.ajax({
        url: `/cart/apply_coupon`,
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
