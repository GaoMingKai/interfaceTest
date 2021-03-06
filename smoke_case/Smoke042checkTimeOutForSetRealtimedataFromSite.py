__author__ = 'sophia'
import unittest
import sys
from interfaceTest.Methods.BeopTools import BeopTools
from interfaceTest import app
import time, datetime
import json


class Smoke042(unittest.TestCase):
    testCaseID = 'Smoke042'
    projectName = "无"
    buzName = '检测后台更新历史数据接口是否超时'
    start = 0.0
    now = 0
    startTime = ""
    errors = []
    timeout = 60
    serverip = app.config['SERVERIP']
    url = "http://%s/admin/dataPointManager/search/" % serverip
    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger = BeopTools.init_log(r'%s\log\%s.txt' % (sys.path[0], self.testCaseID))

    def Test(self):
        self.errors = []
        try:
            data = {"projectId":72,"text":None,"isAdvance":False,"order":"pointname asc","isRemark":False,"flag":0,"starred":"","page_size":200,"current_page":1}
            #data={"projectId":72,"text":"timeout_","isAdvance":False,"order":"time desc","isRemark":False,"flag":0,"starred":"","page_size":500,"current_page":1}
            rv = BeopTools.postJsonToken(self.url, data, t=self.timeout)
            print(rv)
            rv=rv.get("list",0)
            if(rv):
                for r in rv:
                    value_time=r.get('time',0)
                    pointname=r.get("pointname",0)
                    pointvalue=r.get("pointvalue",0)
                    value_time= datetime.datetime.strptime(value_time,'%Y-%m-%d %H:%M:%S')
                    now=datetime.datetime.now()
                    if now>value_time:
                        deltimes = now-value_time
                    else:
                        deltimes = value_time - now
                    if deltimes.seconds>20*60 and now.day==value_time.day or deltimes.seconds>20*60 and now.day!=value_time.day:
                        self.errors.append("错误信息项目%s更新历史数据接口在%s时超时(%s秒)" % (pointname,str(value_time),pointvalue))
                    else:
                        break
            else:
                self.errors.append("错误信息接口:%s 数据:%s 预期有值,实际返回为%s" % (self.url, json.dumps(data),rv))


        except Exception as e:
            self.errors.append("错误信息接口:%s 数据:%s  ,异常信息: %s" % (self.url, json.dumps(data), e.__str__()))
        BeopTools.raiseError(self.errors, self.testCaseID)

    def tearDown(self):
        self.errors = []
        use1 = str((datetime.datetime.now() - self.start).seconds)
        use = use1 + "s"
        print("本次用例执行时间为%s" % use)
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Smoke042('Test'))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
