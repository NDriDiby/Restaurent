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