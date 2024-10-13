var updateBtns = document.getElementsByClassName('update-cart')

for (i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productID = this.dataset.product 
        var action = this.dataset.action 

        console.log({
            "productID": productID, 'action' : action, "user" : user
        })

        if (user == "AnonymousUser"){
            console.log("Hello AnonymousUser")
            addCookieItem(productID, action)
        }
        else{
          
            updateUserOrder(productID,action )
            console.log("Verified user")
        }
    })
}


function updateUserOrder(productID, action){
    var url = '/update_item/'
    fetch(url , {
        method: "POST",
        body: JSON.stringify({
          'productID': productID,
          'action' : action
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          "X-CSRFToken" : csrftoken
        }
      })  
        .then((response) => {
          response.json()
        })
        .then((data) => {
          console.log('Data:', data)
        });
}

function addCookieItem(productID, action){
  console.log('User is not authenticated....')

  if(action == "add"){
    if (cart['productID'] == undefined){
      cart['productID'] = {'quantity': 1}
    }else{
      cart['productID']['quantity'] +=1
    }
  }

  if(action == "remove"){

    cart['productID']['quantity'] -=1

  
    if (cart['productID'] <= 0){
        delete cart['productID'] 
      
      }
    }
    
    console.log("cart======", cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
  }