function showPopup(url) {
    var width = 600;
    var height = 400;
    var left = (screen.width - width) / 2;
    var top = (screen.height - height) / 2;
    window.open(url, 'popupWindow', 'width=' + width + ', height=' + height + ', left=' + left + ', top=' + top + ', resizable=yes');
    return false;
}
