"use strict"
window.onload = function () {
    let _quantity, _price, _price_total, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];
    let price_total_arr = [];
    let TOTAL_FORMS = +$('input[name="orderitems-TOTAL_FORMS"]').val();
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
    for (let i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($(`input[name="orderitems-${i}-quantity"]`).val());
        _price = parseFloat($(`.orderitems-${i}-price`).text().replace(',', '.'));
        _price_total = parseFloat($(`.orderitems-${i}-price_total`).text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        price_arr[i] = _price ? _price : 0;
        price_total_arr[i] = _price_total ? _price_total : 0;
    }

    let orderSummaryUpdate = (orderitem_price, delta_quantity) => {
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_cost.toString());
    };

    let deleteOrderItem = row => {
        let target_name = row[0].querySelector('input[type=number]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    };

    $('.order_form').on('click', 'input[type=number]', () => {
        let target = event.target;
        orderitem_num = +target.name.replace('orderitems-', '').replace('-quantity', '');
        if (price_arr[orderitem_num]) {
            orderitem_quantity = +target.value;
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            $(`.orderitems-${orderitem_num}-price_total`)
                .html((price_arr[orderitem_num] * quantity_arr[orderitem_num]).toFixed(2).toString());
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    })

    $('.order_form').on('click', 'input[type=checkbox]', () => {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = target.checked ? -quantity_arr[orderitem_num] : quantity_arr[orderitem_num]
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });

    $('.formset_row').formset({
        addText: 'Добавить товар',
        deleteText: 'Удалить товар',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

    $('.order_form').on('change', 'select', () => {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        let product_id = target.options[target.selectedIndex].value;
        if (product_id) {
            $.ajax({
                url: `/order/product/price/${product_id}/`,
                success: data => {
                    if (data.price) {
                        price_arr[orderitem_num] = data.price;
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0;
                        }
                        let price_string = `<span>${data.price.toString()}</span>`;
                        let current_tr = $('.order_form table').find(`tr:eq(${orderitem_num + 1})`);
                        current_tr.find('td:eq(2)').html(price_string);

                        $(`.orderitems-${orderitem_num}-price_total`)
                            .html((price_arr[orderitem_num] * quantity_arr[orderitem_num]).toFixed(2).toString());

                        // TODO: summary
                        orderSummaryUpdate(price_arr[orderitem_num], 0);
                    }
                }
            })
        }
    })

}