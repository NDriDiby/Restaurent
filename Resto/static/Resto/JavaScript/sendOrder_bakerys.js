// // send order to the kitchon
var sendOrder = document.getElementsByClassName("send-orderBakerys")
var cust_note = document.getElementById('customer_note')


for (let i = 0; i < sendOrder.length; i++) {
    sendOrder[i].addEventListener("click", function() {

        if(cust_note.value){
            console.log("Sending Order to the Kitchen")
            console.log("recording Order note....", cust_note)
            console.log("Customer Note Recorded:", cust_note.value)
            var action = this.dataset.action
            var order = this.dataset.order
            var note = cust_note.value
            console.log(order)
            console.log(note)
            cuisine(action, order, note)
            console.log('redicting you to .....')
        }
        else{
            console.log("Info Client: Order Completed")
            var action = this.dataset.action
            var order = this.dataset.order
            var note = " "
            console.log('redicting you to .....')
            cuisine(action, order, note)

        }

        

        

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