window.onload = () => {
    $('.basket_list').on('click', 'input[type=number]', (event) => {
        let t_href = event.target;
        $.ajax({
            url: '/basket/edit/' + t_href.name + '/' + t_href.value + '/',
            success: (data) => {
                $('.basket_list').html(data.result)
            }
        })
        return false;
    })
}