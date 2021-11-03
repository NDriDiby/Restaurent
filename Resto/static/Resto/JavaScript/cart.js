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
        cuisine()

    })
}


function cuisine() {
    var url = '/sendorder/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ "order": 'sent' })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data)

        })

}