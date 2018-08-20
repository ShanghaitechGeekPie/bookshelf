function success(data){
    authorlist = data.author;

    var authorNum = authorlist.length;

    all_author  = "";

    for (var i = 0; i < authorNum; i++) {

        all_author += authorlist[i];
        
        if (i + 1 < authorNum){
            all_author += ',';
        }
    }
    console.log(data);


    document.getElementById("id_BookName").value = data.title;
    document.getElementById("id_FrontPage").value = data.image;
    document.getElementById("id_Author").value = all_author;
    document.getElementById("id_Publisher").value = data.publisher;  
    document.getElementById("id_Introduction").innerHTML =  data.summary; 

}




function generateInfo(isbn){

    var geturl = "https://api.douban.com/v2/book/isbn/" + isbn.toString();
    $.ajax({
        url: geturl,
        async: false,
        type: "GET",
        dataType : "jsonp",
        success: function (data){
            success(data);
        }
    })
    
}

window.onkeyup = function(e){
   
    if (e.keyCode == 13){
        isbn = document.getElementById('id_ISBN').value;
        generateInfo(isbn);
    } 
}