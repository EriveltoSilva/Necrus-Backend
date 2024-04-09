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



window.addEventListener('load', ()=>{
    let updateBtns = document.getElementsByClassName('update-cart');
    
    for (let i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function(){
            let productId = this.dataset.product;
            let action = this.dataset.action;
            console.log('elemento:',i,', productId:', productId, ", action:", action);

            console.log('User:', user);
            if(user == 'AnonymousUser'){
                console.log('User is not authenticated!');
            }
            else{
                console.log('User is authenticated!');
                updateCartItem(productId, action);
            }
        });        
    }
    
    function updateCartItem(productId, action){
        let url = "/produtos/actualizaar-carrinho/";
        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId':productId, 'action':action})
        })
        .then((resp)=> resp.json())
        .then((data)=>{
            console.log(data);
            location.reload();
        })
        .catch((e)=>{
            console.log("Erro", e);
        })
    }
});