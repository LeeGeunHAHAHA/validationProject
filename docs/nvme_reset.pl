#!/usr/bin/perl
#version 1.5
use strict;
use warnings;
#declare globals
my $testType = "Compare";
my $blocks = "1";
my $threads = "4";
my $access = "Random";
my $shutdownType =0;
my $resetType = 0;
my $port = -1; my $target = -1;
my $it = 0;
my $delayTime = 10;
my $dateString;
my $testName;
my $fh1; my $fh;
my $pci;
my $glitchLength = "50ms";
my $quarchPort; my $quarchSlot; my $quarchSerial;
main();
sub pollForTestStatus
{
        #first check if the test is still running
        my $testCheck = `cat /iport$port/tests/$testName| grep -c Running`;
        chomp($testCheck);
        if ($testCheck)
        {
                return 1;
        }
        else
        {
                $testCheck = `cat /iport$port/tests/$testName| grep -c Failed`;
                chomp($testCheck);
                if ($testCheck)
                {
                        return 0;
                }
        }
        return -1;
}
#sub to print to output
sub sb_print
{
        my $string = shift;
        print $string;
        print $fh1 $string;

}

sub usage
{
        print"Usage:\n";
        print"perl nvme_resets.pl [-p P] [-t T] [-n N] [-d D] [-r R] [-s S]\n";
        print"-p Port to test (Required)\n";
        print"-t Target/Controller to test (Required)\n";
        print"-n Number of iterations of reset test (Required)\n";
        print"-d Minimum time between resets\n";
        print"-r Reset type 0 = NVM Subsystem Reset | 1 = Controller Reset | 2 = PCI Functional Reset | 3 = PCI Conventional Reset | 4 = PERST# Glitch\n";
        print"-s Shutdown on Controller Reset 0 = Disable | 1 = Enable\n";
        exit;
}
sub getArgs
{
        my $portflag = 0;
        my $numflag=0;
        my $delayflag = 0;
        my $resetflag=0;
        my $shutdownflag=0;
        my $i=0;
        #print ("Scalar ARGV: " . scalar(@ARGV));
        while ($i < scalar @ARGV)
        {
                if ($ARGV[$i] eq "-hh")
                {
                        usage();
                }


                #check number of iterations
                elsif ($ARGV[$i] eq "-n")
                {
                        $numflag = 1;
                        if ($i == (scalar @ARGV -1))
                        {
                                bad("-n");
                        }
                        $i++;
                        my $passedNum = $ARGV[$i];
                        if ($passedNum > 0)
                        {
                                $it = $passedNum;
                        }
                        else
                        {
                                bad("-n");
                        }
                        $i++;
                }
                #check delay time
                elsif ($ARGV[$i] eq "-d")
                {
                        $delayflag = 1;
                        if ($i == (scalar @ARGV -1))
                        {
                                bad("-d");
                        }
                        $i++;
                        my $passedOff = $ARGV[$i];
                        if ($passedOff > 0)
                        {
                                $delayTime = $passedOff;
                        }
                        else
                        {
                                bad("-d");
                        }
                        $i++;
                }
                #check cycle type
                elsif ($ARGV[$i] eq "-r")
                {
                        $resetflag=1;
                        if ($i == (scalar @ARGV -1))
                        {
                                bad("-r");
                        }
                        $i++;
                        my $passedCycle = $ARGV[$i];
                        if ($passedCycle >= 0 || $passedCycle < 5)
                        {
                                $resetType = $passedCycle;
                        }
                        else
                        {
                                bad("-r");
                        }
                        $i++;
                }
                #check shutdown type
                elsif ($ARGV[$i] eq "-s")
                {
                        $shutdownflag=1;
                        if ($i == (scalar @ARGV -1))
                        {
                                bad("-s");
                        }
                        $i++;
                        my $passedShut = $ARGV[$i];
                        if ($passedShut >= 0 || $passedShut < 2)
                        {
                                $shutdownType = $passedShut;
                        }
                        else
                        {
                                bad("-s");
                        }
                        $i++;
                }
                #check port
                elsif ($ARGV[$i] eq "-p")
                {
                        $portflag =1;
                        if ($i == (scalar @ARGV -1))
                        {
                                bad("-p");
                        }
                        $i++;
                        my $passedPort = $ARGV[$i];
                        #check that the port is online, there are some targets, and the port is an init
                        my $check = `grep -w PortState /port$passedPort/port`;
                        chomp $check;
                        my $check2 = `grep -w Mode /port$passedPort/port`;
                        chomp $check2;

                        if (index($check, "Online") != -1 && index($check2, "Init") != -1)
                        {
                                my $check3 = `grep -i NumberOfTargets /iport$passedPort/port`;
                                #check number of targets
                                my $numTargs = substr($check3, index($check3, "=") + 1, length($check3)-index($check3, "=")-1);
                                if ($numTargs <= 0)
                                {
                                        print"No targets found on specified port\n";
                                        usage();
                                }
                                else
                                {
                                        $port = $passedPort;
                                        #get my target and LUN
                                        $i++;
                                        if ($ARGV[$i] ne "-t")
                                        {
                                                bad("-t");
                                        }
                                        $i++;
                                        #make sure the target number is valid
                                        my $checkTarg = $ARGV[$i];
                                        my $isValid=  `ls /iport$port | grep -c target$checkTarg`;
                                        if ($isValid > 0)
                                        {
                                                $target = $checkTarg;
                                        }
                                        else
                                        {
                                                print"Target $checkTarg not found on port $port\n";
                                                usage();
                                        }

                                }
                        }
                        else
                        {
                                print"Bad port\n";
                                usage();
                        }
                        $i++;

                }
                else
                {
                        bad("Unrecognized option: $ARGV[$i]");
                }
        }
        if (!$portflag)
        {
                bad("-p not specified");
        }
        if (!$numflag)
        {
                bad("-n not specified");
        }
        if (!$delayflag)
        {
                print"-d omitted. Running default time betweewn resets: $delayTime\n";
        }
        if (!$resetflag)
        {
                print"-r omitted. Running default cycle type: $resetType\n";
        }
        if (!$shutdownflag)
        {
                print"-s omitted. Running default shutdown type: $shutdownType\n";
        }
}
sub bad
{
        my $reason = shift;
        print"Bad Argument: $reason\n";
        usage();
}
sub startTest
{
        $dateString = localtime();
        #clear error counters
        sb_print"$dateString: Clearing error counters and test history\n";
        system("sbecho WriteEnabled=1>/iport$port/target$target");
        system("sbecho ClearErrors>/iport$port/target$target");
        system("sbecho ClearTests>/iport$port/target$target");
        system("sbecho ClearStats>/iport$port/target$target");
        my $acc  = 0;
        if ($access eq "Sequential")
        {
                $acc = 0;
        }
        elsif ($access eq "Random")
        {
                $acc = 1;
        }
        $dateString = localtime();
        sb_print"$dateString: Starting test with TestType = $testType, BlockSize = $blocks, ThreadCount = $threads, AccessPattern = $access on Port $port Target $target\n";
        system("sbecho $testName,$threads,$blocks,0,$acc,0,0,0,0,0,0 >/iport$port/target$target");

        return;
}






sub stopTest
{
        my $dateString = localtime();# localtime을 string로 바꿈
        sb_print"$dateString: Stopping test\n"; # sb print로 그걸 프린트 합니다.
        system("sbecho StopTests>/iport$port/target$target"); # target 에 StopTest
}
sub getResults
{
        $dateString = localtime();
        sb_print("$dateString: Test Results:\n");
        my $toPrint =`cat /iport$port/tests/$testName`;
        sb_print($toPrint);
        $dateString = localtime();
        sb_print("$dateString: Error Counters\n");
        $toPrint = `cat /iport$port/target$target | grep Errors`;
        sb_print($toPrint);
        $toPrint =`cat /iport$port/target$target | grep -i count`;
        sb_print($toPrint);
}
sub getTimings
{
        #my $pci = getStr(`grep TargetName /iport$port/target$target`);
        #variables for each time
        my $linkUp;
        my $enable;
        my $access;
        my @temp;
        #get the actual time and print it
        if ($resetType == 0 || $resetType == 3)
        {
                @temp=`grep "$pci: Controller Link Up to Controller Enable" /virtualun/log/trace | sort -r`;
                $linkUp = $temp[0];
                $linkUp = substr($linkUp, index($linkUp, "took") + 5, index($linkUp, "\n") - index($linkUp, "took"));
                chomp($linkUp);
        }
        @temp=`grep "$pci: Controller Enable (CC.EN=1) to Controller Ready (CSTS.RDY=1)" /virtualun/log/trace | sort -r`;
        $enable = $temp[0];
        $enable = substr($enable, index($enable, "took") + 5, index($enable, "\n") - index($enable, "took"));
        chomp($enable);
        @temp =`grep \"P$port:T$target:L1: Controller Ready to Media Access\" /virtualun/log/trace | sort -r`;
        $access = $temp[0];
        $access = substr($access, index($access, "took") + 5, index($access, "\n") - index($access, "took"));
        chomp($access);
        if (defined($linkUp))
        {
                print $fh "$linkUp,$enable,$access\n";
        }
        else
        {
                print $fh "N/A,$enable,$access\n";
        }
}

sub main
{
        getArgs();
        $testName= "$testType\_$port\_$target";
        #setup the log file
        my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
        my @abbr = qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
        $year += 1900;
        my $month = $abbr[$mon];
        open $fh1, ">nvme_resets_log\_$mday-$month-$year\_$hour\_$min\_$sec.txt";
        my $outString = "nvme_reset_timing_";

        if ($resetType == 0)
        {
                $outString = $outString . "nssr";
        }
        elsif ($resetType == 1)
        {
                $outString = $outString . "ctlr";
        }
        elsif ($resetType == 2)
        {
                $outString = $outString . "flr";
        }
        elsif ($resetType == 3)
        {
                $outString = $outString . "conv";
        }
        else
        {
                if (!checkQuarch())
                {
                        sb_print("Unable to find this device on a Quarch module!\n");
                        exit;
                }
        }
        if ($resetType != 4)
        {
                $outString = $outString . "_$mday-$month-$year\_$hour\_$min\_$sec.csv";
                open $fh, ">$outString";
        }
        #start the trace
        system("sbecho Trace=2>/proc/vlun/config");
        system("sbecho SizeTrace=1073741824>/proc/vlun/config");
        system("sbecho StartTracing>/proc/vlun/config");
        $dateString = localtime();

        #determine my PCI device
        $pci = getStr(`grep TargetName /iport$port/target$target`);
        #exit;
        startTest();
        #set and start tracing
        if ($resetType != 4)
        {
                print $fh "Iteration,Link Up Time,Enable Time,IO Ready Time\n";
        }
        for (my $i=0; $i < $it; $i++)
        {
                if ($resetType != 4)
                {
                        print $fh "$i,";
                }
                #clearTrace();
                sleep ($delayTime);
                my $status = pollForTestStatus();
                $dateString = localtime();
                if ($status == 0)
                {
                        sb_print("$dateString: Test status is Failed!\n");
                        getResults();
                        exit;
                }
                elsif ($status == -1)
                {
                        sb_print("$dateString: Test status is Passed. This is unexpected!\n");
                        getResults();
                        exit;
                }
                else
                {
                        sb_print("$dateString: Test is still running.\n");
                }
                #make sure the test is still running
                $dateString = localtime();
                doAction();
                sleep 10;
                if ($resetType != 4)
                {
                        getTimings();
                }
        }
        $dateString = localtime();
        stopTest();
        #get results
        getResults();

        exit;
}
sub doAction
{
        #do reset

        my $dateString = localtime();
        if ($resetType == 0)
        {
                sb_print("$dateString: Injecting NVMe Subsystem Reset on Controller $target\n");
                system("echo reset_nvm=$target > /proc/vlun/nvme");
        }
        elsif ($resetType == 1)
        {
                sb_print("$dateString: Injecting ControllerReset on Controller $target\n");
                if ($shutdownType == 0)
                {
                        system("echo reset_ctrl=$target > /proc/vlun/nvme");
                }
                else
                {
                        system("echo power_off=$pci>/proc/vlun/nvme");
                        sleep 1;
                        system("echo power_on=$pci>/proc/vlun/nvme");
                        sleep 5;
                }
        }
        elsif($resetType == 2)
        {
                sb_print("$dateString: Injecting PCI Functional Reset on Controller $target\n");
                system("echo reset_pci_func=$target > /proc/vlun/nvme");
        }
        elsif($resetType == 3)
        {
                sb_print("$dateString: Injecting PCI Conventional Reset on Controller $target\n");
                system("echo reset_pci_conv=$target > /proc/vlun/nvme");
        }
        else
        {
                sb_print("$dateString: Glitching PERST# on Controller $target for $glitchLength\n");
                quarchGlitch();
        }
}
sub clearTrace
{

        $dateString =localtime();
        sb_print("$dateString: Clearing trace\n");
        system("sbecho ClearTrace>/proc/vlun/config");
}
sub getStr
{
        my $str = shift;
        my $start = index ($str, "=");
        my $end = length($str);
        $str = substr ($str, $start+1, $end-$start-1);
        chomp($str);
        return $str;
}
#find the Quarch
sub checkQuarch
{
        #check that the selected target is mapped to a quarch port
        my $pci = getStr(`grep TargetName /iport$port/target$target`);
        my $quarchLoc = `grep -r $pci /virtualun/webs/web/rest/quarchs/*`;

        if (!$quarchLoc)
        {
                print("No mapped Quarch devices!\n");
                return 0;
        }
        else
        {
                if ($quarchLoc =~ m/\/virtualun\/webs\/web\/rest\/quarchs\/(\d+)\/slots\/(\d+)\/\S*/)
                {
                        $quarchPort = $1;
                        $quarchSlot = $2;
                }
                if ($quarchPort == -1 || $quarchSlot == -1)
                {
                        return 0;
                }
                else
                {
                        #get the serial how we do this depends on the module
                        my $serialCheck;
                        if ($quarchSlot != 0)
                        {
                                $serialCheck = 0;
                        }
                        else
                        {
                                $serialCheck = $quarchSlot;
                        }
                        my $quarchSer = `cat /virtualun/webs/web/rest/quarchs/$quarchPort/slots/$serialCheck/vlun/quarch_location`;
                        my $startSN = index($quarchSer, "SN");
                        my $endSN = index($quarchSer, ")");
                        if ($endSN == -1 && $startSN == -1)
                        {
                                print("Unable to find Quarch SN!\n");
                                return 0;
                        }
                        $quarchSerial = substr($quarchSer, $startSN +3, $endSN - $startSN -3);
                        $dateString= localtime;
                        sb_print("$dateString: Quarch Port = $quarchPort. Quarch Slot = $quarchSlot. Quarch Serial Number: $quarchSerial\n");
                        #sb_print $quarchSerial;
                        return 1;
                }
        }

}
#do the glitch
sub quarchGlitch
{
        #setup the glitch
        system("(quarch_usb \"glitch:mult $glitchLength <0>\" -s $quarchSerial) >/dev/null");
        #enable the perst signal for glitching
        system("(quarch_usb \"signal:HOST1_PERST0:glitch:enable on <0>\" -s $quarchSerial) >/dev/null");
        system("(quarch_usb \"signal:HOST2_PERST0:glitch:enable on <0>\" -s $quarchSerial) >/dev/null");
        #do the glitch
        system("(quarch_usb \"run:glitch once <0>\" -s $quarchSerial) >/dev/null");

}

