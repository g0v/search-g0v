# search-hackpad-g0v

這是 g0v 基礎建設的一個小坑，目標是做一個輕便快速的搜尋器，來取代 hackpad 現在的搜尋介面

好處是：

- 開新的專案、idea 之前，可以快速 review 一下是否有類似的討論或專案
- 找舊東西比較方便
- 不用在不同的平台上重複搜尋
- 搜尋結果不需要無止境的分頁、外連


最終希望是將這些都即時索引起來：

- g0v hackpad
- 所有 g0v hackpad 上有公開連結的 hackfoldr
- g0v github readme
- g0v.tw
- irc/slack log

### 目前進度

1. 目前只先做到用 jieba 把 https://github.com/g0v-data/hackpad-backup-g0v 所有的 html 做成可搜尋的索引檔案
2. 2016/6/23 新增 api.py 提供 web api
3. 2016/6/23 新增 透過github api 抓取 g0v 帳號下的專案資訊


現在有以下功能：

### make_index.py
- 會先在 hackpad-backup-g0v 下面 git submodule update 檢查是否有新的檔案
- 根據 hackpad-backup-g0v/pads.json 比對上次更新的時間、目前已經索引的檔案，將新增/更動的 html 重新 merge 到索引檔

### search.py
- 載入索引器後，輸入關鍵字，會找出相關的 hackpad id, last modify(commit) time, title

接下來要：

- 試著將搜尋變成一個 web API
- 當 hackpad-backup-g0v 更新時，自動觸發 make_index.py
- 整合其他資料

----


### Installation

    # 安裝相關套件
    pip3 install -r requirements.txt

    # 設定 GitHub API 所需資訊 ( 抓取 g0v-repos 要用)
    export GITHUB_USER_NAME=<your_github_username>
    export GITHUB_TOKEN=<your_github_token>

    # 下載 子模組的內容 ( search-hackpad-gov )
    git submodule update --init

    # 建立索引
    python3 make_index.py
    python3 make_index_2.py

    # 進行搜尋 目前搜尋的入口是分開的 未來將整合再一起

    # 搜尋 hackfoldr
    python3 search.py

    # 搜尋 g0v-repos
    python3 search2.py

根據這個教學來改的: http://www.jeyzhang.com/realization-of-full-chinese-text-search-using-whoosh-and-jieba.html


### Contributors

- ttcat
- allanfann
- andyhorng
