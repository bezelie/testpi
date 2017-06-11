// bezeMenu.js (node js)
// ベゼリーのメニュー。
// アプリの起動、アプリの設定が行える。
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
var top = fs.readFileSync(__dirname + '/public_html/top.ejs', 'utf-8');
var toHost = fs.readFileSync(__dirname + '/public_html/toHost.ejs', 'utf-8');
var configBasic = fs.readFileSync(__dirname + '/public_html/configBasic.ejs', 'utf-8');
var configDemo = fs.readFileSync(__dirname + '/public_html/configDemo.ejs', 'utf-8');
var execDemo = fs.readFileSync(__dirname + '/public_html/execDemo.ejs', 'utf-8');

// 設定ファイルの読み込み
// config.jsonの中が空だと謎のエラーが表示されて悩むことになる。例外処理を入れたい。
var json = fs.readFileSync(__dirname + "/config.json", "utf-8");  // 同期でファイルを読む
obj = JSON.parse(json); // JSONをオブジェクトに変換する。ejsからも読めるようにグローバルで定義する

// 変数宣言
var routes = { // パスごとの表示内容を連想配列に格納
    "/":{
        "title":"BEZELIE",
        "message":"bezeMenuへようこそ",
        "content":top}, // テンプレート
    "/toHost":{
        "title":"wifi設定（再起動）",
        "message":"再起動します",
        "content":toHost},
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
        if (url_parts.pathname === "/toHost"){ // to Hosting -------------------------------------
            content = renderMessage();
            rendering (res, content);
            var COMMAND = 'sh '+__dirname+'/settingHost.sh';
            exec(COMMAND, function(error, stdout, stderr) {
                if (error !== null) {
                    console.log(error.message);
                    console.log(error.code);
                    console.log(error.signal);
                }
                return;
            }); // end of exec
        } else if (url_parts.pathname === "/configDemo"){ // configDemo -----------------------------------
            content = renderMessage();
            rendering (res, content);
            return;
        } else {
            content = renderMessage();
            rendering (res, content);
            return;
        }// end of if
    } // end of get request
    // POSTリクエストの場合 -------------------------------------------------------------------------------
    if (req.method === 'POST') {
        if (url_parts.pathname == "/execDemo"){ // execDemo -------------------------------------------
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

                line1 = '#!/bin/sh';
                line2a = "ps aux | grep python | grep -v grep | awk '{ ";
                line2b = 'print "kill -9", $2 ';
                line2c = "}' | sh";
                line3 = 'cd '+__dirname+'\n'+'python testTalk1.py';
                line4 = 'exit 0';
                var data = line1+'\n'+line2a+line2b+line2c+'\n'+line3+'\n'+line4;
                fs.writeFile(__dirname + '/exeApp.sh', data, function (err) {
                    console.log(err);
                    var COMMAND = 'sh '+__dirname+'/exeApp.sh';
                    exec(COMMAND, function(error, stdout, stderr) {
                        if (error !== null) {
                            console.log(error.message);
                            console.log(error.code);
                            console.log(error.signal);
                        }
                    });
                }); // end of writeFile
            }); // end of req on
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
var host = getLocalAddress().ipv4[0].address;
console.log ("-"+host+"-");

var server = http.createServer(); // http.serverクラスのインスタンスを作る。戻値はhttp.server型のオブジェクト。
server.on('request', doRequest); // serverでrequestイベントが発生した場合のコールバック関数を登録
server.listen(port, host) // listenメソッド実行。サーバーを待ち受け状態にする。
console.log ("server is listening at "+host+":"+port);

