import requests
import json
import execjs

js = r"""
var i = "320305.131321201"
 
function n(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a), a = "+" === o.charAt(t + 1) ? r >>> a : r << a, r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}
 
function e(r) {
    var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
    if (null === o) {
        var t = r.length;
        t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
    } else {
        for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++) "" !== e[C] && f.push.apply(f, a(e[C].split(""))), C !== h - 1 && f.push(o[C]);
        var g = f.length;
        g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
    }
    var u = void 0, l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
    u = null !== i ? i : (i = window[l] || "") || "";
    for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
        var A = r.charCodeAt(v);
        128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
    }
    for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++) p += S[b], p = n(p, F);
    return p = n(p, D), p ^= s, 0 > p && (p = (2147483647 & p) + 2147483648), p %= 1e6, p.toString() + "." + (p ^ m)
}

"""

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "BIDUPSID=5FC0306C286AE4DF6602124CBA58DF38; PSTM=1545268744; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=5FC0306C286AE4DF6602124CBA58DF38:SL=0:NR=10:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=130610_126887_128700_131777_130510_131964_130164_120175_132051_131602_131908_118885_118871_118841_118834_118788_130762_131649_131577_131536_131534_131529_130222_131295_131871_131390_129564_107318_131796_131393_130128_131873_130569_131195_117335_130347_117429_131241_130076_129652_131247_127024_131435_132120_131035_132090_131045_130990_129646_124030_130828_131423_131168_110085_131570_127969_131358_123290_131955_131034_127416_130725_131264_131263_130987_131037_128806; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1557996584; H_PS_PSSID=1459_21090_29064_28518_28775_28722_28963_28839_28584_28703; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1557796478,1557882814,1557969767,1558053453; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1558053453; yjs_js_security_passport=c083c0edacca33ac66044322ca33032b01d07272_1558053461_js; delPer=0; PSINO=6; locale=zh; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22swe%22%2C%22text%22%3A%22%u745E%u5178%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D",
    "Origin": "http://fanyi.baidu.com",
    "Pragma": "no-cache",
    "Referer": "http://fanyi.baidu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def langdetect(text):
    data = {"query": text}
    url = "https://fanyi.baidu.com/langdetect"
    result = requests.post(url, headers=headers, data=data)
    ret = json.loads(result.content.decode())
    return ret['lan']


data = {
    "from": "",
    "to": "",
    "query": "",
    "transtype": "translang",
    "simple_means_flag": "3",
    "sign": "",
    "token": "59c5a408677de6df12490bd561080159"
}

url = "https://fanyi.baidu.com/v2transapi"

while True:
    text = input("请输入要翻译的内容，按q键退出\n")
    if text == "q":
        break
    lan = langdetect(text)
    data['from'] = lan
    data['to'] = "en" if lan == "zh" else "zh"
    sign = execjs.compile(js).call("e", text)
    data['sign'] = sign
    data['query'] = text
    response = requests.post(url, headers=headers, data=data)
    ret = json.loads(response.content.decode(), encoding="utf8")
    print(ret['trans_result']['data'][0]['dst'])
