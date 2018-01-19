#!/bin/bash
#multi-function IO test

#argument input are initialized to null
port=
target=
target2=
numvf=
starttarget=
endtarget=
runtime=
queuecnt=
queuedepth=
typesplit=
limitsize=
iotype=
acctype=
blocksize=

#internal variable are initialized to
declare -a arg
arg_num=0
i=0
loopcnt=0
sum=0
looptarget=0
position=0
lun=1
endtarget2=0

#default value in case argument isn't set
NUMVF=1
QUEUECNT=1
QUEUEDEPTH=1024
SPLIT=0
LIMITSIZE=2048 #should be modified to get from ID-NS
IOTYPE=0
ACCTYPE=1
BLOCKSIZE=1
MAXLBA=65536 #should be modified to get from ID-NS
SCRIPTTEST=0

d=`date +"%b_%d_%H:%M:%S"`
#d=`date`
PID=
HOMEDIR="$( cd "$( dirname "$0" )" && pwd )"
LOGDIR=${HOMEDIR}/"log"
TESTNAME=$(basename $0)
TESTSUITE="$2"
HOME=`pwd`
DAEMON=${HOMEDIR}/${TESTNAME}
PIDDIR=${HOMEDIR}
PIDFILE=${HOMEDIR}/pid
LOCKFILE=${HOMEDIR}/lock
LOGFILE=${DAEMON}.log
PERFFILE=${LOGDIR}/"Perf_${d}.csv"
LUNDIR=`echo ${HOMEDIR} |awk -F'/tests'  '{ print $1 }'`

# Initialize variables
#test run time in seconds
#runtime=10s
qd=4
#test polling interval in seconds
poll=10
#variable to store test status
teststatus=0
name=0
testtype=0
seek=0
seek_string=0
xfer=0
declare -a testname

doLog() {
    local d=`date +"%a %b %d %H:%M:%S %Y"`
    echo ${d} "$@" >> ${LOGFILE}
}

doEcho() {
    echo "$@"
}

doLogEcho(){
        doLog "$@"
        doEcho "$@"
}

doPerf() {
    echo "$@" >> ${PERFFILE}
}

usage() {

        printf " Usage:\n"
        printf " Multi-Function.sh [-p P] [-t T] [-u U] [-r Rs] [-c C] \n"
        printf " -p Port to test (Required)\n"
        printf " -t Target of Physical Function (Required)\n"
        printf " -u Target2 of Physical Function for Dual Port\n"
        printf " -r Run Time for I/O <Ex>10s\n"
        printf " -c Number of Queue Count\n"
        printf " -d Number of Queue Depth\n"

}

getArgs() {

        doLogEcho "============== Get Argumnet ============== "

        for (( i=0; i<$arg_num; i++ ))
        do

                if [ ${arg[$i]} == "-hh" ]; then
                        usage
                        exit 0
                fi

                if [ ${arg[$i]} == "-p" ]; then
                        port=${arg[$i+1]}
                elif [ ${arg[$i]} == "-t" ]; then
                        target=${arg[$i+1]}
                elif [ ${arg[$i]} == "-u" ]; then
                        target2=${arg[$i+1]}
                elif [ ${arg[$i]} == "-n" ]; then
                        numvf=${arg[$i+1]}
                elif [ ${arg[$i]} == "-s" ]; then
                        starttarget=${arg[$i+1]}
                elif [ ${arg[$i]} == "-e" ]; then
                        endtarget=${arg[$i+1]}
                elif [ ${arg[$i]} == "-r" ]; then
                        runtime=${arg[$i+1]}
                elif [ ${arg[$i]} == "-c" ]; then
                        queuecnt=${arg[$i+1]}
                elif [ ${arg[$i]} == "-d" ]; then
                        queuedepth=${arg[$i+1]}
                elif [ ${arg[$i]} == "-y" ]; then
                        typesplit=${arg[$i+1]}
                #elif [ ${arg[$i]} == "-l" ]; then
                #       limitsize=${arg[$i+1]}
                elif [ ${arg[$i]} == "-o" ]; then
                        iotype=${arg[$i+1]}
                elif [ ${arg[$i]} == "-a" ]; then
                        acctype=${arg[$i+1]}
                elif [ ${arg[$i]} == "-z" ]; then
                        blocksize=${arg[$i+1]}
                fi
        done

        if [ "${port}" == "" ] || [ "${target}" == "" ]; then
                doLogEcho "You should set Port Number & Target Number"
                exit 0
        fi
        if [ "${queuecnt}" == "" ]; then
                queuecnt=$QUEUECNT
                doLogEcho "Queue count is set by default(%d)\n" "$queuecnt"
        fi
        if [ "${queuedepth}" == "" ]; then
                queuedepth=$QUEUEDEPTH
                doLogEcho "Queue Depth is set by default(${queuedepth})}"
        fi

        maxblock="-1"
        result=`grep blocks /iport${port}/target${target}lun1`
        re="([0-9]*) blocks"
        if [[ $result =~ $re ]]; then
                maxblock=${BASH_REMATCH[1]}
        fi

}

vfInit() {

        doLogEcho "============== VF Initialize  ============== "
        doLogEcho "Number of VF = 0"
        echo NumVFs=0 >/iport$port/target$target

        if [ "${target2}" != "" ]
        then
                doLogEcho "Number of VF = 0 of target${target2}"
                echo NumVFs=0 >/iport$port/target$target2
        fi

}
vfEnable() {


        doLogEcho "============== VF Enable ============== "
        doLogEcho "Number of VF = ${numvf}"

        doLog "VF Enalbe of target${target}"
        echo NumVFs=${numvf} >/iport$port/target$target

        if [ "${target2}" != "" ]
        then
                doLogEcho "VF Enalbe of target${target2}(Port1) for Dual Port"
                echo NumVFs=${numvf} >/iport$port/target$target2
        fi
}

makeQueue() {

        queuetarget=0

        if [ $SCRIPTTEST -eq 0 ]
        then
                doLogEcho "============== Make Queue =============="
                if [ "${target2}" != "" ]
                then    #for Dual Port
                        endtarget2=`expr ${endtarget} \+ 2`
                else    #for Single Port
                        endtarget2=`expr ${endtarget} \+ 1`
                fi
        else
                endtarget2=${endtarget}
        fi

        if [ $SCRIPTTEST -eq 0 ]
        then
                for (( looptarget=${starttarget}; looptarget<=${endtarget2}; looptarget++ ))
                do
                        #for VF
                        if [ ${looptarget} -le ${endtarget} ]
                        then
                                echo QueueCount=$queuecnt >/iport$port/target$looptarget
                                echo QueueDepth=$queuedepth >/iport$port/target$looptarget
                                echo QueueAlignment=0 >/iport$port/target$looptarget
                                echo restart=$looptarget >/proc/vlun/nvme
                                doLogEcho "Change QueueSize of Target=$looptarget"
                        #for PF
                        else
                                if [ ${looptarget} == `expr ${endtarget} \+ 1` ]
                                then
                                        queuetarget=${target}
                                else
                                        queuetarget=${target2}
                                fi
                                echo QueueCount=$queuecnt >/iport$port/target$queuetarget
                                echo QueueDepth=$queuedepth >/iport$port/target$queuetarget
                                echo QueueAlignment=0 >/iport$port/target$queuetarget
                                echo restart=$queuetarget >/proc/vlun/nvme
                                doLogEcho "Change QueueSize of Target=$queuetarget"
                        fi

                done

        fi

}

#function to get the status of a test. return 0 if running, 1 if passed, -1 if failed
GetTestStatus()
{
        name=$1
        doLogEcho "Checking status for test $name"
        if ls /iport$port/tests/ | grep ${name}$
        then
                if grep -q "Failed" /iport$port/tests/$name
                then
                        teststatus=-1
                elif grep -q "Passed" /iport$port/tests/$name
                then
                        teststatus=1
                else
                        teststatus=0
                fi
        else
                doLogEcho "Test doesn't exist! It likely failed to start. Check /var/log/messages for details."
                teststatus=-1
        fi
}

statuscheck() {

        doLogEcho "============== Check Status for I/O ============== "
        if [ "${target2}" != "" ]
        then    #for Dual Port
                endtarget2=`expr ${endtarget} \+ 2`
        else    #for Single Port
                endtarget2=`expr ${endtarget} \+ 1`
        fi

        for (( looptarget=${starttarget}; looptarget<=${endtarget2}; looptarget++ ))
        do
               GetTestStatus ${testname[$looptarget]}
               #doLogEcho "teststatus is $teststatus"
               while [ $teststatus -eq 0 ]
               do
                       doLogEcho "Test is still running. Sleeping $poll before polling again"
                       if [ ${looptarget} == ${starttarget} ] || [ $teststatus -eq 0 ]
                       then
                           sleep $poll
                       fi
                       GetTestStatus ${testname[$looptarget]}
               done

               if [ $teststatus -eq 1 ]
               then
                       doLogEcho "PASS : Test is passed"
               else
                       doLogEcho "ERROR: Test is failed"
               fi
        done

}

perflog() {

        local int_label="Target "
        local int_iops="IOPS    "
        local int_mbps="MB/s    "

        doLogEcho "============== Check Status for I/O ============== "
        if [ "${target2}" != "" ]
        then    #for Dual Port
                endtarget2=`expr ${endtarget} \+ 2`
        else    #for Single Port
                endtarget2=`expr ${endtarget} \+ 1`
        fi


        for (( looptarget=${starttarget}; looptarget<=${endtarget2}; looptarget++ ))
        do

                if [ ${looptarget} -le ${endtarget} ]; then
                        looptarget2=${looptarget}
                        log_func="VF${looptarget}"
                else
                        if [ $looptarget == `expr $endtarget \+ 1` ]; then
                                looptarget2=${target}
                                log_func="PF0"
                        else
                                looptarget2=${target2}
                                log_func="PF1"
                        fi
                fi

                iops="-1"
                result=`grep [0-9]/sec /iport${port}/tests/${testname[$looptarget]}`
                re="([0-9]*.[0-9]*)/sec"
                if [[ $result =~ $re ]]; then
                        iops=${BASH_REMATCH[1]}
                fi

                mbps="-1"
                result=`grep MB/sec /iport${port}/tests/${testname[$looptarget]}`
                re="([0-9]*.[0-9]*) MB/sec"
                if [[ $result =~ $re ]]; then
                        mbps=${BASH_REMATCH[1]}
                fi

                if [ $looptarget == 0 ]; then
                        doPerf "NumVF=${numvf}_${testtype}${xfer}${seek_string}${runtime}"
                fi
                int_label="${int_label} ${log_func}"
                int_iops="${int_iops}   ${iops}"
                int_mbps="${int_mbps}   ${mbps}"

        done

        doPerf ${int_label}
        if [ $seek == 0 ]; then
                doPerf ${int_mbps}
        else
                doPerf ${int_iops}
        fi

}

arg_num=$#
arg=( "$@" )

#get Argument for VF I/O testing
getArgs

#vfInit
echo TestLimits=0,0,0 >/iport$port/port

for numvf in 1 #3 7 15
do
        #VF Enable. Number of VF is set from argument
        vfEnable

        starttarget=0
        #endtarget=`expr ${numvf} \- 1`

        if [ "${target2}" == "" ]; then
                endtarget=`expr ${numvf} \- 1`
        else
                endtarget=`expr \( ${numvf} \* 2 \) \- 1`
        fi
        doLogEcho "start target=${starttarget}, end target=${endtarget}"

        #redefine number of Queue for PF and VF
        if [ "${queuecnt}" != "" ]
        then
                makeQueue
        fi

        MAXLBA=$maxblock
        doLogEcho "Maximum LBA = ${MAXLBA}"
        if [ "${target2}" != "" ]; then
                limitsize=`expr ${maxblock} \/ \( ${numvf} \* 2 \+ 2 \)`
        else
                limitsize=`expr ${maxblock} \/ \( ${numvf} \+ 1 \)`
        fi
        doLogEcho "Limit Size = ${limitsize}"

        for seek in 0 1
        do
                for testtype in Write Read R50W50
                do
                        if [ $seek == 0 ]; then
                                xfer=128kb
                                seek_string=Sequential
                        else
                                xfer=4kb
                                seek_string=Random
                        fi

                        if [ "${target2}" == "" ]; then
                                endtarget2=`expr $endtarget \+ 1`
                        else
                                endtarget2=`expr $endtarget \+ 2`
                        fi

                        for (( looptarget=${starttarget}; looptarget<=${endtarget2}; looptarget++ ))
                        do
                                if [ ${looptarget} -le ${endtarget} ]; then
                                        looptarget2=${looptarget}
                                else
                                        if [ $looptarget == `expr $endtarget \+ 1` ]; then
                                                looptarget2=${target}
                                        else
                                                looptarget2=${target2}
                                        fi
                                fi

                                echo WriteEnabled=1 >/iport$port/target$looptarget2

                                position=`expr ${looptarget} \* ${limitsize}`
                                echo TestLimits=${limitsize},${position},0 >/iport$port/port

                                doLogEcho "Target$looptarget2 with NumVF=$numvf : Starting $testype test with Transfer Size = $xfer and Seek Type = $seek for $runtime"

                                testname[$looptarget]=$testtype\_$looptarget2\_$xfer\_$seek\_$numvf
                                echo ${testname[$looptarget]},$qd,$xfer,$runtime,$seek >/iport$port/target$looptarget2
                        done

                        statuscheck

                        perflog
                done
        done
done

echo TestLimits=0,0,0 >/iport$port/port

