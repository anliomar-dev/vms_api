const baseUrl = 'http://127.0.0.1:8000';

async function resetPassword(newPassword, uid, token) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/vms/auth/users/reset_password_confirm/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                uid: uid,
                token: token,
                new_password: newPassword
            }),
        });

        // Si la réponse a un statut 400 (Bad Request)
        if (response.status === 400) {
            // Attends la résolution du JSON
            const errorData = await response.json();

            // Vérifie si le message d'erreur est lié au token ou au uid
            if (errorData.token) {
                return {
                    detail: "The password reset link has either expired or is invalid. " +
                        "send your emails address again to receive a new reset link.",
                    http_status: response.status
                };
            } else if (errorData.uid) {
                return { detail: errorData.uid, http_status: response.status };
            } else {
                return { detail: errorData.new_password, http_status: response.status };
            }
        }

        // Si la réponse est OK, retourne simplement le statut
        return {no_content: response.status};

    } catch (err) {
        alert("Something went wrong, Failed to reset password. Please try again later.");
        console.error(err);
    }
}


document.addEventListener("DOMContentLoaded", ()=>{
    const resetPwdForm = document.getElementById("reset-pwd-form")
    const passwordField = document.getElementById("password")
    const confirmPasswordField = document.getElementById("confirm-password")
    const togglePasswordIcons = document.querySelectorAll("span");

    togglePasswordIcons.forEach(icon => {
        icon.addEventListener("click", (e) => {
            togglePasswordIcons.forEach((el) => {
                el.classList.toggle("d-none");
            });
            [passwordField, confirmPasswordField].forEach((input) => {
                input.type === "password" ? input.setAttribute("type", "text") :
                    input.setAttribute("type", "password");
            })
        })
    })

    resetPwdForm.addEventListener("submit", async(event)=>{
        event.preventDefault()
        const isPasswordValid = validatePassword(passwordField.value, confirmPasswordField.value)
        if (!isPasswordValid) {
            return
        }
        const uid = document.getElementById("uid").value;
        const token = document.getElementById("token").value;

        const resetPwd = await resetPassword(passwordField.value.trim(), uid, token);
        if (resetPwd.detail) {
            alert(resetPwd.detail);
        }else if(resetPwd.no_content === 204){
            console.log(resetPwd.no_content);
            window.location.replace(`${baseUrl}/vms/auth/reset_password_success`);
        }else{
            alert("Sorry something went wrong, please try again later.");
        }
        [passwordField, confirmPasswordField].forEach((input) => {input.value = ""})
    })

})

/**
 * Verifies the validity of the password by checking if both passwords match,
 * and if both passwords meet the criteria:
 * at least 8 characters, including at least 1 uppercase letter, 1 lowercase letter,
 * 1 digit, and 1 special character.
 * Returns true if both passwords match and meet the criteria, false otherwise.
 * @param password {string}
 * @param passwordConfirm {string}
 * @returns {boolean}
 */
function validatePassword(password, passwordConfirm) {
    const regExPwd = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!regExPwd.test(password.trim())) {
        alert(
            "Password must be at least 8 characters long, including at least " +
            "1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character( @ $ ! % * ? & )"
        );
        return false;
    }
    if (password.trim() !== passwordConfirm.trim()) {
        alert("Sorry, Passwords don't match!")
        return false;
    }
    return true;
}