# はじめに 
まず初めに下記のgit cloneを実行します。  
git clone git@github.com:akashima/googlegroup.git  
  
install.shを実行し、必要なパッケージをインストールします。  
  
sh ./install.sh  
 
# 動作環境  
OS:Windows, Mac, Linux(ただし、認証でブラウザが必要)   
Language:Python2系
  
# スクリプトの説明  
- GroupMemberList.py	: Google Groupsの全Groupを取得し、excludes.csvに保存します。  
- GroupMemberUserList.py: Google Groupsの全Groupから全ユーザを取得し、GroupMemberUserList.csvに保存します。  
- GroupMemberDelete.py	: deletemail.csvに書かれたメールアドレスを全Groupから削除します。（excludes.csvに除外したいメールアドレスを複数行記述することで除外します)    
- GroupMemberAdd.py	: addgroup.csvで指定されたグループにaddmail.csvを追加します(いずれのファイルも複数行に書くことが可能ですが、addgroup.csvで指定したグループにaddmail.csvをまとめて追加します)   
- GroupMemberAddCSV.py	: addmaillist.csvの1行目で指定されたグループに2行目に指定されているメールアドレスを追加します  

# csvファイルの説明  
- addgroup.csv		: Google GroupのGroupに追加する一覧。複数行指定。  
- addmail.csv		: Google Groupに追加するメールアドレス一覧。複数行指定。  
- addmaillist.csv	: Google Groupに追加するメールアドレス一覧。複数行指定。  
- excludes.csv		: Google Groupから削除する除外一覧。複数行指定。  
- deletemail.csv	: Google Groupから削除するメールアドレス一覧。複数行指定。  
- GroupMemberUserList.csv: 全グループから全ユーザ情報を出力した一覧。  

# 使い方  
1. 各pythonスクリプトを実行します  
ex.)   
python2 GroupMemberList.py --noauth_local_webserver  
2. 実行することによって表示されたURLをブラウザから実行します。  
3. Googleの認証画面が表示されるので、example.comのメアドで認証します。  
4. 実行したpythonアプリに対して許可を求められるので許可します。  
5. ログインや許可に成功するとverification codeが発行されるので、コピペします。  
6. Enterkeyを押せば実行されます。  
 
