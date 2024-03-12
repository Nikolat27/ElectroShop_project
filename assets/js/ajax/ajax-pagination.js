let page = 1; // Default page number
$(".pagination-link").on('click', function () {
    page = $(this).data('page');
    let filter_object = {};
    console.log(page);
    filter_object.page = page;
    $.ajax({
        url: '/products/filter-data',
        data: filter_object,
        dataType: 'json',
        success: function (response) {
            if (response.bool === true) {
                $("#filteredProducts").html(response.data);
            }
        }
    });
});