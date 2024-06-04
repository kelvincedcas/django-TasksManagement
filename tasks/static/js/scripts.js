const close_sidebar = document.getElementById("close_sidebar");
const sidebar = document.getElementById("sidebar");
const main = document.getElementById("main");
const open_sidebar = document.getElementById("open_sidebar");
const div_separador = document.getElementById("div_separador");
const modal_task = document.getElementById("modal_task")
const button_back = document.getElementById("button_back")
const delete_modal = document.getElementById("delete_modal")

close_sidebar.addEventListener(("click"),()=>{
    sidebar.classList.add("hidden")
    sidebar.classList.remove("sm:flex")
    main.classList.remove("sm:ml-60")
    open_sidebar.classList.add("fixed")
    open_sidebar.classList.remove("sm:hidden")
    div_separador.classList.add("mb-12")
});


open_sidebar.addEventListener(("click"),()=>{
    sidebar.classList.remove("hidden")
    main.classList.add("sm:ml-60")
    open_sidebar.classList.remove("fixed")
    open_sidebar.classList.add("sm:hidden")
    div_separador.classList.remove("mb-12")
});


function open_modal(){
    modal_task.classList.add("flex")
    modal_task.classList.remove("hidden")
}

function open_delete_modal(){
    delete_modal.classList.add("flex")
    delete_modal.classList.remove("hidden")
}


function close_delete_modal(){
    delete_modal.classList.add("hidden")
    delete_modal.classList.remove("flex")
}

button_back.addEventListener(("click"),()=>{
    modal_task.classList.add("hidden")
    modal_task.classList.remove("flex")
})