$(document).ready(function () {
    $("#province-select").on('click', function () {
        let province = document.getElementById("province-select").value

        let data = {}

        data.province = province
        //Ajax Start
        $.ajax({
            method: "GET",
            url: '/cart/filter_cities',
            data: data,
            dataType: 'json',
            success: function (response) {
                if (response.bool === true) {
                    let cities = response.data

                    // Clear existing options
                    $("#city-select").empty();

                    // Loop through the cities and add them as options
                    cities.forEach(function (city) {
                        $("#city-select").append(`<option value="${city.name}">${city.name}</option>`);
                    });
                }
            }
        });
        //End
    })
});