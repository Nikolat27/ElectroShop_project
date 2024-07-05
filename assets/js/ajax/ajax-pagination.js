function ajaxPagination(query_params) {

    // Decode the query parameters
    query_params = decodeURIComponent(query_params);

    // Split the query params string by '&' to get individual key-value pairs
    let params = query_params.split('&');

    // Create an object to store the parsed parameters
    let filter_object = {};

    // Loop through the key-value pairs and parse them
    for (let param of params) {
        let [key, value] = param.split('=');

        // Check if the parameter key already exists in the filter object
        if (filter_object.hasOwnProperty(key)) {
            // If the key already exists, check if the value is an array
            if (Array.isArray(filter_object[key])) {
                // If it's an array, push the new value to it
                filter_object[key].push(value);
            } else {
                // If it's not an array, convert the existing value to an array and push the new value
                filter_object[key] = [filter_object[key], value];
            }
        } else {
            // If the key doesn't exist, add it to the filter object
            filter_object[key] = value;
        }
    }

    $.ajax({
        url: '/products/filter-data',
        data: filter_object,
        dataType: 'json',
        success: function (response) {
            if (response.bool === true) {
                // Update URL with GET parameters
                history.pushState(null, '', response.new_url);
                let url_path_field = document.getElementById("current_url");
                url_path_field.value = response.new_url
                console.log("Pagination function", response.new_url)
                $("#filteredProducts").html(response.data);
                $("#pagination_products").html(response.data2);
            }
        }
    });
}