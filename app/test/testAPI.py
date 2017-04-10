import requests
import json

url = "http://127.0.0.1:5000/api"


def test_api():
    header = {
        "content-type": "application/json"
    }
    format_Request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "idc.create",
        "auth": '',
        "params": {
            'name': 'bj-yz',
            'idc_name': '北京亦庄机房',
            'address': '北京亦庄开发区',
            'phone': '13521095342',
            'email': 'cong.liu@wecan-info.com',
            'user_interface': 'LotusChing',
            'user_phone': '13521095342',
            'rel_cabinet_num': 50,
            'pact_cabinet_num': 60
        }
    }
    # 发送测试用的错误数据
    header_err = {
        "content-type": "application/json_err"
    }
    format_Request_err = {
        "jsonRpcVersion": "1.0",
        "id": "2",
        "method": "idc.getIdc_err",
        "auth": "kch",
        "params": {"idcId": "2"}
    }

    print("======发送正常数据测试返回执行结果：======")
    r = requests.post(url, headers=header, data=json.dumps(format_Request))
    print("response的状态：{}".format(r.status_code))
    print("response的内容：{}".format(str(r.content, 'utf-8')))

    # print("======发送错误json元素信息测试返回报错信息：======")
    # r = requests.post(url, headers=header, data=json.dumps(format_Request_err))

    #  print("response的状态：{}".format(r.status_code))
    #print("response的内容：{}".format(str(r.content, 'utf-8')))

    # print("======测试错误头文件测试返回报错信息：======")
    # r = requests.post(url, headers=header_err, data=json.dumps(format_Request_err))

    # print("response的状态：{}".format(r.status_code))
    # print("response的内容：{}".format(str(r.content, 'utf-8')))


def test_idc_get():
    header = {
        "content-type": "application/json"
    }
    format_Request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "idc.create",
        "auth": '',
        "params": {}
    }
    print("======发送正常数据测试返回执行结果：======")
    r = requests.post(url, headers=header, data=json.dumps(format_Request))
    print("response的状态：{}".format(r.status_code))
    print("response的内容：{}".format(str(r.content, 'utf-8')))


if __name__ == '__main__':
    data = test_idc_get()
    print(data)
