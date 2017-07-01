// bezeHost.js (node js)
// ホスティング状態＝ラズパイがアクセスポイントになっている状態で実行される。
// wifi設定が行える。
// Updated in Jun 10th 2017 by Jun Toyoda.
// ---------------------------------------------------------------------------------

// モジュールの読み込み
var http = require('http'); // httpサーバー・クライアント
var fs = require('fs'); // ファイルおよびファイルシステムを操作するモジュール
var ejs = require('ejs'); // テンプレートエンジンejs
var url = require('url'); // URL文字列をパースやフォーマットするモジュール
var qs = require('querystring'); // formから受信したクエリー文字列をオブジェクトに変換する
var exec = require('child_process').exec; // 子プロセスの生成と管理をするモジュール。
var os = require('os');

// ejsファイルの読み込み
var template = fs.readFileSync(__dirname + '/public_html/template.ejs', 'utf-8');
var host = fs.readFileSync(__dirname + '/public_html/host.ejs', 'utf-8');
var inputPASS = fs.readFileSync(__dirname + '/public_html/inputPASS.ejs', 'utf-8');
var finish = fs.readFileSync(__dirname + '/public_html/finish.ejs', 'utf-8');
var confirm = fs.readFileSync(__dirname + '/public_html/confirm.ejs', 'utf-8');
var toClient = fs.readFileSync(__dirname + '/public_html/toClient.ejs', 'utf-8');

// 設定ファイルの読み込み
// config.jsonの中が空だと謎のエラーが表示されて悩むことになる。例外処理を入れたい。
var json = fs.readFileSync(__dirname + "/config.json", "utf-8");  // 同期でファイルを読む
obj = JSON.parse(json); // JSONをオブジェクトに変換する。ejsからも読めるようにグローバルで定義する

// 変数宣言
var routes = { // パスごとの表示内容を連想配列に格納
    "/":{
        "title":"アクセスポイントの選択",
        "message":"wifiのSSIDを選んでください",
        "content":host}, // テンプレート
    "/inputPASS":{
        "title":"パスワードの入力",
        "message":"パスワードを入力してください",
        "content":inputPASS},
    "/finish":{
        "title":"アクセスポイントへの接続",
        "message":"WiFiに接続します",
        "content":finish},
    "/confirm":{
        "title":"入力確認",
        "message":"このSSIDとパスワードでよろしいですか？",
        "content":confirm},
    "/toClient":{
        "title":"wifi設定中止",
        "message":"再起動します",
        "content":toClient}
};

// 関数定義
function renderMessage (){ // ページに表示する内容を変数conntetに詰め込む
    content = ejs.render( template,
        {
        title: routes[url_parts.pathname].title,
        content: ejs.render(
            routes[url_parts.pathname].content,  // pathnameに応じたテンプレートを指定
                {
                    message: routes[url_parts.pathname].message  // pathnameに応じたメッセージを指定
                })});
   return content;
}

function rendering (res, content){ // ページにcontentを描画する
    res.writeHead(200, {'Content-Type': 'text/html; charset=UTF-8'}); // ステイタスコードやhttpヘッダーをクライアントに送信する。
    res.write(content);
    res.end();
}

function setClient (req, res){ // wifi設定後再起動
    var COMMAND = 'sh '+__dirname+'/settingClient.sh';
    exec(COMMAND, function(error, stdout, stderr) {
        if (error !== null) {
            console.log('exec error: ' + error);
            return;
            }
        console.log('wpa: ' + stdout);
    }); // end of exec
}

// リクエスト処理
function doRequest(req, res){ // requestイベントが発生したら実行
    url_parts = url.parse(req.url); // URL情報をパース
    // 想定していないページに飛ぼうとした場合の処理
    if (routes[url_parts.pathname] == null){ // パスが変数routesに登録されていない場合はエラーを表示する
        var content = "<h1>NOT FOUND PAGE:" + req.url + "</h1>"
        rendering (res, content);
        return;
    }
    // GETリクエストの場合  -------------------------------------------------------------------------------
    if (req.method === "GET"){
        if (url_parts.pathname === "/"){ // WiFiアクセスポイントを検索してssidListに代入 ------------------------
            var COMMAND = "sudo iwlist wlan0 scan|grep ESSID|grep -oE '\".+'|grep -oE '[^\"]+'|grep -v 'x00'";
            exec(COMMAND, function(error, stdout, stderr){
                ssidList = stdout.split(/\r\n|\r|\n/);                
                content = renderMessage();
                rendering (res, content);
                return;
            }); // end of exec
        } else if (url_parts.pathname == "/toClient"){ // toClient ------------------------------------------------
            content = renderMessage();
            rendering (res, content);
            setClient (req, res);
            return;
        } else if (url_parts.pathname == "/finish"){ // finish ------------------------------------------------
            // wifiアクセスポイントのSSIDとパスワードを設定ファイルに書きこむ
            var COMMAND = 'sudo sh -c "wpa_passphrase ' + ssid +' '+ pass + ' >> /etc/wpa_supplicant/wpa_supplicant.conf"';
            exec(COMMAND, function(error, stdout, stderr) {
                if (error !== null) {
                    console.log('exec error: ' + error);
                    return;
                }
                console.log('wpa: ' + stdout);
            }); // end of exec
            content = renderMessage();
            rendering (res, content);
            setClient (req, res);
            return;
        } else {
            content = renderMessage();
            rendering (res, content);
            return;
        }// end of if
    } // end of get request
    // POSTリクエストの場合 -------------------------------------------------------------------------------
    if (req.method === 'POST') {
        if (url_parts.pathname == "/inputPASS"){ // inputPASS ---------------------------------------------
            req.data = ""; // 初期化
            req.on("data", function(data) { // dataイベント発生時（＝data受信中）のイベントハンドラを登録。
                // onメソッドはイベントに対してコールバック関数（イベントハンドラ）を登録するメソッド。
                req.data += data; // POSTされたデータは引数で渡されるので、どんどん追加していく
            });
            req.on("end", function() { // endイベントが発生（＝data受信完了）した後のイベントハンドラを登録。
                var query = qs.parse(req.data); // 受信したクエリー文字列をパースしてオブジェクトにまとめる
                ssid = query.ssid
                content = renderMessage();
                rendering (res, content);
            });
        }else if (url_parts.pathname == "/confirm"){ // confirm -------------------------------------------
            req.data = ""; // 初期化
            req.on("data", function(data) { // dataイベントは、ポストされたデータを受信している間に発生する
                req.data += data; // POSTされたデータは引数で渡されるので、どんどん追加していく
            });
            req.on("end", function() { // ポスト読み込み終了後の処理
                var query = qs.parse(req.data); // 受信したクエリー文字列をパースしてオブジェクトにまとめる
                pass = query.pass
                content = renderMessage();
                rendering (res, content);
            });
        } else { // 該当せず -------------------------------------------------------------------------------
            var content = "NO-POST!!";
            rendering (res, content);
            return;
        } // end of if
    } // end of POST request
} // end of doRequest

// サーバーの起動
// 同期処理は続く処理を止めてしまうので、必ずcreateServerする前に実行すること
console.log ("Lets get started");

var port = 3000 // 1024以上の数字なら何でもいいが、expressは3000をデフォにしているらしい
//var host = 'localhost'
var host = '10.0.0.1'

var server = http.createServer(); // http.serverクラスのインスタンスを作る。戻値はhttp.server型のオブジェクト。
server.on('request', doRequest); // serverでrequestイベントが発生した場合のコールバック関数を登録
server.listen(port, host) // listenメソッド実行。サーバーを待ち受け状態にする。
console.log ("server is listening at "+host+":"+port);
