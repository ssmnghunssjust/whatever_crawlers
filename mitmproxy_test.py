# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mitmproxy_test.py 
   Description :   None
   Author :        LSQ
   date：          2020/9/15
-------------------------------------------------
   Change Activity:
                   2020/9/15: None
-------------------------------------------------
"""
from mitmproxy import ctx
from mitmproxy.http import HTTPFlow


class SoJson(object):
    def __init__(self):
        pass

    # def request(self, flow: HTTPFlow):
    #     if flow.request.host != 'https://www.sojson.com/':
    #         return

    def response(self, flow:HTTPFlow):
        if flow.request.url == 'https://www.sojson.com/':
            text = flow.response.get_text()
            text = text.replace(r"function _0xeb8d24(_0x50ceb9){var _0x22f581={'ADylx':function _0x1081de(_0x1667c9,_0x303976){return _0x1667c9!==_0x303976;},'CqweQ':_0x4a9a('0x11f','uU]2'),'TixCu':function _0x2083ca(_0x35db3a,_0x35100c){return _0x35db3a===_0x35100c;},'MTZbs':_0x4a9a('0x120','5yDQ'),'RrFzv':'pgk','RAizZ':_0x4a9a('0x121','aRgz'),'DZYUq':'function\x20*\x5c(\x20*\x5c)','NIOsy':function _0xa0e87d(_0x88d214,_0x71af77){return _0x88d214(_0x71af77);},'VxKAW':function _0x4aa97c(_0x2aaf92,_0x55b612){return _0x2aaf92+_0x55b612;},'fzxRC':_0x4a9a('0x122','dVUy'),'VtJUq':function _0x179145(_0x255dd3,_0x24a1d7){return _0x255dd3+_0x24a1d7;},'IhmqO':function _0x5fb353(_0x8fa4ea){return _0x8fa4ea();},'zOfva':function _0x41469f(_0xe49d0d){return _0xe49d0d();},'UaZTa':function _0x1dcf25(_0x1186dd,_0x45170a){return _0x1186dd!==_0x45170a;},'iBDyo':_0x4a9a('0x123','h8us'),'GRAPx':function _0x213aa2(_0x55e70d,_0x1eaaa1){return _0x55e70d%_0x1eaaa1;},'Csfmy':function _0x1598d9(_0x3ec62e,_0x39c1d7){return _0x3ec62e===_0x39c1d7;},'TnxkC':_0x4a9a('0x124','yxcB'),'jhjlk':function _0x477833(_0x1f6fe8,_0x1b0b58){return _0x1f6fe8(_0x1b0b58);}};if(_0x22f581['ADylx']('YSJ',_0x22f581['CqweQ'])){}else{if(_0x22f581['TixCu'](typeof _0x50ceb9,_0x22f581['MTZbs'])){if(_0x22f581[_0x4a9a('0x125','ohxW')]===_0x22f581['RAizZ']){var _0x4a27ae=new RegExp(_0x22f581[_0x4a9a('0x126','T6M[')]);var _0x487537=new RegExp(_0x4a9a('0x127','ftNe'),'i');var _0x194148=_0x22f581[_0x4a9a('0x128','aRgz')](_0x37ca1b,'init');if(!_0x4a27ae['test'](_0x22f581[_0x4a9a('0x129','diqm')](_0x194148,_0x22f581[_0x4a9a('0x12a','C2PO')]))||!_0x487537['test'](_0x22f581[_0x4a9a('0x12b','pYIH')](_0x194148,_0x4a9a('0x12c','RTsc')))){_0x22f581[_0x4a9a('0x12d','zVH)')](_0x194148,'0');}else{_0x22f581['IhmqO'](_0x37ca1b);}}else{var _0x1edb84=function(){var _0x2451e4={'NjoNx':function _0x2380e8(_0x43d91b,_0x3231d7){return _0x43d91b===_0x3231d7;},'syXTz':_0x4a9a('0x12e','C2PO')};if(_0x2451e4['NjoNx']('RfZ',_0x2451e4['syXTz'])){while(!![]){}}else{Vso['editor'][_0x4a9a('0x12f','zVH)')](_val);}};return _0x22f581[_0x4a9a('0x130','F(]2')](_0x1edb84);}}else{if(_0x22f581['UaZTa'](_0x22f581['VtJUq']('',_0x50ceb9/_0x50ceb9)[_0x22f581[_0x4a9a('0x131','QJT#')]],0x1)||_0x22f581[_0x4a9a('0x132','RTsc')](_0x22f581['GRAPx'](_0x50ceb9,0x14),0x0)){if(_0x22f581[_0x4a9a('0x133','ojiy')]('Tyv',_0x22f581['TnxkC'])){return __2089[_1366[0x1]]('')[_1366[0x2]]()[_1366[0x3]]('');}else{return;}}else{return;}}}}",
                                "")   # "_0x22f581['jhjlk'](_0xeb8d24,_0x50ceb9);"
            text = text.replace('debugger;', 'return;')
            flow.response.set_text(text)

addons = [SoJson()]
