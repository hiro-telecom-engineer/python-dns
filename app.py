# coding: utf -8
import PySimpleGUI as sg  # ライブラリの読み込み
import udp
import dns
import threading
import sys

# テーマの設定
sg.theme("SystemDefault ")

# ドメイン設定
L1 = [
    # ドメイン設定1
    [sg.Text("・ドメイン1 "),
     sg.InputText(default_text="dns.test1.jp", text_color="#000000", background_color="#ffffff", size=(25, 1), key="domain1"),
     sg.Text("・IPアドレス "),
     sg.InputText(default_text="127.0.0.2", text_color="#000000", background_color="#ffffff", size=(15, 1), key="ip1")],
    # ドメイン設定2
    [sg.Text("・ドメイン2 "),
     sg.InputText(default_text="dns.test2.jp", text_color="#000000", background_color="#ffffff", size=(25, 1), key="domain2"),
     sg.Text("・IPアドレス "),
     sg.InputText(default_text="127.0.0.3", text_color="#000000", background_color="#ffffff", size=(15, 1), key="ip2")],
    # ドメイン設定3
    [sg.Text("・ドメイン3 "),
     sg.InputText(default_text="dns.test3.jp", text_color="#000000", background_color="#ffffff", size=(25, 1), key="domain3"),
     sg.Text("・IPアドレス "),
     sg.InputText(default_text="127.0.0.4", text_color="#000000", background_color="#ffffff", size=(15, 1), key="ip3")]]

# DNSサーバ設定
L2 = [
    [sg.Text("・DNSドメイン "),
     sg.InputText(default_text="dns.test_domain.jp", text_color="#000000", background_color="#ffffff", size=(25, 1), key="domain4"),
     sg.Text("・IPアドレス "),
     sg.InputText(default_text="127.0.0.1", text_color="#000000", background_color="#ffffff", size=(15, 1), key="ip4")],
    [sg.Button("DNSサーバ起動", border_width=4, size=(15, 1), key="btn_udp_open")]]

L = [[sg.Frame("応答ドメイン設定", L1)],
     [sg.Frame("DNSサーバ設定", L2)]]

# ウィンドウ作成
window = sg.Window("DNS_SERVER ", L)


def main():
    # イベントループ
    while True:
        # イベントの読み取り（イベント待ち）
        event, values = window.read()
        # 確認表示
        print(" イベント:", event, ", 値:", values)
        # 終了条件（ None: クローズボタン）
        if event == "btn_udp_open":
            dns.dns_init(values)
            print("DNSサーバ起動")
            # スレッド制御
            thread1 = threading.Thread(target=udp.udp_open, args=(values["ip4"], values,))
            thread1.setDaemon(True)
            thread1.start()
        elif event is None:
            break
    # 終了処理
    window.close()


if __name__ == '__main__':
    main()
