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
        token: "71198f64877251cba46a2a88ab061f4a4369298a",
        type: "ADDRESS",
        /* Вызывается, когда пользователь выбирает одну из подсказок */
        onSelect: function(suggestion) {
            console.log(suggestion);
        }
    });

$("#email").suggestions({
        token: "71198f64877251cba46a2a88ab061f4a4369298a",
        type: "EMAIL",
        /* Вызывается, когда пользователь выбирает одну из подсказок */
        onSelect: function(suggestion) {
            console.log(suggestion);
        }
    });