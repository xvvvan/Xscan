import sys,time
from tqdm import tqdm
sys.path.append('../')
from plugins.printmsg import *
tasking = 0
class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    # 初始化函数，需要知道总共的处理次数
    def __init__(self,hosts,ports,infoDone = 'Done'):

        self.hosts = hosts
        self.ports = ports
        self.tasks = int(len(self.hosts)*len(self.ports))
        self.infoDone = infoDone
        self.z = 0
        # self.pbar = tqdm(total=int(self.tasks))
        self.max_arrow = 50


    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self):
        tasking = self.z
        tasks = len(self.hosts)*len(self.ports)

        a = int(self.z*100.0 / tasks)
        if self.z is not None:
            self.z += 1

        num_arrow = int(self.z /tasks* 50) #计算显示多少个'>'
        num_line = self.max_arrow - num_arrow #计算显示多少个'-'

        percents = '>'*num_arrow+'-'*num_line+str(a+1) +'%' #计算完成进度，格式为xx.xx%

        percent = percents+'\n'
        if int(self.z*100.0 / tasks)!=a and a%5==0:
            # sys.stdout.write(percents) #这两句打印字符到终端
            # sys.stdout.flush()
            # sys.stdout.write('\r\n')
            printBlue(percents)
            # print("\r[{0}]{1}{2}".format('>'*num_arrow,'-'*num_line,str(a)+'%'),end='',flush=True)
        if self.z >= tasks:
            self.z=tasks

    # def show(self):
    #     self.pbar.update(1)


if __name__ == '__main__':
    hosts=[i for i in range(1000)]
    ports = [p for p in range(10)]
    for t in range(100):
        time.sleep(0.1)
        print('a')
        # if t%5==0:
            # print('\n'+str(t))
            # time.sleep(0.1)
        # process(hosts,ports)


        

