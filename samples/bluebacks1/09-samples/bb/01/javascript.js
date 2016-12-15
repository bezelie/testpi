function initialize_webiopi(){
    // webiopiの準備が終わってからstyles.cssを適用する
    applyCustomCss('styles.css');

    // GPIOの状態を監視しない
    webiopi().refreshGPIO(false);
}

function toggleLED(gpio){
    // responseにトグル後のGPIOの状態(True/False)が格納されている
    var changeButtonColor = function(macro, args, response){
        if(response){
            document.getElementById("gpio"+gpio).className = "HIGH";
        }else{
            document.getElementById("gpio"+gpio).className = "LOW";
        }
    }

    // script.py内のtoggleLED関数を実行。引数はGPIO番号。終了後にchangeButtonColor関数を呼ぶ
    webiopi().callMacro("toggleLED", [gpio], changeButtonColor);
}

function applyCustomCss(custom_css){
    var head = document.getElementsByTagName('head')[0];
    var style = document.createElement('link');
    style.rel = "stylesheet";
    style.type = 'text/css';
    style.href = custom_css;
    head.appendChild(style);
}

