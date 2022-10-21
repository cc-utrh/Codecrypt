/* Declaración de funciones existentes en el archivo
de python (app.py) */

function select_file_py() {
    eel.select_file_py();
}

/* Declaración de funciones que podrán llamarse desde
el archivo de de python (app.py) */

eel.expose(go_to)
function go_to(url) {
    window.location.href =url;
}

eel.expose(go_logout)
function go_logout(url) {
    window.location.href =url;
}

/* Esta función se encarga de cambiar el valor del input filepath
por el filepath pasado por parámetro, además de mostrar el nombre
del archivo seleccionado */

eel.expose(select_file_js);

function select_file_js(filePath) {
    if (filePath !== null && filePath !== "") {
        document.getElementById("filepath").value = filePath;
        document.getElementById("selected-file").innerHTML = "Archivo seleccionado: " + filePath.split("/").slice(-1)
    }
}

/* Mostrar mensaje de error después del título del formulario
pasado por parámetro. */

function showFormError(errorMessage, formElement) {

    /* Eliminamos el mensaje de error del formulario */
    hideFormError(formElement);

    errorElement = document.createElement("div");
    errorElement.classList.add("error-message");
    errorElement.innerHTML = errorMessage;
    insertAfter(errorElement, formElement.firstElementChild);

}

/* Eliminar todos los mensajes de error de la página actual. */

function hideFormError(formElement) {

    errorMessages = formElement.getElementsByClassName("error-message");

    for (let i = 0; i < errorMessages.length; i++) {
        errorMessages[i].remove();
    }

}

/* Insertar elemento después de otro. */

function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

/* Validar formulario para añadir un nuevo archivo encriptado.
Este devuelve true en caso de ejecutarse correctamente y false
en caso de haber algún error de validación. */

function validate(formElement) {

    let formData = new FormData(formElement);
    if (formData.get("filepath") === null || formData.get("filepath") === "") {
        showFormError("No se ha seleccionado ningún archivo.", formElement);
        return false;
    } else {
        hideFormError(formElement);
        eel.preEncrypt(sessionStorage.getItem('user'), sessionStorage.getItem('password'));
        return true;
    }

}

async function validate_login(formElement) {

    let formData = new FormData(formElement);
    let aux_bool;
    if (formData.get("user") === "") {
        showFormError("El usuario no puede quedar en blanco.", formElement);
        return false;
    }else if (formData.get("password") === "") {
        showFormError("La contraseña no puede quedar en blanco.", formElement);
        return false;
    } else {
        //hideFormError(formElement);
        aux_bool = await eel.check_log_py(formData.get("user"),formData.get("password"))();
        if(aux_bool == true){
            sessionStorage.setItem('user', formData.get("user"));
            sessionStorage.setItem('password', formData.get("password"));
            //window.location.href = "index.html";
            eel.auxbool();
            //return true;
        }
        else if(aux_bool == formData.get("user")){
            alert("Usuario creado correctamente. Debe iniciar sesión");
            return false;
        }else{
            alert("La contraseña es incorrecta.");
            return false;
        }
        
    }
    return false;
}

async function cerrarSesion(){
    sessionStorage.removeItem('user');
    sessionStorage.removeItem('password');
    eel.auxlogout();
}

/* Esta función se encarga de mostrar la lista de
archivos encriptados */

async function showEncryptedFilesList() {

    let encryptedFilesListArray = await eel.get_encrypted_files_list(sessionStorage.getItem('user'))();
    let encryptedSharedListArray = await eel.get_shared_files_list(sessionStorage.getItem('user'))();

    let encryptedFilesListElement = document.getElementById("encrypted-files");
    let encryptedSharedListElement = document.getElementById("shared-files");

    encryptedFilesListArray.forEach(encryptedFile => {
        console.log(encryptedFile)
        let encryptedFileElement = document.createElement("div");
        encryptedFileElement.classList.add("item");

        let fileNameElement = document.createElement("div");
        fileNameElement.classList.add("name");
        fileNameElement.innerHTML = encryptedFile.name;
        encryptedFileElement.append(fileNameElement);

        let buttonsElement = document.createElement("div");
        buttonsElement.classList.add("buttons");

        let downloadButtonElement = document.createElement("div");
        downloadButtonElement.classList.add("download");
        downloadButtonElement.setAttribute("onclick", "download(" + encryptedFile.id + ")");
        downloadButtonElement.innerHTML = "Desencriptar";
        buttonsElement.append(downloadButtonElement);

        let removeButtonElement = document.createElement("div");
        removeButtonElement.classList.add("remove");
        removeButtonElement.setAttribute("onclick", "remove(" + encryptedFile.id + ")");
        removeButtonElement.innerHTML = "Eliminar";
        buttonsElement.append(removeButtonElement);

        let shareButtonElement = document.createElement("div");
        shareButtonElement.classList.add("share");
        shareButtonElement.setAttribute("onclick", "share(" + encryptedFile.id + ")");
        shareButtonElement.innerHTML = "Compartir";
        buttonsElement.append(shareButtonElement);

        encryptedFileElement.append(buttonsElement);

        encryptedFilesListElement.append(encryptedFileElement);

    });

    encryptedSharedListArray.forEach(encryptedFile => {
        console.log(encryptedFile)
        let encryptedFileElement = document.createElement("div");
        encryptedFileElement.classList.add("item");

        let fileNameElement = document.createElement("div");
        fileNameElement.classList.add("name");
        fileNameElement.innerHTML = encryptedFile.name;
        encryptedFileElement.append(fileNameElement);

        let buttonsElement = document.createElement("div");
        buttonsElement.classList.add("buttons");

        let downloadSharedButtonElement = document.createElement("div");
        downloadSharedButtonElement.classList.add("download-share");
        downloadSharedButtonElement.setAttribute("onclick", "downloadShared(" + encryptedFile.id + ")");
        downloadSharedButtonElement.innerHTML = "Desencriptar";
        buttonsElement.append(downloadSharedButtonElement);

        let removeButtonElement = document.createElement("div");
        removeButtonElement.classList.add("remove");
        removeButtonElement.setAttribute("onclick", "remove(" + encryptedFile.id + ")");
        removeButtonElement.innerHTML = "Eliminar";
        buttonsElement.append(removeButtonElement);

        let shareButtonElement = document.createElement("div");
        shareButtonElement.classList.add("share");
        shareButtonElement.setAttribute("onclick", "share(" + encryptedFile.id + ")");
        shareButtonElement.innerHTML = "Compartir";
        buttonsElement.append(shareButtonElement);

        encryptedFileElement.append(buttonsElement);

        encryptedSharedListElement.append(encryptedFileElement);

    });



}

/** Función que muestra el formulario para introducir los
 * datos de validación para descargar o eliminar un archivo. */

function showValidateForm(elementId) {
    document.getElementById(elementId).style.display = "flex";
}

function download(id) {
    showValidateForm("download-form");
    downloadId = id;
}

function validateDownload(formElement){
    formData = new FormData(formElement);
    formData.get("password");
    if (formData.get("password") === "") {
        showFormError("La contraseña no puede quedar en blanco.", formElement);
        return false;
    } else {
        hideFormError(formElement);
        eel.preDecrypt(downloadId, sessionStorage.getItem('user'), formData.get("password"));
        return true;
    }
}

function downloadShared(id) {
    showValidateForm("download-shared-form");
    downloadSharedId = id;
}

function validateDownloadShared(formElement){
    formData = new FormData(formElement);
    formData.get("password");
    if (formData.get("password") === "") {
        showFormError("La contraseña no puede quedar en blanco.", formElement);
        return false;
    } else {
        hideFormError(formElement);
        eel.preDecryptShared(downloadSharedId, sessionStorage.getItem('user'), formData.get("password"));
        return true;
    }
}

function remove(id) {
    showValidateForm("remove-form");
    removeId = id;
}

async function validateRemove(formElement){
    let formData = new FormData(formElement);
    formData.get("password");
    if (formData.get("password") === "") {
        alert("La contraseña no puede quedar en blanco.")
        showFormError("La contraseña no puede quedar en blanco.", formElement);
        return false;
    } else {
        hideFormError(formElement);
        let result = await eel.eliminarFila(removeId, sessionStorage.getItem('user'), formData.get("password"))();
        if(result === true){
            
            return true;
        }
        else{
            alert("La contraseña es incorrecta.")
            return false;
        }
    }
}


//Funcion para compartir

function share(id) {
    showValidateForm("share-form");
    shareId = id;
}


function validateShare(formElement){    
    let formData = new FormData(formElement);
    formData.get("password");
    if (formData.get("password") === "") {
        showFormError("La contraseña no puede quedar en blanco.", formElement);
        return false;
    }else if(formData.get("shared")===""){
        showFormError("El usuario no puede estar vacío", formElement)
        return false;
    } else {
        // shared_user = await eel.getSharedUser(formData.get("shared"))();
        shared_user = eel.getSharedUser(formData.get("shared"));
        if(shared_user == false){
            alert("El usuario al que quieres compartir no existe");
            return false;
        }else{
            hideFormError(formElement);
            eel.Share(shareId, sessionStorage.getItem('user'), formData.get("shared") ,formData.get("password"));
            return true;
        }
    }
}


function setTitle(){
    let html = `Hola ` + sessionStorage.getItem('user');
    let aux = document.querySelector('.user-title')
    aux.innerText = html;
}

window.onload = function() {
    showEncryptedFilesList();
    setTitle();
};

let downloadId = null
let downloadSharedId = null
let removeId = null
let shareId = null