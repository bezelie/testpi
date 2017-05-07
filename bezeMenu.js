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
// var csv = require('csv');
var CSV = require("comma-separated-values");
// var execSync = require('child_process').execSync; // シェルを同期実行するオブジェクト

// ejsファイルの読み込み（同期）
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

// 変数宣言
var routes = { // パスごとの表示内容を連想配列に格納
    "/":{
        "title":"BEZELIE",
        "message":"bezeMenuへようこそ",
        "content":top}, // テンプレート
    "/first":{
        "title":"BEZELIE",
        "message":"bezeMenuへようこそ",
        "content":first}, // テンプレート
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
        "message":"WiFiに接続します",
        "content":finish},
    "/confirm":{
        "title":"BEZELIE",
        "message":"このSSIDとパスワードでよろしいですか？",
        "content":confirm},
    "/configBasic":{
        "title":"BEZELIE",
        "content":configBasic},
    "/configDemo":{
        "title":"デモの設定",
        "content":configDemo},
    "/execDemo":{
        "title":"デモちゃんの実行",
        "message":"メッセージです",
        "content":execDemo}
};
global.alarmOn, global.alarmTime, global.alarmKind, global.alarmVol
global.awake1Start ,global.awake1End, global.awake2Start, global.awake2End
//ringOn,ringKind,chatOn,chatFreq,chatKind

// 関数定義
function renderMessage (){
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
function rendering (res, content){
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(content);
    res.end();
}

// サーバーの起動
// 同期処理は続く処理を止めてしまうので、必ずcreateServerする前に実行すること
var server = http.createServer(); // httpオブジェクトを使ってサーバーのオブジェクトを作る
server.on('request', doRequest); // requestが来たら関数実行
var port = 3000
var host = '192.168.10.8'
// var host = '10.0.0.1'
server.listen(port, host) // ポート開放。サーバーを待ち受け状態にする。
console.log ("server is listening at "+host+":"+port);

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
            var text = fs.readFileSync('/home/pi/bezelie/testpi/wifiConnectionSucceed.csv', 'utf8');
            var list = new CSV(text, {header:false}).parse();
            if (list.length > 1){
                content = renderMessage();
                rendering (res, content);
                return;
            } else {
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
            var text = fs.readFileSync('/home/pi/bezelie/testpi/config.csv', 'utf8');
            var list = new CSV(text, {header:false}).parse();
            global.alarmOn0 = '', global.alarmOn1 = ''
            global.alarmKind0 = "", global.alarmKind1 = ""
            var checked = "checked = 'checked'";
            var selected = "selected = 'true'";
            console.log("read data= \n"+list);
            for (i=0;i<list.length;++i){
                switch (list[i][0]){
                    case 'alarmOn':
                      if (list[i][1]=='true'){alarmOn0 = checked}else{alarmOn1 = checked}
                    break;
                    case 'alarmTime':alarmTime = list[i][1];break;
                    case 'alarmKind':
                      if (list[i][1]=='mild'){alarmKind0 = selected}else{alarmKind1 = selected}
                    break;
                    case 'alarmVol':alarmVol = list[i][1];break;
                    case 'awake1Start':awake1Start = list[i][1];break;
                    case 'awake1End':awake1End = list[i][1];break;
                    case 'awake2Start':awake2Start = list[i][1];break;
                    case 'awake2End':awake2End = list[i][1];break;
                }
            }
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
            return;
        } // end of else
    } // end of get
    // POSTリクエストの場合 -------------------------------------------------------------------------------
    if (req.method === 'POST') {
        if (url_parts.pathname == "/inputPASS"){ // inputPASS ---------------------------------------------
            req.data = ""; // 初期化
            req.on("data", function(data) { // dataイベントは、ポストされたデータを受信している間に発生する
                req.data += data; // POSTされたデータは引数で渡されるので、どんどん追加していく
            });
            req.on("end", function() { // ポスト読み込み終了後の処理
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
                var query = qs.parse(req.data);
                var data = "alarmOn,"+query.alarmOn+"\n"+"alarmTime,"+query.alarmTime+"\n"+"alarmKind,"+query.alarmKind+"\n"+"alarmVol,"+query.alarmVol+"\n"+
                "awake1Start,"+query.awake1Start+"\n"+"awake1End,"+query.awake1End+"\n"+"awake2Start,"+query.awake2Start+"\n"+"awake2End,"+query.awake2End+"\n";
                    
                console.log('write data=\n'+data);
                fs.writeFile('/home/pi/bezelie/testpi/config.csv', data , function (err) { // ファイルに書込
//                    console.log(err);
                });
                content = renderMessage();
                rendering (res, content);
            });
        } else { // 該当せず -------------------------------------------------------------------------------
            var content = "NO-POST!!";
            rendering (res, content);
        }
    }
} // end of doRequest
