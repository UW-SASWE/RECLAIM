document.addEventListener("DOMContentLoaded", function() {
    var footerDiv = document.createElement('div');
    footerDiv.innerHTML = `{{ footer_custom }}`;
    document.body.appendChild(footerDiv);
});