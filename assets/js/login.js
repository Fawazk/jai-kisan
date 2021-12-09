$(document).ready(()=>{
    $("#login").validate({
        rules:{
            username:{
                required:true,
                minlength:4,
            },
            password:{
                required:true,
                minlength:8,
            },   

        }
        })
    })