function showLoader() {
    document.getElementById("preloader").style.display = "block";
}

function showWarningToasty(message) {
    Toastify({
        text: message,
        duration: 4000,
        close: true,
        backgroundColor: "#0000FF",
    }).showToast();
}

// Form Validation
function user_Form() {
    if (document.user_form.user_name.value === "") {
        showWarningToasty("User Name is Empty!");
        document.user_form.user_name.focus();
        return false;
    } else if (document.user_form.mobile_no.value === "") {
        showWarningToasty("Mobile No is Empty!");
        document.user_form.mobile_no.focus();
        return false;
    } else if (document.user_form.email.value === "") {
        showWarningToasty("Email Id is Empty!");
        document.user_form.email.focus();
        return false;
    } else if (document.user_form.password.value === "") {
        showWarningToasty("Password is Empty!");
        document.user_form.password.focus();
        return false;
    } else if (document.user_form.shop_name.value === "") {
        showWarningToasty("Shop Name is Empty!");
        document.user_form.shop_name.focus();
        return false;
    } else if (document.user_form.shop_id.value === "") {
        showWarningToasty("Shop Id is Empty!");
        document.user_form.shop_id.focus();
        return false;
    } else {
        showLoader();
    }
}

// Reset Form
function ClearFields() {
    document.getElementById("user_name").value = "";
    document.getElementById("mobile_no").value = "";
    document.getElementById("email").value = "";
    document.getElementById("password").value = "";
    document.getElementById("shop_name").value = "";
    document.getElementById("shop_id").value = "";
}

