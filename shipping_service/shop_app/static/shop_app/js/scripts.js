const buttonPlus = document.querySelector('#plus');
const buttonMinus = document.querySelector('#minus');
const hiddenField = document.querySelector('#myHidden');
const output = document.querySelector('#output');

if (buttonPlus) {
  buttonPlus.addEventListener('click', () => {
    if (hiddenField && output && hiddenField.value < 20) {
      hiddenField.value = parseInt(hiddenField.value) + 1;
      output.textContent = hiddenField.value;
    }
  });
}

if (buttonMinus) {
  buttonMinus.addEventListener('click', () => {
    if (hiddenField && output && hiddenField.value > 1) {
      hiddenField.value = parseInt(hiddenField.value) - 1;
      output.textContent = hiddenField.value;
    }
  });
}

$("#address").suggestions({
    token: "{{TOKEN_ID_DADATA}}",
    type: "ADDRESS",
    onSelect: function(suggestion) {
        localStorage.setItem("selectedAddress", JSON.stringify(suggestion));
    }
});

$("#email").suggestions({
    token: "{{TOKEN_ID_DADATA}}",
    type: "EMAIL",
    onSelect: function(suggestion) {
        localStorage.setItem("selectedEmail", JSON.stringify(suggestion));
    }
});

// Заполняем поля при обновлении страницы
$(document).ready(function() {
    var selectedAddress = localStorage.getItem("selectedAddress");
    var selectedEmail = localStorage.getItem("selectedEmail");

    if (selectedAddress) {
        $("#address").val(JSON.parse(selectedAddress).value);
    }

    if (selectedEmail) {
        $("#email").val(JSON.parse(selectedEmail).value);
    }
});

