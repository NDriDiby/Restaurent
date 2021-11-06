// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart")
for (var i = 0; i < updated_but.length; i++) {
    updated_but[i].addEventListener('click', function() {
        var itemId = this.dataset.product
        var action = this.dataset.action

        if (user === 'AnonymousUser') {
            console.log('not logged in')
        } else {
            updateUserOrder(itemId, action)
        }
    })
}


function updateUserOrder(itemId, action) {
    console.log(user, 'is logged in, sengind data....')

    var url = '/updateitem/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ "itemId": itemId, 'action': action })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data)

        })
}


// // send order to the kitchon
var sendOrder = document.getElementsByClassName("send-order")

for (let i = 0; i < sendOrder.length; i++) {
    sendOrder[i].addEventListener("click", function() {
        console.log("Sending Order....")


        var action = this.dataset.action
        var order = this.dataset.order

        console.log(order)
        cuisine(action, order)
        console.log('redicting you to .....')

    })
}



function cuisine(act, ord) {

    var url = '/sendorder/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ "action": act, 'order': ord })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data)

        })
}