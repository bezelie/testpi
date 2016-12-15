// スライダの最小値、最大値、刻み幅、初期値
var sliderMin = 0;
var sliderMax = 20;
var sliderStep = 1;
var sliderValue = 0;

function initialize_webiopi(){
    // webiopiの準備が終わってからstyles.cssを適用する
    applyCustomCss('styles.css');

    // GPIOの状態を監視しない
    webiopi().refreshGPIO(false);
}

// jQuery UIによるスライダの設定
$(function() {
    // スライダを動かしたときに呼ばれるイベントハンドラの設定
    var sliderHandler1 = function(e, ui){
        var ratio = ui.value/sliderMax;
        // 共通カソードの場合次の行を無効に
        ratio = 1.0 - ratio;
        webiopi().pulseRatio(25, ratio);
    };
    var sliderHandler2 = function(e, ui){
        var ratio = ui.value/sliderMax;
        // 共通カソードの場合次の行を無効に
        ratio = 1.0 - ratio;
        webiopi().pulseRatio(24, ratio);
    };
    var sliderHandler3 = function(e, ui){
        var ratio = ui.value/sliderMax;
        // 共通カソードの場合次の行を無効に
        ratio = 1.0 - ratio;
        webiopi().pulseRatio(23, ratio);
    };

    // 3つのスライダへ設定を適用
    $( "#slider1" ).slider({
        min: sliderMin,
        max: sliderMax,
        step: sliderStep,
        value: sliderValue,
        change: sliderHandler1,
        slide: sliderHandler1
    });
    $( "#slider2" ).slider({
        min: sliderMin,
        max: sliderMax,
        step: sliderStep,
        value: sliderValue,
        change: sliderHandler2,
        slide: sliderHandler2
    });
    $( "#slider3" ).slider({
        min: sliderMin,
        max: sliderMax,
        step: sliderStep,
        value: sliderValue,
        change: sliderHandler3,
        slide: sliderHandler3
    });
});

function applyCustomCss(custom_css){
    var head = document.getElementsByTagName('head')[0];
    var style = document.createElement('link');
    style.rel = "stylesheet";
    style.type = 'text/css';
    style.href = custom_css;
    head.appendChild(style);
}

