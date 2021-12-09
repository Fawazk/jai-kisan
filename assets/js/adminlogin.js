$(document).ready(()=>{
    $("#login").validate({
        rules:{
            username:{
            required:true,
        },
            password:{
                required:true,
                minlength:8,
            },   

        }
        })
    })