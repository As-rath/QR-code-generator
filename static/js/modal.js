function handleGenerate(){
    const form = document.querySelector("form");
    const formData = new FormData(form);

    fetch("/generate", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.qr_url){
            openModal(data.qr_url);
        }
        else{
            alert("Failed to generate QR.");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Something went wrong.");
    });
}

function openModal(qrURL){
    const modal = document.getElementById("previewModal");
    const img = document.getElementById("qrPreview");
    const downloadBtn = document.getElementById("downloadBtn");

    img.src = qrURL;
    downloadBtn.href = qrURL;

    modal.classList.remove("hidden");
}

function closeModal(){
    document.getElementById("previewModal").classList.add("hidden");
}

function shareQR(){
    const img = document.getElementById("qrPreview").src;

    if (navigator.share){
        navigator.share({
            title: "My QR Code",
            text: "Here is my QR code.",
            url: img
        });
    }
    else{
        alert("Sharing not supported on this device.")
    }
}