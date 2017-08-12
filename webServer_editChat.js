// node js
// べゼリー対話データの編集 
// 
// Updated in Aug 10th 2017 by Jun Toyoda.
// ---------------------------------------------------------------------------------

// モジュールをロードして変数にオブジェクトとして読み込む
var http = require('http'); // httpアクセスのための機能を提供するモジュール
                            //   http.createServer(function);
var fs   = require('fs');   // ファイルおよびファイルシステムを操作するモジュール
                            //   fs.readFile('file name','utf-8',callback function)
                            //   fs.readFileSync('file name','utf-8')
var ejs  = require('ejs');  // JS用テンプレートエンジンejs(Embedded JavaScript Templates)
                            //    ejs.render(変数に代入されたejs, 置換データオブジェクト);
var url  = require('url');  // URL文字列をパースやフォーマットするモジュール
                            //    url.parse(request.url);
var qs   = require('querystring');
                            // クエリー文字列をパースしてオブジェクトに変換するモジュール
                            //    qs.parse();
var exec = require('child_process').exec; 
                            // 子プロセスの生成と管理をするモジュール。
var os   = require('os');
var CSV  = require("comma-separated-values"); 
                            // CSVを配列変数やオブジェクトに変換する

// ejsファイルの読み込み
var template            = fs.readFileSync(__dirname + '/public_html/template.ejs', 'utf-8');
var top                 = fs.readFileSync(__dirname + '/public_html/top.ejs', 'utf-8');
var editChat            = fs.readFileSync(__dirname + '/public_html/editChat.ejs', 'utf-8');
var editTime            = fs.readFileSync(__dirname + '/public_html/editTime.ejs', 'utf-8');
var setTime             = fs.readFileSync(__dirname + '/public_html/setTime.ejs', 'utf-8');
var editIntent          = fs.readFileSync(__dirname + '/public_html/editIntent.ejs', 'utf-8');
var selectIntent4entity = fs.readFileSync(__dirname + '/public_html/selectIntent4entity.ejs', 'utf-8');
var editEntity          = fs.readFileSync(__dirname + '/public_html/editEntity.ejs', 'utf-8');
var selectIntent4dialog = fs.readFileSync(__dirname + '/public_html/selectIntent4dialog.ejs', 'utf-8');
var editDialog          = fs.readFileSync(__dirname + '/public_html/editDialog.ejs', 'utf-8');
var starting_pythonApp  = fs.readFileSync(__dirname + '/public_html/starting_pythonApp.ejs', 'utf-8');
var stop_pythonApp      = fs.readFileSync(__dirname + '/public_html/stop_pythonApp.ejs', 'utf-8');
var disableServer       = fs.readFileSync(__dirname + '/public_html/disableServer.ejs', 'utf-8');
var test       = fs.readFileSync(__dirname + '/public_html/test.ejs', 'utf-8');

// 設定ファイル（アラーム時刻や活動時間などの設定）の読み込み
// jsonファイルの中が空だと謎のエラーが表示されて悩むことになる。例外処理を入れたい。
var json = fs.readFileSync(__dirname + "/data_chat.json", "utf-8");  // 同期でファイルを読む
obj_config = JSON.parse(json); // JSONをオブジェクトに変換する。ejsからも読めるようにグローバルで定義する

// 変数宣言
var routes = { // パスごとの表示内容を連想配列に格納
    "/":{
        "title":"BEZELIE",
        "message":"",
        "content":top}, // テンプレート
    "/editChat":{
        "title":"会話設定",
        "message":"",
        "content":editChat},
    "/editTime":{
        "title":"時間設定",
        "content":editTime},
    "/disableServer":{
        "title":"",
        "message":"再起動します",
        "content":disableServer},
    "/editIntent":{
        "title":"インテント（意図）の編集",
        "message":"インテントの追加や削除ができます。インテントとはロボットに伝えたい内容のことです。この文字が音声認識されるわけではないので、内容がわかるような簡潔な名称をつけてください",
        "content":editIntent},
    "/selectIntent4entity":{
        "title":"エンティティ（同意語）の編集",
        "message":"エンティティを関連付けるインテントを選んでください。",
        "content":selectIntent4entity},
    "/editEntity":{
        "title":"エンティティ（同意語）の編集",
        "message":"エンティティの追加や削除ができます。エンティティとはインテントをロボットに伝えるための具体的な言葉のことです。ひとつのインテントに対して複数設定することができます。ひらがなで入力してください（カタカナなどが含まれているとエラーになります）",
        "content":editEntity},
    "/selectIntent4dialog":{
        "title":"ダイアログ（対話）の編集",
        "message":"ダイアログを関連付けるインテントを選んでください。",
        "content":selectIntent4dialog},
    "/editDialog":{
        "title":"ダイアログ（対話）の編集",
        "message":"ダイアログの追加や削除ができます。ダイアログとはインテントに対するロボットの返答です。ひとつのインテントに対して複数設定した場合はランダムで選ばれます。",
        "content":editDialog},
    "/stop_pythonApp":{
        "title":"プログラム停止",
        "message":"デモを停止します",
        "content":stop_pythonApp},
    "/starting_pythonApp":{
        "title":"チャットプログラム実行",
        "message":"デモを起動します",
        "content":starting_pythonApp},
    "/setTime":{
        "title":"設定完了",
        "message":"",
        "content":setTime},
    "/test":{
        "title":"test",
        "message":"test",
        "content":test}
};
// グローバル変数は便利だが多用すべきではない
// global.postsLength;

// 関数定義
function renderMessage (){ // ページに表示する内容を変数conntetに詰め込む
    content = ejs.render( template,
        {
        title: routes[url_parts.pathname].title,
        content: ejs.render(
            routes[url_parts.pathname].content,
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

function disableServer (req, res){ // サーバーを無効化する設定をしたあと再起動
    var COMMAND = 'sh '+__dirname+'/setting_disableServer.sh';
    exec(COMMAND, function(error, stdout, stderr) {
        if (error !== null) {
            console.log('exec error: ' + error);
            return;
            }
        console.log('wpa: ' + stdout);
    }); // end of exec
}

// ルーティング
function routing(req, res){ // requestイベントが発生したら実行
    url_parts = url.parse(req.url); // URL情報をパース処理
    // 想定していないページに飛ぼうとした場合の処理
    if (routes[url_parts.pathname] == null){ // パスが変数routesに登録されていない場合はエラーを表示する
        var content = "<h1>NOT FOUND PAGE:" + req.url + "</h1>"
        rendering (res, content);
        return;
    }
    // GETリクエストの場合  -------------------------------------------------------------------------------
    if (req.method === "GET"){
        if (url_parts.pathname == "/stop_pythonApp"){ // -------------------------------------------
            rendering (res, renderMessage());
            var COMMAND = "sh stop_pythonApp.sh";
            exec(COMMAND, function(error, stdout, stderr) {
               if (error !== null) {
                    console.log(error.message);
                } // end of if
            }); // end of exec
            var COMMAND = "sh stop_julius.sh";
            exec(COMMAND, function(error, stdout, stderr) {
               if (error !== null) {
                    console.log(error.message);
                } // end of if
            }); // end of exec
        } else if (url_parts.pathname == "/starting_pythonApp"){ // ----------------
            rendering (res, renderMessage());
            var COMMAND = 'sh '+__dirname+'/starting_pythonApp.sh';
            exec(COMMAND, {maxBuffer : 1024 * 1024 * 1024}, function(error, stdout, stderr) {
                console.log(stdout);
                if (error !== null) {
                    console.log(error.message);
                } // end of if
            }); // end of exec
        } else if (url_parts.pathname === "/disableServer"){ //  -------------------------------------
            rendering (res, renderMessage());
            disableServer (req, res);
            return;
        } else if (url_parts.pathname === "/selectIntent4entity" || url_parts.pathname === "/selectIntent4dialog"){
            var text = fs.readFileSync(__dirname + "/chatIntent.csv", 'utf8'); // 同期でファイルを読む
            var intents = new CSV(text, {header:false}).parse(); //  CSVファイルをリスト変数に変換する
            content = ejs.render( template,
            {
                title: routes[url_parts.pathname].title,
                content: ejs.render(
                routes[url_parts.pathname].content,  // pathnameに応じたテンプレートを指定
                {
                    message: routes[url_parts.pathname].message,  // pathnameに応じたメッセージを指定
                    intents: intents // 投稿の内容
            })});
            rendering (res, content);
            return;
        } else if (url_parts.pathname === "/editIntent"){ // editIntent -----------------------------------
            var text = fs.readFileSync(__dirname + "/chatIntent.csv", 'utf8'); // 同期でファイルを読む
            var posts = new CSV(text, {header:false}).parse(); //  CSVファイルをリスト変数に変換する
            content = ejs.render( template,
            {
                title: routes[url_parts.pathname].title,
                content: ejs.render(
                routes[url_parts.pathname].content,  // pathnameに応じたテンプレートを指定
                {
                    message: routes[url_parts.pathname].message,  // pathnameに応じたメッセージを指定
                    posts: posts // 投稿の内容
            })});
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
        if (url_parts.pathname == "/editDialog"){ // editDialog -------------------------------------------
            req.data = "";
            req.on("data", function(data) {
                req.data += data;
            });
            req.on("end", function() {
                var query = qs.parse(req.data); // 全受信データをquerry stringでパースする。
                var text = fs.readFileSync(__dirname + "/chatDialog.csv", 'utf8'); // 同期でCSVファイルを読む
                posts = new CSV(text, {header:false}).parse(); //  TEXTをCSVを仲介してリスト変数に変換する
                postsLength = posts.length; // ejsに受け渡すためグローバル変数を利用

                if (query.newItem){ // addItem
                    var flag = true;
                    for (var i=0;i < posts.length; i++ ) {
                        if (posts [i][0] == intent && posts[i][1] == query.newItem){
                            console.log ('It has existed');
                            flag = false;
                        }
                    }
                    if (flag == true){ 
                        text = text+intent+','+query.newItem+'\n';
                        posts.push([intent,query.newItem]); // newItemをpostの配列に入れる。
                    }
//                }else if (query.intent){ // intentが設定された場合
//                    intent = query.intent; // グローバル変数intentに代入。もっといい方法ないの？
                }else{ // delItem
                    text = '';
                    for (var i=0;i < posts.length; i++ ) {
                        if (i != query.delNum){
                            text = text+posts[i]+'\n';
                        }
                    }
                    posts.splice(query.delNum, 1); // postsからもdelNum行を削除
                }
                fs.writeFileSync(__dirname + '/chatDialog.csv', text , 'utf8', function (err) { // ファイルに書込
                    console.log(err);
                });

                content = ejs.render( template,
                {
                    title: routes[url_parts.pathname].title,
                    content: ejs.render(
                    routes[url_parts.pathname].content,  // pathnameに応じたテンプレートを指定
                    {
                        message: routes[url_parts.pathname].message,  // pathnameに応じたメッセージを指定
                        intent: intent, // インテント
                        posts: posts // 投稿の内容
                })});
//                console.log (posts);
                rendering (res, content);
            }); // end of req on
        } else if (url_parts.pathname == "/editEntity"){ // editEntity -------------------------------------------
            req.data = "";
            req.on("data", function(data) {
                req.data += data;
            });
            req.on("end", function() {
                var query = qs.parse(req.data); // 全受信データをパースする。
                var text = fs.readFileSync(__dirname + "/chatEntity.csv", 'utf8'); // 同期でファイルを読む
                posts = new CSV(text, {header:false}).parse(); //  TEXTをCSVを仲介してリスト変数に変換する
                postsLength = posts.length; // ejsに受け渡すためグローバル変数を利用

                if (query.newItem){ // addItem
                    var flag = true;
                    for (var i=0;i < posts.length; i++ ) {
                        if (posts [i][0] == intent && posts[i][1] == query.newItem){
                            console.log ('It has existed');
                            flag = false;
                        }
                    }
                    if (flag == true){ 
                        text = text+intent+','+query.newItem+'\n';
                        posts.push([intent,query.newItem]); // newItemをpostの配列に入れる。
                    }
//                }else if (query.intent){ // intentが設定された場合
//                    intent = query.intent; // グローバル変数intentに代入。もっといい方法ないの？
                }else{ // delItem
                    text = '';
                    for (var i=0;i < posts.length; i++ ) {
                        if (i != query.delNum){
                            text = text+posts[i]+'\n';
                        }
                    }
                    posts.splice(query.delNum, 1); // postsからもdelNum行を削除
                }
                fs.writeFileSync(__dirname + '/chatEntity.csv', text , 'utf8', function (err) { // ファイルに書込
                    console.log(err);
                });

                var COMMAND = 'sudo sed -E "s/,/    /g" chatEntity.csv > chatEntity.tsv'; // csvをtsvに変換
                exec(COMMAND, function(error, stdout, stderr) {
                    if (error !== null) {
                        console.log(error.message);
                    }

                var COMMAND = 'iconv -f utf8 -t eucjp chatEntity.tsv | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > chatEntity.dic'; // tsvをdicに変換
                exec(COMMAND, function(error, stdout, stderr) {
                    if (error !== null) {
                        console.log(error.message);
                    }
                });
                });

                content = ejs.render( template,
                {
                    title: routes[url_parts.pathname].title,
                    content: ejs.render(
                    routes[url_parts.pathname].content,  // pathnameに応じたテンプレートを指定
                    {
                        message: routes[url_parts.pathname].message,  // pathnameに応じたメッセージを指定
                        intent: intent, // インテント
                        posts: posts // 投稿の内容
                })});
                rendering (res, content);
            }); // end of req on
        } else if (url_parts.pathname == "/editIntent"){ // editIntent -------------------------------------------
            req.data = "";
            req.on("data", function(data) {
                req.data += data;
            });
            req.on("end", function() {
                var query = qs.parse(req.data); // 全受信データをパースする。
                var text = fs.readFileSync(__dirname + "/chatIntent.csv", 'utf8'); // 同期でファイルを読む
                posts = new CSV(text, {header:false}).parse(); //  TEXTをCSVを仲介してリスト変数に変換する
                postsLength = posts.length; // ejsに受け渡すためグローバル変数を利用

                if (query.newItem){ // addItem
                    var flag = true;
                    for (var i=0;i < posts.length; i++ ) {
                        if (posts[i][1] == query.newItem){
                            console.log ('It has existed');
                            flag = false;
                        }
                    }
                    if (flag == true){ 
                        text = text+'common,'+query.newItem+'\n';
                        posts.push(['common',query.newItem]); // newItemをpostの配列に入れる。
                    }
                }else{ // delItem
                    text = '';
                    for (var i=0;i < posts.length; i++ ) {
                        if (i != query.delNum){
                            text = text+posts[i]+'\n';
                        }
                    }
                    posts.splice(query.delNum, 1);
                }
                fs.writeFileSync(__dirname + '/chatIntent.csv', text , 'utf8', function (err) { // ファイルに書込
                    console.log(err);
                });

                content = ejs.render( template,
                {
                    title: routes[url_parts.pathname].title,
                    content: ejs.render(
                    routes[url_parts.pathname].content,  // pathnameに応じたテンプレートを指定
                    {
                        message: routes[url_parts.pathname].message,  // pathnameに応じたメッセージを指定
                        posts: posts // 投稿の内容
                })});
                rendering (res, content);
            }); // end of req on
        } else if (url_parts.pathname == "/setTime"){ //  -------------------------------------------
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

// var host = 'localhost'
// var host = '10.0.0.1' // ラズパイをサーバーにする時は、この行をコメントアウトする。

var server = http.createServer(); // http.serverクラスのインスタンスを作る。戻値はhttp.server型のオブジェクト。
server.on('request', routing); // serverでrequestイベントが発生した場合のコールバック関数を登録
//server.listen(port, host) // listenメソッド実行。サーバーを待ち受け状態にする。
server.listen(port) // listenメソッド実行。サーバーを待ち受け状態にする。
console.log ("server is listening at "+host+":"+port);

