#!/bin/bash
if [ $# -lt 1  ]; then
    echo "usage:vmstart.sh <vm>"
    echo "available machines:cs,cs2,cs3,us,us2,us3,xs"
    exit 1
fi
declare -A  dic
dic=(['cs']="e:/virtual_machines/CentOS-Server/CentOS-Server.vmx"  \
     ['xs']="e:/virtual_machines/XUbuntu-Server/XUbuntu-Server.vmx"  \
    )
key=$1
vmx_path=${dic[$key]}
if [ x"$vmx_path" == x"" ];then
    vmx_path=$1
fi
#vmrun.exe start $vmx_path  nogui
cmd="vmrun.exe start $vmx_path  nogui"
echo $cmd
eval $cmd
