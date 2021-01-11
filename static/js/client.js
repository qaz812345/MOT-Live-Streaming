
function fetch_from_server(){
    var req = new XMLHttpRequest();
    req.open('GET', '/api/test');
    req.onreadystatechange = function () {
      if (req.readyState === 4) {
        //console.log(JSON.parse(req.responseText));
        process_data(req.responseText);
      }
    };
    req.send();
}

function process_data(v){
    document.getElementById('data').innerHTML = v;
    selectArray = JSON.parse(v)
    var selectBox = document.getElementById('tracking_id');
    var index = selectBox.selectedIndex;
    selectBox.options.length = 0;
    for(var i = 0; i < selectArray.length; i++){
        selectBox.options.add(new Option(selectArray[i], selectArray[i]));
    }
    
}

function repeatedly_get(){
    fetch_from_server();
    setTimeout(repeatedly_get, 5000);
}

function track_start(){
    var req = new XMLHttpRequest();
    req.open('GET', '/api/track');
    console.log("track_start")
    req.send();
}

/////////////////main//////////////////
$(document).ready(function(){  
    
    //track_start();
    repeatedly_get();
    
    var selectBox = document.getElementById('tracking_id');
    document.getElementById('select_id').onclick = function () {
        console.log(selectBox.value);
    }

    $('#select_id').click(function(){
        var select_id = {
            "id" : selectBox.value
        }
        $.ajax({
            type: 'POST',
            url:"http://127.0.0.1:5000/get_select_id",
            headers: {'Access-Control-Allow-Origin': '*'},
            data:JSON.stringify(select_id)
        }).done(function(responce){
            alert(responce);
        });
    })

})