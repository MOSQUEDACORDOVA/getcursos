// selectores de Instructor o Estudiante
var selector_profesor = document.getElementById("selector_profesor");
var selector_estudiante = document.getElementById("selector_estudiante");

// inputs que se colocan en hidden provenientes del backend
var profesor_input = document.getElementById("id_is_instructor");
var estudiante_input = document.getElementById("id_is_student");

function in_list(list, element){
    // solo sirve para saber si se encuentra un solo tipo de elemento en una lista
    for(var i=0;i<list.length;i++){
        if(element === list[i]){
            return true;
        }
    }
}

function set_checkboxes_values(){
        console.log("clickeado");
    
        if (in_list(selector_profesor.classList, "active-btn")){
            profesor_input.checked = true;
            estudiante_input.checked = false;
        }else{
            profesor_input.checked = false;
            estudiante_input.checked = true;
            
        }
        console.log("profesor input  " +  profesor_input.checked +"\nestudiante input  "+estudiante_input.checked)
    
}


if (selector_profesor &&  selector_estudiante){
    document.getElementById("selector_profesor").addEventListener("click", set_checkboxes_values);
    document.getElementById("selector_estudiante").addEventListener("click", set_checkboxes_values);
}