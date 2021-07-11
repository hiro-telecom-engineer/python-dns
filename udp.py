from socket import socket, AF_INET, SOCK_DGRAM
import dns

# バッファサイズ指定
BUFSIZE = 1024


def udp_open(ip_addr, values):
    # 受信側アドレスをtupleに格納
    src_addr = (ip_addr, 53)
    # ソケット作成
    udp_serv_sock = socket(AF_INET, SOCK_DGRAM)
    # 受信側アドレスでソケットを設定
    udp_serv_sock.bind(src_addr)
    print("サーバ起動")
    # While文を使用して常に受信待ちのループを実行
    while True:
        # ソケットにデータを受信した場合の処理
        # 受信データを変数に設定
        data, addr = udp_serv_sock.recvfrom(BUFSIZE)
        # 受信を出力
        print(data, addr)
        # 受信データチェック
        result, res = dns.chk_data(data)
        # 送信データを出力
        print(result, res)
        if result:
            udp_serv_sock.sendto(res, addr)
            print(res)
