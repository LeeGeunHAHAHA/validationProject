#!/usr/bin/env python3
import argparse
import sys
import os
from subprocess import call
from random import *

LIMIT_SIZE = 2048
NSZE = 65536 #0X10000
port = open("/iport0/port", 'w')


def vfEnable(port, target, target2, numvf):
    target = open("./iport"+port+"/target"+target,'w')
    target.write("NumVFs="+numvf)
    if(target2 != ""):
        target2 = open("./iport"+port+"/target"+target2,'w')
        target2.write("NumVFs="+numvf)



def makeQueue():
    queuetarget=0

    for looptarget in range(starttarget, endtarget2):
        #for VF
        if(looptarget <= endtarget):
            targetN_file = open("./iport"+port+"/target"+looptarget,'w')
            targetN_file.write("QueueCount="+queuecnt)
            targetN_file.write("QueueDepth="+queuedepth)
            targetN_file.write("QueueAlignment=0")
            nvme_file.write("restart="+looptarget)

        #for PF
        else:
            if(looptarget == endtarget+1):
                queuetarget = target
            else:
                queuetarget = target2

            queuetarget_file = open("./iport"+port+"/target"+queuetarget,'w')
            queuetarget_file.write("QueueCount="+queuecnt)
            queuetarget_file.write("QueueDepth="+queuedepth)
            queuetarget_file.write("QueueAlignment=0")
            nvme_file.write("restart="+queuetarget)




def Random_test(method,start_target,end_target,limit_size):
        nsze = NSZE
        randomSize = 0
        total = 0
        end_cnt = 0
        sizeArr = []
        if(end_target == 29):
                print("ok")
                end_cnt = 32   # dual
        else:
                end_cnt = 16    # single
        for target_cnt in range(end_cnt,0,-1):
            tmp = nsze/target_cnt
            randomSize = randint(int(tmp*0.8),int(tmp*1.3))
            nsze -= randomSize
            total += randomSize
            sizeArr.append(randomSize)

        for target_cnt in range(start_target, end_target+1):
            target = open("/iport0/target" + str(target_cnt), 'w')

            port.write("Testlimits="+str(sizeArr[target_cnt])+","+str(sum(sizeArr[:target_cnt]))+",0")
            target.write("WriteEnabled=1")
            target.write(method+str(target_cnt)+",1,1,0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0")

#       if(sum > 65536):
#           sizeArr[-1] = 65536-(sum-sizeArr[-1])


def Sequential_test(method,start_target,end_target,limit_size):

        loop_cnt = 0
        for target_cnt in range(start_target, end_target+1):
                target = open("/iport0/target"+str(target_cnt), 'w')
                port.write("Testlimits="+str(limit_size)+","+str(loop_cnt * limit_size)+",0")
                target.write("WriteEnabled=1")
                target.write(method+str(target_cnt)+",1,1,0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0")

                loop_cnt += 1

def main():
    try :
        parser = argparse.ArgumentParser(add_help = "True",description = "run test virtual function in auto")
        parser.add_argument("start_target", type= int, action="store", nargs=1,\
                help = "starting controller number (integer)")
        parser.add_argument("end_target", type= int,\
                default=[int(sys.argv[1])if sys.argv[1] != '-h' and sys.argv[1] !="--help" else 0], action="store", nargs="*", \
                help = "end controller number (integer)")
        parser.add_argument("limit_size", type= int, default=[LIMIT_SIZE], action="store", nargs="*", \
                help="limit_size for test(integer)")
        parser.add_argument("--Random", "-R", action="store_true", dest="random_test", required=False,\
                help="modify test method if use this arg, test will be done in radom way.")
        parser.add_argument("--read", "-r", action="store_true", dest="read", required=False,\
                help = "decide test method. default is compare. if you use this arg, test will be read test.")
        parser.add_argument("--write", "-w", action="store_true", dest="write", required=False,\
                help="decied test method. default is compare. if you use this arg, test will be write test.")
        given_args=parser.parse_args()

        start_target = given_args.start_target[0]
        end_target = given_args.end_target[0]
        limit_size = given_args.limit_size[0]
        random_test = given_args.random_test
        read = given_args.read
        write = given_args.write
        target = start_target
        method = "Compare_"
        if read :  method = "Read_"
        elif write : method = "Write_"


        target = open("/iport"+port+"target"+target)
        if(random_test):
                Random_test(method, start_target,end_target,limit_size)
        else:
                Sequential_test(method, start_target,end_target,limit_size)

    except:
        print("This command is not available. Please use -h or --help option")


if __name__ == "__main__":
        main()
