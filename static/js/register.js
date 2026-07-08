function togglePassword(id, button){

    const input = document.getElementById(id);

    if(input.type==="password"){

        input.type="text";

        button.innerHTML="🙈";

    }

    else{

        input.type="password";

        button.innerHTML="👁";

    }

}