# 固定値
DOMAINNAME = "c00c"
QLASS = "0001"
TTL = "0000ffff"
FLAG = "8180"
# DNS情報テーブル
dns_tbl = []


def dns_init(values):
    global dns_tbl
    # DNS情報初期化
    dns_tbl = [(DnsInfo(values["ip1"], values["domain1"])),
               (DnsInfo(values["ip2"], values["domain2"])),
               (DnsInfo(values["ip3"], values["domain3"])),
               (DnsInfo(values["ip4"], values["domain4"]))]


# 取得データ解析
def chk_data(data):
    global dns_tbl
    result = False
    response = ""
    data2 = []
    # Question取得
    qtype, qname = get_question(data)
    # 問い合わせに合致する情報の有無を検索
    for i in range(len(dns_tbl)):
        result = dns_tbl[i].chk_question(qtype, qname)
        if result:
            tbl_index = i
            break
    # 検索成功時はレスポンス取得
    if result:
        # 受信データのフラグ、ANCOUNTを応答へ設定
        data2 = data[:2] + bytes.fromhex(FLAG) + data[4:6] + bytes.fromhex("0001") + data[8:]
        response = data2 + dns_tbl[tbl_index].get_answer(qtype)
    return result, response


# Question取得
def get_question(data):
    # 先頭12byte切り捨て
    chk_data = data[12:]
    index = 0
    # QNAME取得
    qname = []
    for i in range(len(chk_data)):
        # データ長分リストにデータを格納
        if 0 != chk_data[index]:
            size = chk_data[index] + 1
            qname.append(chk_data[index + 1:index + size].decode())
            index += size
        else:
            # 末尾0x00で抜ける
            break
    # QTYPE取得
    qtype = chk_data[index + 1:index + 3].hex()

    return qtype, qname


# アドレス解決クラス
class DnsInfo:
    ipaddr = ""
    domain = ""
    response = ""

    # 初期化
    def __init__(self, ipaddr, domain):
        self.ipaddr = ipaddr.split(".")
        self.domain = domain.split(".")
        return

    # Question取得
    def chk_question(self, qtype, qname):
        result = True
        if qtype == "000c":
            # IP問い合わせ
            for i in range(len(self.ipaddr)):
                if self.ipaddr[int(i)] != qname[int(3 - i)]:
                    result = False
                    break
        elif qtype == "0001":
            # ドメイン問い合わせ
            for i in range(len(self.domain)):
                if self.domain[i] != qname[i]:
                    result = False
                    break
        else:
            result = False

        return result

    def get_answer(self, qtype):
        res = ""
        rdata = b""
        rdata_len = 0
        data = DOMAINNAME + qtype + QLASS + TTL
        res = bytes.fromhex(data)
        if qtype == "000c":
            # RDATA作成
            for i in range(len(self.domain)):
                rdata += len(self.domain[i]).to_bytes(1, 'big')
                rdata_len += len(self.domain[i]) + 1
                rdata += self.domain[i].encode()
            # RLENGTGH追加
            res += rdata_len.to_bytes(2, 'big')
            res += rdata
            res += b"\x00"
        else:
            for i in self.ipaddr:
                rdata += int(i).to_bytes(1, 'big')
            res += len(self.ipaddr).to_bytes(2, 'big')
            res += rdata
            res += b"\x00"
        return res
