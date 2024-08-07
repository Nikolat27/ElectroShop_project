$(document).ready(function () {
    $(".filter-checkbox, #priceFilterBtn, .sort-by, .show-by, .search-btn").on('click', function () {
        let filter_object = {};
        let price_slider = $("#price-slider").val

        let minPrice = $("#price-min").val()
        let maxPrice = $("#price-max").val()
        let q = $("#q").val()
        let sortBy = $("#sort-input-select").val() //Notice this input-select must be an "ID" not class!
        let show = $("#show-input-select").val()  //This too!

        filter_object.minPrice = minPrice;
        filter_object.maxPrice = maxPrice;
        filter_object.sortBy = sortBy;
        filter_object.show = show;
        filter_object.q = q;

        $(".filter-checkbox").each(function (index, ele) {
            let filter_value = $(this).val();
            let filter_key = $(this).data('filter');
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (el) {
                return el.value;
            });
        });
        $.ajax({
            url: '/products/filter-data',
            data: filter_object,
            dataType: 'json',
            success: function (response) {
                if (response.bool === true) {
                    // Update URL with GET parameters
                    history.pushState(null, '', response.new_url);
                    let url_path_field = document.getElementById("current_url");
                    console.log("Filter function", response.new_url)
                    url_path_field.value = response.new_url
                    $("#filteredProducts").html(response.data);
                    $("#pagination_products").html(response.data2);
                }
            }
        });
    });
});
