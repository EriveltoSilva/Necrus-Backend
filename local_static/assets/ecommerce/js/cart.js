const csrftoken = getCookie('csrftoken');
var cart = JSON.parse(getCookie('cart'));


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// function getCookie(name) {
//     let cookieArr = document.cookie.split(';');
//     for (let i = 0; i < cookieArr.length; i++) {
//         let cookiePair = cookieArr[i].split("=");
//         if (name == cookiePair[0].trim()) {
//             return decodeURIComponent(cookiePair[i]);
//         }
//     }
//     return null;
// }

(function ($) {
    "use strict";

    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });

})(jQuery);



window.addEventListener('load', () => {
    let updateBtns = document.getElementsByClassName('update-cart');

    for (let i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            let productId = this.dataset.product;
            let action = this.dataset.action;
            // console.log('elemento:', i, ', productId:', productId, ", action:", action);

            if (user == 'AnonymousUser'){
                addCookieItem(productId, action);
            }
            else 
                updateCartItem(productId, action);
        });
    }

    function addCookieItem(productId, action){
        console.log('User is not authenticated!');
        if (action=='add'){
            if(cart[productId] == undefined){
                cart[productId] = {'quantity':1}
            }
            else
            {
                cart[productId]['quantity'] += 1
            }
        }
        if (action=='remove'){
            cart[productId]['quantity'] -= 1

            if(cart[productId]['quantity']<=0)
            {
                console.log("Deleting item from cart!");
                delete cart[productId]
            }
        }
        console.log('Cart:', cart);
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
        window.location.reload()
    }

    function updateCartItem(productId, action) {
        let url = "/produtos/actualizaar-carrinho/";
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
            .then((resp) => resp.json())
            .then((data) => {
                console.log(data);
                location.reload();
            })
            .catch((e) => {
                console.log("Erro", e);
            })
    }
});


window.addEventListener('load', () => {

    if (cart == undefined) {
        cart = {}
        console.log('Cart Created!', cart);
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    }
})