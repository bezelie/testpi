// bezeMenu.js (node js)
// ベゼリーを再起動すると自動起動する。
// wifi設定、アプリの起動、アプリの設定が行える。
// Updated in May 5th 2017 by Jun Toyoda.
// ---------------------------------------------------------------------------------

// 外部オブジェクトの読み込み
var http = require('http'); // httpオブジェクトの読み込み。いろいろ便利な命令が使える
var fs = require('fs'); // ファイルを読み込むためファイルシステム
var ejs = require('ejs'); // テンプレートエンジンejs
var url = require('url'); // URLをパースするオブジェクト
var qs = require('querystring'); // formから受信したクエリー文字列をオブジェクトに変換する
var exec = require('child_process').exec; // シェルを実行するオブジェクト
// var execSync = require('child_process').execSync; // シェルを同期実行するオブジェクト

// ejsファイルの読み込み
var template = fs.readFileSync(__dirname + '/public_html/template.ejs', 'utf-8'); // テンプレートの同期読み込み
var top = fs.readFileSync(__dirname + '/public_html/top.ejs', 'utf-8');
var inputSSID = fs.readFileSync(__dirname + '/public_html/inputSSID.ejs', 'utf-8');
var inputPASS = fs.readFileSync(__dirname + '/public_html/inputPASS.ejs', 'utf-8');
var finish = fs.readFileSync(__dirname + '/public_html/finish.ejs', 'utf-8');
var confirm = fs.readFileSync(__dirname + '/public_html/confirm.ejs', 'utf-8');
var configBasic = fs.readFileSync(__dirname + '/public_html/configBasic.ejs', 'utf-8');
var configDemo = fs.readFileSync(__dirname + '/public_html/configDemo.ejs', 'utf-8');

// 変数宣言
ssidList = []; // varを省略するとグローバル変数になる。
var routes = { // パスごとの表示内容を連想配列に格納
    "/":{
        "title":"BEZELIE",
        "message":"bezeMenu.jsへようこそ",
        "content":top},
    "/inputSSID":{
        "title":"BEZELIE",
        "message":"wifiのSSIDを選んでください",
        "content":inputSSID},
    "/inputPASS":{
        "title":"BEZELIE",
        "message":"パスワードを入力してください",
        "content":inputPASS},
    "/finish":{
        "title":"BEZELIE",
        "message":"WiFiを設定しました。再起動します",
        "content":finish},
    "/confirm":{
        "title":"BEZELIE",
        "content":confirm},
    "/configBasic":{
        "title":"BEZELIE",
        "content":configBasic},
    "/configDemo":{
        "title":"デモちゃんの設定",
        "content":configDemo}
};

// サーバーの起動
// 同期処理は続く処理を止めてしまうので、必ずcreateServerする前に実行すること
//var settings = require('./wifiInfo.js'); // hostとportを別ファイル(wifiInfo.js)から読み込む
//console.log(settings); // 念のため内容確認
var server = http.createServer(); // httpオブジェクトを使ってサーバーのオブジェクトを作る
server.on('request', doRequest); // requestが来たら関数実行
server.listen(3000, '192.168.10.8') // ポート開放。サーバーを待ち受け状態にする。
//server.listen(3000, '10.0.0.1') // ポート開放。サーバーを待ち受け状態にする。
//server.listen(settings.port, settings.host) // ポート開放。サーバーを待ち受け状態にする。
console.log ("server is listening ... ");

// 関数定義
function doRequest(req, res){ // requestイベントが発生したら実行
    var url_parts = url.parse(req.url); // URL情報をパース
    // 想定していないページに飛ぼうとした場合の処理
    if (routes[url_parts.pathname] == null){ // パスが変数routesに登録されていない場合はエラーを表示する
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end("<html><body><h1>NOT FOUND PAGE:" + 
            req.url + "</h1></body></html>");
        return;
    }
    // GETリクエストの場合
    if (req.method === "GET"){
        if (url_parts.pathname === "/inputSSID"){
            var COMMAND = "sudo iwlist wlan0 scan | grep ESSID | grep -o -E '\".+' | grep -o -E '[^\"]+'";
            exec(COMMAND, function(error, stdout, stderr){
                ssidList = stdout.split(/\r\n|\r|\n/);                
                var content = ejs.render( template, {
                    title: routes[url_parts.pathname].title,
                    content: ejs.render(
                        routes[url_parts.pathname].content,  // pathnameに応じたテンプレートを指定
                        {
                            message: routes[url_parts.pathname].message  // pathnameに応じたメッセージを指定
                        }
                    )
                });
                res.writeHead(200, {'Content-Type': 'text/html'});
                res.write(content);
                res.end();
                return;
            }); // end of exec
        } else {
            if (url_parts.pathname == "/finish"){
                var COMMAND = 'sudo sh -c "wpa_passphrase ' + ssid +' '+ pass + ' >> /etc/wpa_supplicant/wpa_supplicant.conf"';
                exec(COMMAND, function(error, stdout, stderr) {
                    // シェル上でコマンドを実行できなかった場合のエラー処理
                    if (error !== null) {
                        console.log('exec error: ' + error);
                        return;
                    }
                    console.log('wpa: ' + stdout);
                }); // end of exec
            } // end of finish
            var content = ejs.render( template,
                {
                    title: routes[url_parts.pathname].title,
                    content: ejs.render(
                        routes[url_parts.pathname].content,  // pathnameに応じたテンプレートを指定
                        {
                            message: routes[url_parts.pathname].message  // pathnameに応じたメッセージを指定
                        }
                    )
                }
            );
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(content);
            res.end();
            return;
        } // end of else
    } // end of get
    // POSTリクエストの場合
    if (req.method === 'POST') {
        if (url_parts.pathname == "/inputPASS"){
            req.data = ""; // 初期化
            req.on("data", function(data) { // dataイベントは、ポストされたデータを受信している間に発生する
                req.data += data; // POSTされたデータは引数で渡されるので、どんどん追加していく
            })
            req.on("end", function() { // ポスト読み込み終了後の処理
                var query = qs.parse(req.data); // 受信したクエリー文字列をパースしてオブジェクトにまとめる
                ssid = query.ssid
                var content = ejs.render( template,
                    {
                        title: routes[url_parts.pathname].title,
                        content: ejs.render(
                            routes[url_parts.pathname].content,
                            {
                                message: routes[url_parts.pathname].message,  // pathnameに応じたメッセージを指定
                                ssid: ssid
                            }
                        )
                    }
                );
                res.writeHead(200, {'Content-Type': 'text/html'});
                res.write(content);
                res.end();
            });
        }else if (url_parts.pathname == "/confirm"){
            req.data = ""; // 初期化
            req.on("data", function(data) { // dataイベントは、ポストされたデータを受信している間に発生する
                req.data += data; // POSTされたデータは引数で渡されるので、どんどん追加していく
            })
            req.on("end", function() { // ポスト読み込み終了後の処理
                var query = qs.parse(req.data); // 受信したクエリー文字列をパースしてオブジェクトにまとめる
                pass = query.pass
                var content = ejs.render( template,
                    {
                        title: routes[url_parts.pathname].title,
                        content: ejs.render(
                            routes[url_parts.pathname].content,
                            {
                                ssid: ssid,
                                pass: pass
                            }
                        )
                    }
                );
                res.writeHead(200, {'Content-Type': 'text/html'});
                res.write(content);
                res.end();
            });
        } else {
            res.writeHead(200, {'Content-Type': 'text/plain'});
            res.write("NO-POST!!");
            res.end();
        }
    }
} // end of doRequest
