# search-g0v

這是 g0v 基礎建設的一個小坑，目標是做一個輕便快速的搜尋器，來取代 hackpad 現在的搜尋介面

好處是：

- 開新的專案、idea 之前，可以快速 review 一下是否有類似的討論或專案
- 找舊東西比較方便
- 不用在不同的平台上重複搜尋
- 搜尋結果不需要無止境的分頁、外連

## 2016/10 新改版

- Jim 將抓 github README, hackfoldr 等 component 都改以像 backup-hackpad 的方式，用新的 repo 定時來處理。未來如果有需要用到這些資料的其他專案，就可以直接連結這些 repo files，取代原本 build.py 的功能

  [hackfoldr]
  - code repo: https://github.com/jmehsieh/hackfoldr-backup
  - data repo: https://github.com/jmehsieh/hackfoldr-backup-g0v

  [repo-info]
  - code repo: https://github.com/jmehsieh/generate-g0v-repo-info
  - data repo: https://github.com/jmehsieh/g0v-repo-info

- Ronnywang 用 elasticsearch 來取代原本的結巴分詞與 whoosh 的 api 功能 

  目前 API 位置在 https://api.search.g0v.io/query.php?q= 


===

### 舊版

現在有以下功能：

### build.py
- 會先在 hackpad-backup-g0v 下面 git submodule update 檢查是否有新的檔案
- 找出所有 hackfoldr 網址，並建立 hackfoldr 內連結「title」(only) 的搜尋索引
- 根據 hackpad-backup-g0v/pads.json 比對上次更新的時間、目前已經索引的檔案，將新增/更動的 html 重新 merge 到索引檔
- 會去抓 g0v, awesome-g0v github 下面所有 repo 的 README.md

### search.py
- 載入索引器後，輸入關鍵字，會找出相關的 github repo & hackfoldr & hackpad id, last modify(commit) time, title

### api.py
- 在 localhost:5000 建立 api, 用 /search?keyword= 來搜尋

### web.py
- 在 http://127.0.0.1:5000/ 用網頁搜尋


接下來要：

- ~~試著將搜尋變成一個 web API~~
- ~~當 hackpad-backup-g0v 更新時，自動觸發 make_index.py~~ 因整合了其他資料，改為每個小時 run 一次
- 優化建立索引檔的效能
- 搜尋關鍵字分析紀錄
- 優化前台介面
- 優化 API
- 優化搜尋速度
- 整合其他資料
  - ~~g0v hackpad~~
  - ~~所有 g0v hackpad 上有公開連結的 hackfoldr~~
  - ~~g0v github readme~~
  - g0v.tw
  - irc/slack log

----

### Installation

    # 安裝相關套件
    pip3 install -r requirements.txt

    # 設定 GitHub API 所需資訊 ( 抓取 g0v-repos 要用)
    #mac 寫在 .bash_profile 後執行 source .bash_profile

    export GITHUB_USER_NAME=<your_github_username>
    export GITHUB_TOKEN=<your_github_token>

    # 下載 子模組的內容 ( hackpad_backup_g0v, build 時會自動更新 )
    git submodule update --init

    # 建立索引
    python3 build.py

    # 透過 command line 搜尋
    python3 search.py

    # 啟動 web server (透過網頁搜尋)
    python3 web.py

最初是根據這篇教學來改的: http://www.jeyzhang.com/realization-of-full-chinese-text-search-using-whoosh-and-jieba.html

### Development

    $ docker-compose run app python3 build.py # build index
    $ docker-compose up # start the api server, go to http://localhost:5000/search?keyword=test to see result


### Change Log

1. 目前只先做到用 jieba 把 https://github.com/g0v-data/hackpad-backup-g0v 所有的 html 做成可搜尋的索引檔案
2. 2016/06/23 新增 api.py 提供 web api
3. 2016/06/23 新增 透過 github api 抓取 g0v github 下的專案 README.md
4. 2016/07/21 新增 aswesome-g0v 下的專案 README.md
5. 2016/07/23 整合 hackfoldr 進索引檔
6. 2016/07/23 專案改名 search-g0v
7. 2016/07/24 前端介面 web.py
8. 2016/10 改版

### Contributors

- ttcat
- allanfann
- andyhorng
- ronnywang

### g0v Slack channel: #search
Join by yourself: http://join.g0v.today/
