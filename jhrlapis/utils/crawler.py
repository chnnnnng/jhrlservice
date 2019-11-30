from bs4 import BeautifulSoup
import time, json, requests, re
from .crypto_rsa.RSAJS import RSAKey
from .crypto_rsa.base64 import Base64 as pB64


class Crawler:

    host = 'www.gdjw.zjut.edu.cn'
    baseurl = 'http://' + host + '/'
    getSessionUrl = baseurl + 'jwglxt/'
    loginurl = baseurl + 'jwglxt/xtgl/login_slogin.html?time='
    publickeyurl = baseurl + 'jwglxt/xtgl/login_getPublicKey.html?time='
    kaptchaurl = baseurl + 'jwglxt/kaptcha?time='
    getkburl = baseurl + 'jwglxt/kbcx/xskbcx_cxXsKb.html'
    jsid = ""
    defaultHeader = {}

    def __init__(self,jsid=''):
        if jsid == '':
            self.jsid = re.search("^(JSESSIONID=)(.*)(; Path=/jwglxt; HttpOnly)$",
                                 requests.get(self.getSessionUrl).headers.get('Set-Cookie')).group(2)
        else:
            self.jsid = jsid
        self.defaultHeader = {'Cookie': 'JSESSIONID=' + self.jsid + '; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1'}


    def getNowTime(self):
        return str(int(round(time.time() * 1000)))

    def getJsid(self):
        return self.jsid

    def getYzm(self):
        return self.baseurl + 'jwglxt/kaptcha?time='

    def getYzmBin(self):
        resl = requests.get(self.getYzm(),headers=self.defaultHeader)
        return resl


    def getYzmHeader(self):
        return self.headers4

    def getEnPassword(self, string, exponent, modulus):
        b64 = pB64()
        exponent = b64.b64_to_hex(exponent)
        modulus = b64.b64_to_hex(modulus)
        rsa = RSAKey()
        rsa.setPublic(modulus, exponent)
        crypto_t = rsa.encrypt(string)
        return b64.hex_to_b64(crypto_t)

    def login(self,username,password,yzm):
        #page = requests.get(self.loginurl + self.getNowTime(), headers=self.defaultHeader)
        #soup = BeautifulSoup(page.text, 'html.parser')
        #csrftoken = soup.find('input', id='csrftoken')['value']
        publickeypage = requests.get(self.publickeyurl + self.getNowTime(), headers=self.defaultHeader)
        publickeyarray = json.loads(publickeypage.text)
        enMm = self.getEnPassword(password, publickeyarray['exponent'], publickeyarray['modulus'])
        formdata = [
            #('csrftoken', csrftoken),
            ('yhm', username),
            ('mm', enMm),
            ('mm', enMm),
            ('yzm', yzm)
        ]
        loginpage = requests.post(self.loginurl + self.getNowTime(), data=formdata, headers=self.defaultHeader,allow_redirects=False)
        loginpagesoup = BeautifulSoup(loginpage.text, 'html.parser')
        if loginpagesoup.find(id="tips") is None:
            newCookie = re.search("^(.*JSESSIONID=)(.*)(; Path=/jwglxt; HttpOnly)$",loginpage.headers.get('Set-Cookie')).group(2)
            return {'status':True ,'data':newCookie}
        else:
            hint = loginpagesoup.find(id="tips").span.next_sibling
            return {'status' : False , 'data' : str(hint).strip()}

    def getKb(self,xn,xq):
        if xq == 1 : xq = 3;
        if xq == 2: xq = 12;
        if xq == 3: xq = 16;
        resl = requests.post(self.getkburl,data={'xnm':xn,'xqm':xq},headers=self.defaultHeader)
        # if not resl['kbList']:
        #     return False
        # else:
        #     return resl
        return resl
