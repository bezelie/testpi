// millisミリ秒ごとに温度を取得する関数
function getTempPeriodic(millis){
    // responseに温度が格納されている
    var drawTemp = function(macro, args, response){
        var temp = response;
        $("#temp_text").val(temp);
    }

    // script.py内のgetTemp関数を実行。終了後にdrawTemp関数を呼ぶ
    webiopi().callMacro("getTemp", [], drawTemp);

    // millisミリ秒後に自分自身を呼び出す
    setTimeout(function(){ getTempPeriodic(millis); }, millis);
}

function initialize_webiopi(){
    // webiopiの準備が終わってからstyles.cssを適用する
    applyCustomCss('styles.css');
    // 2秒ごとに温度を取得して描画
    getTempPeriodic(2000);

    // GPIOの状態を監視しない（自分で作成した関数で温度を定期的に取得するため）
    webiopi().refreshGPIO(false);
}

function applyCustomCss(custom_css){
    var head = document.getElementsByTagName('head')[0];
    var style = document.createElement('link');
    style.rel = "stylesheet";
    style.type = 'text/css';
    style.href = custom_css;
    head.appendChild(style);
}

