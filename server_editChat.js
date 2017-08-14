// node js
// べゼリー対話データを編集するWebアプリ 
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
                            //    exec(COMMAND, [options], callback(error, stdout, stderr) {}
                            //    option maxBuffer:バッファの最大容量(byte)
                            //    error :エラーオブジェクト
                            //    stdout:標準出力に出力されたデータ
                            //    stderr:標準エラー出力に出力されたデータ
var CSV  = require("comma-separated-values"); 
                            // CSVを配列変数やオブジェクトに変換する
var os   = require('os');
                            //    os.networkInterfaces();

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
var test                = fs.readFileSync(__dirname + '/public_html/test.ejs', 'utf-8');

// 変数宣言
var routes = { // パスごとの表示内容を連想配列に格納
    "/":{
        "title":"BEZELIE",
        "message":"べゼリーとの対話データの編集やアラーム時間などの変更ができます",
        "content":top}, // テンプレート
    "/editChat":{
        "title":"対話設定",
        "message":"３つのデータを編集することで、自分だけの対話を作ることができます",
        "content":editChat},
    "/editTime":{
        "title":"時間設定",
        "message":"アラームと活動時間の設定をします",
        "content":editTime},
    "/disableServer":{
        "title":"再起動",
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
        "title":"プログラムの実行",
        "message":"再起動します",
        "content":starting_pythonApp},
    "/setTime":{
        "title":"設定完了",
        "message":"設定を更新しました",
        "content":setTime},
    "/test":{
        "title":"テスト",
        "message":"これはテスト用のページです",
        "content":test}
};
// 変数宣言
var errorMsg = ""; // これが空欄のときはエラー無し
var posts = "";    // ブラウザからPOSTで送られてきたデータ
var intent = "";   // 今回選択されたintent（単数）

// 関数定義
function getLocalAddress() { // IPアドレスの取得
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

function reboot(){ // ラズパイの再起動
    var COMMAND = 'sudo reboot';
    exec(COMMAND, function(error, stdout, stderr) {
    }); // end of exec
}

function pageWrite (res){ // ページ描画
    content = ejs.render( template, {
        title: routes[url_parts.pathname].title,
        errorMsg: errorMsg,
        content: ejs.render( routes[url_parts.pathname].content, {
            message: routes[url_parts.pathname].message,  // pathnameに応じたメッセージを指定
            posts: posts,  // ブラウザからPOSTされてきたデータ
            intent: intent // 今回選ばれたインテント
        })
    });
    res.writeHead(200, {'Content-Type': 'text/html; charset=UTF-8'}); // ステイタスコードやhttpヘッダーをクライアントに送信する。
    res.write(content);
    res.end();
}

function delChk (query, posts, intent){ // 削除しようとしている番号が、選択中のインテントのものかを調べる
    errorMsg = "番号が違います";
    for (var i=0;i < posts.length; i++ ) {
        if (posts[i][0]==intent && i==query.delNum){
            errorMsg = "";
        }
    }
    return errorMsg;
}

function readPosts(file){
    var text = fs.readFileSync(__dirname + "/" + file, 'utf8'); // 同期でファイルを読む
    posts = new CSV(text, {header:false}).parse(); //  TEXTをCSVを仲介してリスト変数に変換する
    return posts;
}

function obj2csv(posts){
    text = '';
    for (var i=0;i < posts.length; i++ ) {
        text = text+posts[i]+'\n';
        }
    return text;
}

//-------------------------------------------------------------------------------------------------------
// ルーティング
function routing(req, res){ // requestイベントが発生したら実行される関数
    url_parts = url.parse(req.url); // URL情報をパース処理
    errorMsg = "";
    // 想定していないページに飛ぼうとした場合の処理
    if (routes[url_parts.pathname] == null){ // パスが変数routesに登録されていない場合はエラーを表示する
        content = "<h1>NOT FOUND PAGE:" + req.url + "</h1>"
        res.writeHead(200, {'Content-Type': 'text/html; charset=UTF-8'}); // ステイタスコードやhttpヘッダーをクライアントに送信する。
        res.write(content);
        res.end();
        return;
    }
    // GETリクエストの場合  -------------------------------------------------------------------------------
    if (req.method === "GET"){
        if (url_parts.pathname === "/editIntent" || url_parts.pathname === "/selectIntent4entity" || url_parts.pathname === "/selectIntent4dialog"){ 
            posts = readPosts("chatIntent.csv");
            pageWrite(res);
            return;
        } else if (url_parts.pathname == "/starting_pythonApp"){ // ラズパイ再起動
            pageWrite(res);
            var COMMAND = 'sh '+__dirname+'/setting_enableApp.sh';
            exec(COMMAND, {maxBuffer : 1024 * 1024 * 1024}, function(error, stdout, stderr) {
            // reboot(); // ラズパイを再起動させる。
            }); // end of exec
        } else if (url_parts.pathname == "/stop_pythonApp"){ // アプリ停止
            pageWrite(res);
            var COMMAND = "sh stop_pythonApp.sh";
            exec(COMMAND, function(error, stdout, stderr) {
            }); // end of exec
            var COMMAND = "sh stop_julius.sh";
            exec(COMMAND, function(error, stdout, stderr) {
            }); // end of exec
        } else if (url_parts.pathname === "/disableServer"){ // サーバーを無効化して再起動
            pageWrite(res);
            var COMMAND = 'sh '+__dirname+'/setting_disableServer.sh';
            exec(COMMAND, function(error, stdout, stderr) {
               reboot();
            }); // end of exec
        } else if (url_parts.pathname === "/editTime"){ // 時間編集
            var json = fs.readFileSync(__dirname + "/data_chat.json", "utf-8");  // 同期でファイルを読む
            obj_config = JSON.parse(json); // JSONをオブジェクトに変換する。ejsからも読めるようにグローバルで定義する
            pageWrite(res)
        } else {
            pageWrite(res);
        }// end of if
    } // end of get request
    // POSTリクエストの場合 -------------------------------------------------------------------------------
    if (req.method === 'POST') {
        req.data = "";
        req.on("data", function(data) {
            req.data += data;
        });
        req.on("end", function() {
            var query = qs.parse(req.data); // 全受信データをquerry stringでパースする。
        // ----------------------------------------------------------------------------------------------
            if (url_parts.pathname == "/editIntent"){ // インテントの編集
                posts = readPosts("chatIntent.csv");
                if (query.newItem){ // 新規追加
                    for (var i=0;i < posts.length; i++ ) {
                        if (posts[i][1] == query.newItem){
                            errorMsg = "すでに登録されています";
                        }
                    }
                    if (errorMsg == ""){ 
                        posts.push(['common',query.newItem]); // newItemをpostの配列に入れる。
                    }
                } else if (query.delNum){ // 削除
                    if(isNaN(query.delNum)){
                        errorMsg = "数字(半角)を入力してください";
                    } else if(query.delNum >= posts.length) {
                        errorMsg = "数字が大きすぎます";
                    } else {
                        intent = posts[query.delNum][1];
                        posts = readPosts("chatEntity.csv");
                        for (var i=0;i < posts.length; i++ ) {
                            if (posts[i][0] == intent){
                                errorMsg = "インテントを削除するには、対応するエンティティをすべて削除してください。";
                            }
                        }
                        posts = readPosts("chatDialog.csv");
                        for (var i=0;i < posts.length; i++ ) {
                            if (posts[i][0] == intent){
                                errorMsg = "インテントを削除するには、対応するダイアログをすべて削除してください。";
                            }
                        }
                        posts = readPosts("chatIntent.csv");
                    }
                    if (errorMsg == ""){ // エラーがなかったのでアイテム削除
                        posts.splice(query.delNum, 1); // postsからdelNum行を削除
                    }
                } else { // 必要ないが念のため。
                }
                if (errorMsg == ""){
                    text = obj2csv(posts);
                    fs.writeFileSync(__dirname + '/chatIntent.csv', text , 'utf8', function (err) { // ファイルに書込
                    });
                }
                pageWrite(res);
            } else if (url_parts.pathname == "/editEntity"){ // エンティティの編集
                posts = readPosts("chatEntity.csv");
                if (query.intent){ // selectIntentから来た場合
                    intent = query.intent; // グローバル変数intentに代入。
                    errorMsg = " ";
                } else if (query.newItem){ // 新規追加
                    for (i=0;i<query.newItem.length;i++){ // ひらがなかチェック
                        var unicode = query.newItem.charCodeAt(i);
                        if ( unicode<0x3040 || unicode>0x309f ){
                            errorMsg = "エンティティはひらがな(全角)で入力してください";
                        }
                    }
                    for (var i=0;i < posts.length; i++ ) { // 重複チェック
                        if (posts [i][0] == intent && posts[i][1] == query.newItem){
                            errorMsg = "すでに登録されています";
                        }
                    }
                    if (errorMsg == ""){ // エラーがなかったのでアイテム追加
                        posts.push([intent,query.newItem]); // newItemをpostの配列に入れる。
                    }
                } else if (query.delNum){ // 削除
                    if(isNaN(query.delNum)){ // 数値かチェック
                        errorMsg = "数字(半角)を入力してください";
                    }else{ // 選択中のインテントにひもづくエンティティかどうかチェック
                        errorMsg = delChk(query, posts, intent);
                    }
                    if (errorMsg == ""){ // エラーがなかったのでアイテム削除
                        posts.splice(query.delNum, 1); // postsからdelNum行を削除
                    }
                } else { // 必要ないが念の為
                }
                if (errorMsg == ""){ // エラーがなかったらファイルに書き込み
                   text = obj2csv(posts);
                   fs.writeFileSync(__dirname + '/chatEntity.csv', text , 'utf8', function (err) { // ファイルに書込
                       // csvファイルをタブセパレート(tsv)に変換
                       var COMMAND = 'sudo sed -E "s/,/    /g" chatEntity.csv > chatEntity.tsv'; // csvをtsvに変換
                       exec(COMMAND, function(error, stdout, stderr) { 
                           // tsvファイルをjuliusのdic形式に変換
                           var COMMAND = 'iconv -f utf8 -t eucjp chatEntity.tsv | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > chatEntity.dic'; // tsvをdicに変換
                           exec(COMMAND, function(error, stdout, stderr) {
                           });
                       });
                   });
                }
                pageWrite(res);
            } else if (url_parts.pathname == "/editDialog"){ // ダイアログの編集
                posts = readPosts("chatDialog.csv");
                if (query.intent){ // intentを選択した場合の処理。
                    intent = query.intent; // グローバル変数intentに代入。
                    errorMsg = " ";
                } else if (query.newItem){ // 新規追加の場合。重複をチェックする。
                    for (var i=0;i < posts.length; i++ ) {
                        if (posts [i][0] == intent && posts[i][1] == query.newItem){
                            errorMsg = "すでに登録されています";
                        }
                    }
                    if (errorMsg == ""){ // 重複がなかった場合。追加する。
                        posts.push([intent,query.newItem]); // newItemをpostの配列に入れる。
                    }
                } else if (query.delNum){ // 削除
                    if(isNaN(query.delNum)){ // 数字じゃない場合
                        errorMsg = "数字(半角)を入力してください";
                    }else{
                        errorMsg = delChk(query, posts, intent);
                    }
                    if (errorMsg == ""){ // エラーがなかったので削除
                        posts.splice(query.delNum, 1); // postsからdelNum行を削除
                    }
                } else { //必要ないが念の為
                }
                if (errorMsg == ""){ // エラーがなかったらファイルに書き込み
                    text = obj2csv(posts);
                    fs.writeFileSync(__dirname + '/chatDialog.csv', text , 'utf8', function (err) { // ファイルに書込
                    });
                }
                pageWrite(res);
            } else if (url_parts.pathname == "/setTime"){ // 時間設定の保存
                obj_config.data1[0] = qs.parse(req.data);
                fs.writeFile(__dirname + '/data_chat.json', JSON.stringify(obj_config), function (err) {
                });
                pageWrite(res);
            } else { // 該当せず
                res.writeHead(200, {'Content-Type': 'text/html; charset=UTF-8'});
                res.write("NO-POST!!");
                res.end();
                return;
            } // end of if
        }); // end of req on
    } // end of POST request
} // end of doRequest

// ---------------------------------------------------------------------------------------------------------
// IPアドレスの設定
var host = getLocalAddress().ipv4[0].address; // 現在のIPアドレスを取得する。
// var host = 'localhost'         // macやwindows10以降であれば、localhostで指定できる。
// var host = '10.0.0.1'          // IPアドレスの取得がうまくいかない場合は直接指定する。

// サーバーの起動
var server = http.createServer(); // http.serverクラスのインスタンスを作る。戻値はhttp.server型のオブジェクト。
server.on('request', routing);    // serverでrequestイベントが発生した場合のコールバック関数を登録
var port = 3000;                  // portは1024以上の数字なら何でもよい。
server.listen(port, host)         // サーバーを待ち受け状態にする。
console.log ("server is listening at "+host+":"+port);
