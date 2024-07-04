function clear_filters() {
    data = {}
    let current_url = document.getElementById("current_url")
    data.current_url = current_url
    console.log("Your current url", current_url)
    $.ajax({
        method: "GET",
        url: `/products/clear-filters`,
        data: data,
        dataType: 'json',
        success: function (response) {
            let new_url = response.url
            $.ajax({
                method: "GET",
                url: `${new_url}`,
                data: data,
                dataType: 'json',
                success: function (response) {
                    history.pushState(null, '', response.new_url);
                    let url_path_field = document.getElementById("current_url");
                    url_path_field.value = response.new_url
                    $("#filteredProducts").html(response.data);
                    $("#pagination_products").html(response.data2);
                }
            });
        }
    });
}