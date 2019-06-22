document.addEventListener("DOMContentLoaded", () => {
    let state = {
        sol: "0",
        camera: "",
        page: 1
    };

    let searchForm = document.querySelector("#search_form");
    let solInput = document.querySelector("#sol_input");
    let cameraInput = document.querySelector("#camera_input");
    solInput.setAttribute("value", state.sol);
    searchForm.addEventListener("submit", handleFormSubmit.bind(null, state));
    solInput.addEventListener("change", handleSolInputChange.bind(null, state));
    cameraInput.addEventListener("change", handleCameraInputChange.bind(null, state));
    renderLoadMore();


    function handleSolInputChange(state, event){
        state.sol = event.target.value;
    }

    function handleCameraInputChange(state, event){
        state.camera = event.target.value;
    }

    function handleFormSubmit(state, event){
        console.log(event);
        event.preventDefault();
        let errors = validateInput();
        if (errors.length === 0){
            initialize();
            getPhotos();
        } else {
            renderErrors(errors);
        }
    }

    function initialize(){
        document.querySelector("#photos").innerHTML = "";
        document.querySelector("#errors").innerHTML = "";
        state.page = 1;
        hideLoadMore();
    }

    function getPhotos(){
        let queryString = `sol=${encodeURIComponent(state.sol)}`;
        queryString += `&camera=${encodeURIComponent(state.camera)}`;
        queryString += `&page=${encodeURIComponent(state.page)}`;
        let request = new Request("/api/photos?" + queryString);
        renderStatus("Loading Images");
        fetch(request)
            .then(response => {
                if (response.status === 408) {
                    renderStatus("API Timed Out");
                } else if (response.status === 200){
                    return response.json()
                }
            }).then(handleGetPhotosJson)
    }


    function handleGetPhotosJson(json){
        if (json == null){
        } else if (json.length === 0){
            hideLoadMore();
            renderStatus("No Photos Found");
        } else {
            renderPhotoPage(json);
        }
    }

    function showLoadMore(){
        let loadMore = document.querySelector("#load_more");
        loadMore.style.display = "block";
    }


    function hideLoadMore(){
        let loadMore = document.querySelector("#load_more");
        loadMore.style.display = "none";
    }

    function renderLoadMore(){
        let loadMore = document.querySelector("#load_more");
        let loadMoreBtn = document.createElement("button");
        loadMoreBtn.textContent = "Load More";
        loadMoreBtn.classList.add("load_more_btn");
        loadMoreBtn.addEventListener("click", () => {
           state.page++;
           getPhotos();
        });
        loadMore.appendChild(loadMoreBtn);
    }

    function renderPhotoPage(photos){
        let photoContainer = document.querySelector("#photos");
        let messages = document.querySelector("#status");
        messages.innerHTML= "";
        photos.forEach((photo) => {
            photoContainer.appendChild(createPhotoElement(photo.src));
        });
        if (photos.length < 25) {
            hideLoadMore();
        } else {
            showLoadMore();
        }
    }

    function createPhotoElement(src){
        let element = document.createElement("img");
        element.setAttribute("class", "photo");
        element.setAttribute("src", src);
        element.setAttribute("alt", "Mars Photo");
        return element;
    }

    function createMessageElement(text){
        let message = document.createElement("P");
        message.textContent = text;
        return message;
    }

    function renderStatus(text){
        let messages = document.querySelector("#status");
        messages.innerHTML = "";
        messages.appendChild(createMessageElement(text));
    }

    function validateInput(){
        let errors = [];
        if (state.sol === ""){
            errors.push("Sol is required");
        }
        return errors;
    }

    function renderErrors(errors){
        let errorsElement = document.querySelector("#errors");
        errorsElement.innerHTML = "";
        errors.forEach((error) => {
            let errorElement = document.createElement("P");
            errorElement.style.color = "red";
            errorElement.textContent = error;
            errorsElement.appendChild(errorElement);
        });
    }
});