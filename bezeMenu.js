// bezeMenu.js (node js)
// ベゼリーを再起動すると自動起動する。
// wifi設定、アプリの起動、アプリの設定が行える。
// Updated in May 25th 2017 by Jun Toyoda.
// ---------------------------------------------------------------------------------

// モジュールの読み込み
var http = require('http'); // httpサーバー・クライアント
var fs = require('fs'); // ファイルおよびファイルシステムを操作するモジュール
var ejs = require('ejs'); // テンプレートエンジンejs
var url = require('url'); // URL文字列をパースやフォーマットするモジュール
var qs = require('querystring'); // formから受信したクエリー文字列をオブジェクトに変換する
var exec = require('child_process').exec; // 子プロセスの生成と管理をするモジュール。
// var csv = require('csv');
var CSV = require("comma-separated-values"); // CSVを配列変数やオブジェクトに変換する
// var execSync = require('child_process').execSync; // シェルを同期実行するオブジェクト
var os = require('os');


// ejsファイルの読み込み
var template = fs.readFileSync(__dirname + '/public_html/template.ejs', 'utf-8');
var top = fs.readFileSync(__dirname + '/public_html/top.ejs', 'utf-8');
var first = fs.readFileSync(__dirname + '/public_html/first.ejs', 'utf-8');
var inputSSID = fs.readFileSync(__dirname + '/public_html/inputSSID.ejs', 'utf-8');
var inputPASS = fs.readFileSync(__dirname + '/public_html/inputPASS.ejs', 'utf-8');
var finish = fs.readFileSync(__dirname + '/public_html/finish.ejs', 'utf-8');
var confirm = fs.readFileSync(__dirname + '/public_html/confirm.ejs', 'utf-8');
var configBasic = fs.readFileSync(__dirname + '/public_html/configBasic.ejs', 'utf-8');
var configDemo = fs.readFileSync(__dirname + '/public_html/configDemo.ejs', 'utf-8');
var execDemo = fs.readFileSync(__dirname + '/public_html/execDemo.ejs', 'utf-8');

// 設定ファイルの読み込み
var json = fs.readFileSync(__dirname + "/config.json", "utf-8");  // 同期でファイルを読む
obj = JSON.parse(json); // JSONをオブジェクトに変換する。ejsからも読めるようにグローバルで定義する

// 変数宣言
var routes = { // パスごとの表示内容を連想配列に格納
    "/":{
        "title":"BEZELIE",
        "message":"bezeMenuへようこそ",
        "content":top}, // テンプレート
    "/first":{
        "title":"Bezelie Menu Top Page",
        "message":"bezeMenuへようこそ",
        "content":first}, // テンプレート
    "/inputSSID":{
        "title":"アクセスポイントの選択",
        "message":"wifiのSSIDを選んでください",
        "content":inputSSID},
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
    "/configBasic":{
        "title":"BEZELIE",
        "content":configBasic},
    "/configDemo":{
        "title":"デモアプリの設定",
        "content":configDemo},
    "/execDemo":{
        "title":"デモアプリ設定完了",
        "message":"デモを起動します",
        "content":execDemo}
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

function getLocalAddress() {
    var ifacesObj = {}
    ifacesObj.ipv4 = [];
    ifacesObj.ipv6 = [];
    var interfaces = os.networkInterfaces();

    for (var dev in interfaces) {
        interfaces[dev].forEach(function(details){
            if (!details.internal){
                switch(details.family){
                    case "IPv4":
                        ifacesObj.ipv4.push({name:dev, address:details.address});
                    break;
                    case "IPv6":
                        ifacesObj.ipv6.push({name:dev, address:details.address})
                    break;
                }
            }
        });
    }
    return ifacesObj;
};

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
        if (url_parts.pathname === "/"){ // first Arraival  -----------------------------------------------
            // wifi設定ができていない場合はwifi設定のページに飛ばしたいのだけど、まだよい方法がわからない。
            // wifiConnecttionScceed.csvが空だったらwifi設定できてないとみなしているけど、このファイルに書きこむ
            // 処理はまだできてない。
            var text = fs.readFileSync('/home/pi/bezelie/testpi/wifiConnectionSucceed.csv', 'utf8'); // 同期で読み込み
            var list = new CSV(text, {header:false}).parse();
            if (list.length > 1){ // wifi接続が成功したことがある場合
                content = renderMessage();
                rendering (res, content);
                return;
            } else { // wifi接続にいちども成功していない場合
                var content = "<H3>最初にwifiを設定してください</H3><H5><a href='/inputSSID'>wifi設定</a></H5>"
                rendering (res, content);
                return;}
        } else if (url_parts.pathname === "/inputSSID"){ // inputSSID -------------------------------------
            var COMMAND = "sudo iwlist wlan0 scan|grep ESSID|grep -oE '\".+'|grep -oE '[^\"]+'|grep -v 'x00'";
            exec(COMMAND, function(error, stdout, stderr){
                ssidList = stdout.split(/\r\n|\r|\n/);                
                content = renderMessage();
                rendering (res, content);
                return;
            }); // end of exec
        } else if (url_parts.pathname === "/configDemo"){ // configDemo -----------------------------------
            content = renderMessage();
            rendering (res, content);
            return;
        } else {
            if (url_parts.pathname == "/finish"){ // finish ------------------------------------------------
                // wifiアクセスポイントのSSIDとパスワードを設定ファイルに書きこむ
                var COMMAND = 'sudo sh -c "wpa_passphrase ' + ssid +' '+ pass + ' >> /etc/wpa_supplicant/wpa_supplicant.conf"';
                exec(COMMAND, function(error, stdout, stderr) {
                    // シェル上でコマンドを実行できなかった場合のエラー処理
                    if (error !== null) {
                        console.log('exec error: ' + error);
                        return;
                    }
                    console.log('wpa: ' + stdout);
                }); // end of exec
                // wifi接続試験の実施
                var COMMAND = 'sudo sh connectingWifi.sh';
                exec(COMMAND, function(error, stdout, stderr) {
                    if (error !== null) {
                        console.log('exec error: ' + error);
                        return;
                    }
                    console.log('wpa: ' + stdout);
                }); // end of exec
            } // end of finish
            content = renderMessage();
            rendering (res, content);
            // process.exit(); // node終了
            return;
        } // end of else
    } // end of get
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
        }else if (url_parts.pathname == "/execDemo"){ // execDemo -------------------------------------------
            req.data = "";
            req.on("data", function(data) {
                req.data += data;
            });
            req.on("end", function() {
                obj.data1[0] = qs.parse(req.data);
                fs.writeFile(__dirname + '/config.json', JSON.stringify(obj), function (err) {
                    console.log(err);
                });
                content = renderMessage();
                rendering (res, content);

                //var data = "aaa";
                //console.log(data);
                //fs.writeFile(__dirname + '/exeApp1.sh', data, function (err) {
                //    console.log(err);
                //});
                // var COMMAND = 'sudo sh ;
                // exec(COMMAND, function(error, stdout, stderr) {
            });
        } else { // 該当せず -------------------------------------------------------------------------------
            var content = "NO-POST!!";
            rendering (res, content);
        }
    }
} // end of doRequest

// サーバーの起動
// 同期処理は続く処理を止めてしまうので、必ずcreateServerする前に実行すること
var server = http.createServer(); // http.serverクラスのインスタンスを作る。戻値はhttp.server型のオブジェクト。
server.on('request', doRequest); // serverでrequestイベントが発生した場合のコールバック関数を登録
//var port = 8080 // 1024以上の数字なら何でもいいが、expressは3000をデフォにしているらしい
var port = 3000 // 1024以上の数字なら何でもいいが、expressは3000をデフォにしているらしい
// ここ自動的にIPアドレスを代入したい
//var host = 'localhost'
//var host = '192.168.10.5'
var host = '10.0.0.1'

var host1 = getLocalAddress().ipv4[0].address;
console.log ("-"+host1+"-");

server.listen(port, host) // listenメソッド実行。サーバーを待ち受け状態にする。
console.log ("server is listening at "+host+":"+port);
