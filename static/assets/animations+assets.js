const akoSlider = document.getElementById("ako-range");
const gamesSlider = document.getElementById("games-range");
const outputDecimal = document.getElementById("val-decimal");
const outputInteger = document.getElementById("val-integer");
const lowRisk = document.getElementById("low-risk");
const normalRisk = document.getElementById("normal-risk");
const highRisk = document.getElementById("high-risk");
const button = document.getElementById('start-button');
const loader = document.getElementById('loader');

/*sliders*/
function updateAkoValue() {
    outputDecimal.textContent = (akoSlider.value / 10).toFixed(1);
}

function updateGamesValue() {
    outputInteger.textContent = gamesSlider.value;
}

akoSlider.addEventListener("input", updateAkoValue);
gamesSlider.addEventListener("input", updateGamesValue);

updateAkoValue();
updateGamesValue();

/*checkboxes*/
document
    .querySelectorAll("#league-container input[type='checkbox']")
    .forEach(checkbox => {
        checkbox.checked = true;
    });

normalRisk.checked = true;

lowRisk.addEventListener('change', function() {
    if(this.checked){
        highRisk.checked = false;
        normalRisk.checked = false;
    }
});
highRisk.addEventListener('change', function() {
    if(this.checked){
        lowRisk.checked = false;
        normalRisk.checked = false;
    }
});
normalRisk.addEventListener('change', function() {
    if(this.checked){
        highRisk.checked = false;
        lowRisk.checked = false;
    }
});

/*button*/
button.addEventListener('mouseenter', () => {
    button.classList.add('slide-fwd-center');
});

button.addEventListener('mouseleave', () => {
    button.classList.remove('slide-fwd-center');
});
