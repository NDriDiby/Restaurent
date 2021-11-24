// // send order to the kitchon
var sendOrder = document.getElementsByClassName("send-orderBakerys")


for (let i = 0; i < sendOrder.length; i++) {
    sendOrder[i].addEventListener("click", function() {
        console.log("Sending Order....")


        var action = this.dataset.action
        var order = this.dataset.order
        var note = this.dataset.note

        console.log(order)
        console.log(note)
        cuisine(action, order, note)
        console.log('redicting you to .....')

    })
}

function cuisine(act, ord, note) {

    var url = '/bakerys/sendorder/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ "action": act, 'order': ord, 'note': note })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data)

        })
}