pet_type_select = document.getElementById('pet_type');
breed_select = document.getElementById('breed');
       
pet_type_select.onchange = function(){
    pet_type = pet_type_select.value;
    fetch('breed/' + pet_type).then(function(response){
        response.json().then(function(data){
            optionHTML = '';
            for (breed of data.breedbytype){
                optionHTML += '<option value="' + breed.id +'">' + breed.name + '</option>'
            }
            breed_select.innerHTML = optionHTML;
        })
    })
}

function deletePost(postId) {
    fetch("/delete-post", {
      method: "POST",
      body: JSON.stringify({ postId: postId }),
    }).then((_res) => {
      window.location.href = "/home";
    });
  }
