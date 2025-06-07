$(document).ready(function () {
    const $productsList = $("#products-list");

    // Save original index and clone for each product
    $(".product-item").each(function (index) {
        $(this).attr("data-original-index", index);
        $(this).data("original", $(this).clone());
    });

    // CATEGORY FILTER
    $(".filter-btn").click(function () {
        const filter = $(this).data("filter");

        // Highlight the active filter button
        $(".filter-btn").removeClass("active-filter");
        $(this).addClass("active-filter");

        // Filter products
        $(".product-item").each(function () {
            const category = $(this).data("category");
            if (filter === "all" || category === filter) {
                $(this).removeClass("d-none");
            } else {
                $(this).addClass("d-none");
            }
        });

        // Reset sort highlight (optional)
        $(".price-option").removeClass("active-sort");
    });

    // PRICE SORT
    $(".price-option").click(function (e) {
        e.preventDefault();

        const order = $(this).data("order");

        // Highlight active sort button
        $(".price-option").removeClass("active-sort");
        $(this).addClass("active-sort");

        const $visible = $(".product-item").filter(function () {
            return !$(this).hasClass("d-none");
        });

        // DEFAULT SORT
        if (order === "default") {
            const sorted = $visible.sort(function (a, b) {
                const indexA = parseInt($(a).attr("data-original-index"));
                const indexB = parseInt($(b).attr("data-original-index"));
                return indexA - indexB;
            });

            $productsList.append(sorted);
            return;
        }

        // ASC/DESC PRICE SORT
        const sorted = $visible.sort(function (a, b) {
            const aSale = $(a).data("sale-price");
            const bSale = $(b).data("sale-price");

            const priceA = aSale ? parseFloat(aSale) : parseFloat($(a).data("price"));
            const priceB = bSale ? parseFloat(bSale) : parseFloat($(b).data("price"));

            return order === "asc" ? priceA - priceB : priceB - priceA;
        });

        $productsList.append(sorted);
    });
});
