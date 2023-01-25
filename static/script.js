
fetch("http://127.0.0.1:5000/useritems", {
    method: "GET",
    headers : {"Authorization" : `Bearer ${window.localStorage.token}`}
})
.then(r => r.json())
.then(res => {
    var tbody = document.getElementById("quest-items-tbody");
    var namespan = document.querySelector(".name")
    useritems = JSON.parse(res[0])
    console.log(useritems)
    data = res[1]
    namespan.innerHTML = res[2]
    for (var i = 0; i < data.length; i++) {
        var tr = document.createElement("tr");
        tr.id = "tr-"+i
        var itemNameTd = document.createElement("td");
        itemNameTd.innerHTML = data[i].itemName;
        tr.appendChild(itemNameTd);

        var neededContTd = document.createElement("td");
        neededContTd.id = "needed-"+i
        neededContTd.innerHTML = data[i].neededCont;
        tr.appendChild(neededContTd);

        var questNamesTd = document.createElement("td");
        questNamesTd.innerHTML = data[i].questNames;
        tr.appendChild(questNamesTd);

        var imageTd = document.createElement("td");
        var image = data[i].image;
        if (image != "") {
            var img = document.createElement("img");
            img.className = "orangeItem"
            img.src = image;
            img.style.width = "50px";
            imageTd.appendChild(img);
        }
        tr.appendChild(imageTd);

        var collectedTd = document.createElement("td")

        var decrementButton = document.createElement("button");
        decrementButton.innerHTML = "-";
        decrementButton.id = "collected-button-minus-"+i
        
        decrementButton.className = "collected-button"

        var collectedNumber = document.createElement("span");
        collectedNumber.innerHTML = useritems[data[i].itemName];
        collectedNumber.id = "collected-number-"+i
        collectedNumber.className = "collected-number"
        collectedNumber.dataset.itemName= data[i].itemName

        var incrementButton = document.createElement("button");
        incrementButton.innerHTML = "+";
        incrementButton.id = "collected-button-plus-"+i
        incrementButton.className = "collected-button"

        incrementButton.addEventListener("click", function(){
            var cl = this.id 
            const arr = cl.split("-");
            var number = document.getElementById("collected-number-"+arr[3])
            var itemName = number.dataset.itemName
            var currentValue = parseInt(number.innerHTML)
            var updatedValue = currentValue + 1
            number.innerHTML = updatedValue;


            useritems[itemName] = updatedValue

            let jsonData = JSON.stringify(useritems);
            fetch('http://127.0.0.1:5000/updateitems', {
                method: 'POST',
                headers : { 
                    'Content-Type': 'application/json', 
                    'Authorization' : `Bearer ${window.localStorage.token}`,
                },
                body: jsonData
            })
                
        })


        collectedNumber.addEventListener('DOMSubtreeModified', function(){
            var cl = this.id 
            const arr = cl.split("-");
            var btn = document.getElementById("collected-button-minus-"+arr[2])
            var currentValue = parseInt(this.innerHTML)
        
            objectiveNumber = parseInt(document.getElementById("needed-"+arr[2]).innerHTML)
            objectiveTr = document.getElementById("tr-"+arr[2])
            if(currentValue >= objectiveNumber){
                if(!objectiveTr.classList.contains('crossed-out')){
                    objectiveTr.classList.toggle('crossed-out');
                }
            }else{
                if(objectiveTr.classList.contains('crossed-out')){
                    objectiveTr.classList.toggle('crossed-out');
                }
                    
            }
        })

        decrementButton.addEventListener("click", function(){
            var cl = this.id 
            const arr = cl.split("-");
            var number = document.getElementById("collected-number-"+arr[3])
            var currentValue = parseInt(number.innerHTML)
            if(currentValue >0){
                number.innerHTML = currentValue -1;
                }

        });

        collectedTd.appendChild(decrementButton);
        collectedTd.appendChild(collectedNumber)
        collectedTd.appendChild(incrementButton)
        tr.appendChild(collectedTd);

        if(parseInt(collectedNumber.innerHTML) >= parseInt(neededContTd.innerHTML)){
            if(!tr.classList.contains('crossed-out')){
                tr.classList.toggle('crossed-out');
            }
        }else{
            if(tr.classList.contains('crossed-out')){
                tr.classList.toggle('crossed-out');
            }    
        }

        tbody.appendChild(tr);

        
    }    
    })


function searchitems() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("quest-items-table");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }

}