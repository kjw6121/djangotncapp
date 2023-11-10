// custom.js

document.addEventListener("DOMContentLoaded", function () {
    const qrDataList = document.getElementById("qr-data-list");
    let isFirstScan = true;

    const html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", 
        { 
            fps: 10,
            qrbox: 250,
            useBarCodeDetectorIfSupported: true,
            rememberLastUsedCamera: true,
            showTorchButtonIfSupported: true,
            showZoomSliderIfSupported: true,
            defaultZoomValueIfSupported: 2
        }
    );

    html5QrcodeScanner.render(onScanSuccess);

    function onScanSuccess(qrCodeMessage) {
        addToQRDataList(qrCodeMessage);

        // Django 템플릿 태그를 사용하여 현재 로그인한 사용자명 가져오기
        const currentUsername = "{% if user.is_authenticated %}{{ user.username }}{% else %}Guest{% endif %}";

        // JavaScript를 사용하여 현재 시간 가져오기
        const currentTime = new Date().toLocaleString();

        // 스캔 데이터에 사용자명과 시간 추가
        const scannedData = `${currentUsername} - ${currentTime} - ${qrCodeMessage}`;

        if (isFirstScan) {
            // 첫 번째 스캔에서는 "문제없습니다. 다음 QR을 스캔하세요." 메시지만 표시
            displaySuccessMessage();
            isFirstScan = false;
        } else {
            // 이후 스캔에서는 이전 스캔된 값과 현재 스캔된 값 비교 후 처리
            if (previousQRCode !== null && previousQRCode === scannedData) {
                displaySuccessMessage();
            } else {
                // 값이 다를 경우 error.html로 리다이렉션
                window.location.href = "{% url 'error_page' %}";
            }
        }

        previousQRCode = scannedData;
    }

    function addToQRDataList(data) {
        const listItem = document.createElement("li");
        listItem.textContent = data;
        qrDataList.appendChild(listItem);
    }

    function displaySuccessMessage() {
        alert("문제없습니다. 다음 QR을 스캔하세요.");
    }
});
