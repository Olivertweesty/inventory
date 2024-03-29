$('[id=alertsDropdown]').hide();

var userid;
    if(location.search.split('=')[1] == undefined){
      if (sessionStorage.getItem("userid") === null) {
        window.location = window.location.protocol+"//"+window.location.hostname+":4000"
      }else{
        userid = sessionStorage.getItem("userid");
      }
    }else{
      userid = location.search.split('=')[1];
      sessionStorage.setItem("userid",userid)
    }
  

  ajaxObj = $.ajax({ 
        url: window.location.protocol+"//"+window.location.hostname+":4000/getuserrights/"+userid,
        type: "POST",
        contentType: "application/json",  
        success: function(result){
          var access_rights = (result[0]['access_rights'].split(','))
          for(var i = 0; i<access_rights.length;i++){
            if (access_rights[i] == "warehouse") {
              $('[aria-labelledby=userDropdown]').prepend('<a class="dropdown-item" href="warehouse"><i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>WareHouse</a>');
            }else if(access_rights[i] == "admin"){
              $("[aria-labelledby=userDropdown]").prepend('<a class="dropdown-item" href="management"><i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>Management</a>');
            }else if(access_rights[i] == "humanresource"){
              $("[aria-labelledby=userDropdown]").prepend('<a class="dropdown-item" href="humanresource"><i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>Human Resource</a>');
            }else if(access_rights[i] == "pointofsale"){
              $("[aria-labelledby=userDropdown]").prepend('<a class="dropdown-item" href="pointofsale"><i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>Point Of Sale</a>');
            }else if(access_rights[i] == "accounting"){
              $("[aria-labelledby=userDropdown]").prepend('<a class="dropdown-item" href="account"><i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>Finance</a>');
            }
          }

        } 
  });
var myswal;
function loading(boxTitle){
  $(document).ready(function(){       
        
      myswal = Swal.fire({
         title : boxTitle,
         text : 'Please Wait ...',
         imageUrl : 'static/img/loading.gif',
         showConfirmButton : false,
         allowOutsideClick : false
        });
    });
}

function showError(boxTitle,boxMessage){
  $(document).ready(function(){
    Swal.fire({        
               type: 'error',
               title: boxTitle,
               text: boxMessage,
               showConfirmButton: true
        });
  });
    
}

function closeLoading(){
  myswal.close()
}