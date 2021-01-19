// selectores de Instructor o Estudiante
const selector_profesor = document.getElementById("selector_profesor");
const selector_estudiante = document.getElementById("selector_estudiante");

// inputs que se colocan en hidden provenientes del backend
const profesor_input = document.getElementById("is_instructor");
const profesor_input = document.getElementById("is_student");

function in_list(list, element){
    // solo sirve para saber si se encuentra un solo tipo de elemento en una lista
    for(var i=0;i<list.length();i++){
        if(element === list[i]){
            return true;
        }
    }
}

if (selector_profesor &&  selector_estudiante){
    if (in_list(selector_profesor.classList, "active-btn")){
        
    }else{

    }
}