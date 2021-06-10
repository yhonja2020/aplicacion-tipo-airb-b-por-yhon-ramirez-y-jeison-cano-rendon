function validateformlogin() {
    let email = document.getElementById("loginemail").value;
    let password = document.getElementById("loginpassword").value;

    let expr = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    // console.log(password);
    if (email === "" || password === "") {

        alert("Todos los campos deben de estar llenos");
        return false;
    }
    else
        if (!expr.test(email)) {                                                            //COMPRUEBA MAIL
            alert("Error: La dirección de correo " + email + " no tiene el formato correcto.");
            return false;

        }
        else
            if (!containsNumber(password)) {
                alert("La contraseña no tiene el formato ")
                return false;
            }
    return true;
}



function containsNumber(data) {
    var hasNumber = /\d/;
    // console.log(hasNumber.test(data)); 
    return hasNumber.test(data);

}

//para ver si hay un numero 
// function ifThereANumber(data){
//     let number = [0,1,2,3,4,5,6,7,8,9]
//     findNumber = false;
//     for(let i=0; i<SVGAnimatedNumberList.length;i++){
//         for(let j=0; j<data.length; j++){
//             if(data[j]==number[i]){
//                 findNumber = true;
//                 break;

//             }
//         }
// if(findNumber){
//     break;
// }

//     }
//return findNumber;
// }

function validateformlrecord() {
    let name = document.getElementById("recordname").value;
    let email = document.getElementById("recordemail").value;
    let country = document.getElementById("recordcountry").value;
    let city = document.getElementById("recordcity").value;
    let password = document.getElementById("recordpassword").value;
    let rol = document.getElementById("recordrol").value;

    let expr = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    // console.log(password);
    if (name === "" || email === "" || country === "" || city === "" || password === "" || rol === "") {

        alert("Todos los campos deben de estar llenos");
        return false;
    }
    else
        if (!expr.test(email)) {                                                            //COMPRUEBA MAIL
            alert("Error: La dirección de correo " + email + " no tiene el formato correcto.");
            return false;

        }
        else
            if (!containsNumber(password)) {
                alert("La contraseña no tiene el formato DEBE DE CONTENER ALMENOS UN NUMERO ")
                return false;
            }
    return true;
}








