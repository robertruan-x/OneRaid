#!/usr/bin/python3
############################################
# FileName: one_raid.py
# FileEnconding: UTF-8
# Date: 2022-08-11
#############################################

import argparse
import os
from pydoc import classname
import re
import subprocess
from typing import Tuple
import json
from prettytable import PrettyTable

from errors import *

__version__ = "0.0.19"

DEBUG = 1

# raid软件存放位置
PATH_SAS3IRU = "/tmp/raid/sas3ircu"
PATH_SAS2IRU = "/tmp/raid/sas2ircu"
PATH_PERCCLI64 = "/tmp/raid/perccli64"
PATH_STORCLI64 = "/tmp/raid/storcli64"
PATH_ARCCONF = "/tmp/raid/arcconf"

# raid软件下载链接
DOWNLOAD_URL_SAS3IRU = "https://oneraid.oss-cn-hangzhou.aliyuncs.com/linux_x64/sas3ircu"
DOWNLOAD_URL_SAS2IRU = "https://oneraid.oss-cn-hangzhou.aliyuncs.com/linux_x86/sas2ircu"
DOWNLOAD_URL_PERCCLI64 = "https://oneraid.oss-cn-hangzhou.aliyuncs.com/linux_x64/perccli64"
DOWNLOAD_URL_STORCLI64 = "https://oneraid.oss-cn-hangzhou.aliyuncs.com/linux_x64/storcli64"
DOWNLOAD_URL_ARCCONF = "https://oneraid.oss-cn-hangzhou.aliyuncs.com/linux_x64/arcconf"

# 包含raid对象的数组
RAID_ALL = []


#  运行系统命令
def run_cmd(cmd: str) -> Tuple[str, str]:
    # p = os.popen(cmd)
    # output = p.read()
    # p.close()
    if DEBUG == 1:
        print("run command: ", cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.stdout.read().decode('utf-8')
    errcode = p.poll()

    return output, errcode


class Raid():
    def __init__(self) -> None:
        self.cli = ""  # 使用的命令路径
        self.pdlist = []  # class Pdinfo的列表
        self.vdlist = []  # class Vdinfo的列表
        self.adapterid = ""
        self.apinfo = self.Apaterinfo()

    def getPdlist(self) -> list:
        pass

    def getVdlist(self) -> list:
        pass
    # def getControllers() -> list:
    #     pass

    #  物理磁盘信息的结构
    class Pdinfo():
        def __init__(self) -> None:
            self.controler_id = ""
            self.device_id = ""
            self.state = ""
            self.size = ""
            self.sn = ""
            self.manufacturer = ""
            self.model = ""
            self.protocal = ""
            self.type = ""
            self.diskname = ""  # 存放块设备名
            self.remark = ""  # 扩展使用

        def __str__(self) -> str:
            return str(self.__dict__)

    # raid组信息的结构
    class Vdinfo():
        def __init__(self) -> None:
            self.device_group = ""
            self.vd_id = ""
            self.state = ""
            self.access_mode = ""
            self.consistent = ""
            self.raid_detail = ""
            self.scheduled = ""
            self.size = ""

        def __str__(self) -> str:
            return str(self.__dict__)

    # raid卡自己的信息
    class Apaterinfo():
        def __init__(self) -> None:
            self.apater_name = ""
            self.sn = ""
            self.bios_version = ""
            self.fireware_version = ""
            self.bus_id = ""
            self.device_id = ""
            self.function_id = ""

        def __str__(self) -> str:
            return str(self.__dict__)

    def pretty_display(self):
        if self.apinfo:
            a = PrettyTable([u"raid名字", u"sn", u"bios版本", u"fireware版本", u"bus id", u"device id", u"function id",
                             u"使用软件"])
            a.add_row(
                [
                    self.apinfo.apater_name,
                    self.apinfo.sn,
                    self.apinfo.bios_version,
                    self.apinfo.fireware_version,
                    self.apinfo.bus_id,
                    self.apinfo.device_id,
                    self.apinfo.function_id,
                    self.__class__.__name__
                ]
            )
            print(a.get_string(title="raid卡信息"))

        x = PrettyTable([u"控制id", u"设备id", u"sn", u"状态", u"容量", u"厂商", u"型号", u"协议", u"类型", u"备注"])
        for pd in self.pdlist:
            x.add_row([
                pd.controler_id,
                pd.device_id,
                pd.sn,
                pd.state,
                pd.size,
                pd.manufacturer,
                pd.model,
                pd.protocal,
                pd.type,
                pd.remark
            ])
        print(x.get_string(title="物理磁盘列表"))

        if self.vdlist:
            v = PrettyTable(
                [u"设备组", u"Raid组id", u"sn", u"状态", u"读写模式", u"一致性", u"Raid组参数", u"容量"])
            for vd in self.vdlist:
                v.add_row([
                    vd.device_id,
                    vd.vd_id,
                    vd.state,
                    vd.access_mode,
                    vd.consistent,
                    vd.raid_detail,
                    vd.scheduled,
                    vd.size
                ])
            print(x.get_string(title="虚拟磁盘列表"))



    def log_success(self, s: str):
        print(s)

    def log_debug(self, s: str):
        print(s)


"""
    sas3iru命令
    适用：Serial Attached SCSI controller: LSI SAS3008 PCI-Express Fusion-MPT SAS-3
"""


class Sas3iru(Raid):
    def __init__(self, cli, adapterid) -> None:
        super().__init__()
        self.cli = cli
        self.adapterid = adapterid
        self.pdlist = []

    def getApinfo(self):

        cmd = "{} {} display".format(self.cli, self.adapterid)
        # 解析原命令信息
        output, errorcode = run_cmd(cmd)
        self.format_apinfo(output)

    def format_apinfo(self, output: str):
        appattern = re.compile(r"Controller type.*\n(.*\n){12}")
        apinfostr = appattern.search(output).group()
        apinfo = Raid.Apaterinfo()
        apinfo.apater_name = self.sas_re_search("Controller type", apinfostr)
        apinfo.sn = ""
        apinfo.bios_version = self.sas_re_search("BIOS version", apinfostr)
        apinfo.fireware_version = self.sas_re_search("Firmware version", apinfostr)
        apinfo.bus_id = self.sas_re_search("Bus", apinfostr)
        apinfo.device_id = self.sas_re_search("Device", apinfostr)
        apinfo.function_id = self.sas_re_search("Function", apinfostr)
        self.apinfo = apinfo

    def getPdlist(self) -> list:
        cmd = "{} {} display".format(self.cli, self.adapterid)
        # 解析原命令信息
        output, errorcode = run_cmd(cmd)
        self.format_sas3iru(output)
        return []

    # 格式化命令输出信息，然后填充到pdlist
    def format_sas3iru(self, output: str):
        pdpattern = re.compile(r"Device is a Hard disk\n(.*\n){13}")
        matches = pdpattern.finditer(output)
        for match in matches:
            pdinfostr = match.group()
            pdinfo = Raid.Pdinfo()
            pdinfo.controler_id = self.sas_re_search("Enclosure", pdinfostr)
            pdinfo.device_id = self.sas_re_search("Slot", pdinfostr)
            pdinfo.state = self.sas_re_search("State", pdinfostr)
            pdinfo.size = self.sas_re_search("Size", pdinfostr)
            pdinfo.sn = self.sas_re_search("Unit Serial No", pdinfostr)
            pdinfo.manufacturer = self.sas_re_search("Manufacturer", pdinfostr)
            pdinfo.model = self.sas_re_search("Model Number", pdinfostr)
            pdinfo.protocal = self.sas_re_search("Protocol", pdinfostr)
            pdinfo.type = self.sas_re_search("Drive Type", pdinfostr)
            self.pdlist.append(pdinfo)


    # sas3和sas2正则查询属性
    def sas_re_search(self, part: str, sources: str) -> str:
        res = re.search(part + ".*: (.*)\n", sources)
        if res:
            return res.group(1)
        else:
            return ""

    def onLED_core(self, controler_id, device_id):
        cmd = "{} {} locate {}:{} on".format(self.cli, self.adapterid, controler_id, device_id)
        output, code = run_cmd(cmd)
        if code == 0:
            super().log_success("成功点亮磁盘{}:{}".format(controler_id, device_id))

    def offLED_core(self, controler_id, device_id):
        cmd = "{} {} locate {}:{} off".format(self.cli, self.adapterid, controler_id, device_id)
        run_cmd(cmd)

    #  点亮功能通过sn
    def onLED_by_sn(self, sn):
        for pd in self.pdlist:
            if pd.sn == sn:
                self.onLED_core(pd.controler_id, pd.device_id)

    # 自动点亮未挂载磁盘
    def onLED_by_auto(self):
        # 查找没有挂载的磁盘
        cmd = "lsblk | egrep -v '/|NAME' | grep -v ` lsblk | grep boot | awk 'NR==1{print $1}' | cut -c3-5 ` | awk '{print $1}'"
        output, returncode = run_cmd(cmd)
        unusedisk = []
        if returncode == 0:
            unusedisk = output.splitlines()

        # 如果没有未挂载的提示
        if len(unusedisk) == 0:
            print("没有未挂载磁盘")
            return

        cmd = "/usr/local/bin/disk_info --all"
        output, returncode = run_cmd(cmd)
        if returncode == 0:
            diskinfo = json.loads(output)
            for disk in unusedisk:
                sn = diskinfo.get("disk_info").get(str(disk)).get("disk_list")[0].get("serial_number")
                self.onLED_by_sn(sn)
        else:
            pass

    # 关闭所有LED灯
    def offLED_ALL(self):
        for pd in self.pdlist:
            self.offLED_core(pd.controler_id, pd.device_id)


# 直接继承Sas3iru
class Sas2iru(Sas3iru):

    def format_sas3iru(self, output: str):
        pdpattern = re.compile(r"Device is a Hard disk\n(.*\n){12}")
        matches = pdpattern.finditer(output)
        for match in matches:
            pdinfostr = match.group()
            pdinfo = Raid.Pdinfo()
            pdinfo.controler_id = super().sas_re_search("Enclosure", pdinfostr)
            pdinfo.device_id = super().sas_re_search("Slot", pdinfostr)
            pdinfo.state = super().sas_re_search("State", pdinfostr)
            pdinfo.size = super().sas_re_search("Size", pdinfostr)
            pdinfo.sn = super().sas_re_search("Serial No", pdinfostr)
            pdinfo.manufacturer = self.sas_re_search("Manufacturer", pdinfostr)
            pdinfo.model = super().sas_re_search("Model Number", pdinfostr)
            pdinfo.protocal = super().sas_re_search("Protocol", pdinfostr)
            pdinfo.type = super().sas_re_search("Drive Type", pdinfostr)
            self.pdlist.append(pdinfo)

    def onLED_by_sn(self, sn):
        for pd in self.pdlist:
            if (pd.sn == sn) or (pd.sn in sn) or (sn in pd.sn):
                self.onLED_core(pd.controler_id, pd.device_id)


class Storcli64(Raid):
    def __init__(self, cli, adapterid) -> None:
        super().__init__()
        self.cli = cli
        self.adapterid = adapterid
        self.pdlist = []

    def getApinfo(self):
        cmd = "{} /c{} show J".format(self.cli, self.adapterid)
        # 解析原命令信息
        output, errorcode = run_cmd(cmd)
        if errorcode == 0:
            self.format_apinfo(output)

    def format_apinfo(self, output: str):
        j = json.loads(output)
        resdata = j.get("Controllers")[0].get("Response Data")
        apinfo = Raid.Apaterinfo()
        apinfo.apater_name = resdata.get("Product Name")
        apinfo.sn = resdata.get("Serial Number")
        apinfo.bios_version = resdata.get("BIOS Version")
        apinfo.fireware_version = resdata.get("FW Version")
        apinfo.bus_id = resdata.get("Bus Number")
        apinfo.device_id = resdata.get("Device Number")
        apinfo.function_id = resdata.get("Function Number")
        self.apinfo = apinfo

    def getPdlist(self) -> list:
        cmd = "{} /c{} show all J".format(self.cli, self.adapterid)
        # 解析原命令信息
        output, errorcode = run_cmd(cmd)
        self.format_pdinfo(output)
        return []

    # 格式化命令输出信息，然后填充到pdlist
    def format_pdinfo(self, output: str):
        j = json.loads(output)
        for pd in j.get("Controllers")[0].get("Response Data").get("PD LIST"):
            pdinfo = Raid.Pdinfo()
            pdinfo.controler_id = pd.get("EID:Slt").split(":")[0:1][0]
            pdinfo.device_id = pd.get("EID:Slt").split(":")[1:2][0]
            pdinfo.state = pd.get("State")
            pdinfo.size = pd.get("Size")

            pdinfo.model = pd.get("Model")
            pdinfo.protocal = pd.get("Intf")
            pdinfo.type = pd.get("Med")

            # 重新获取sn
            pdposition = ""
            if pdinfo.controler_id == ' ':
                pdposition = "/c{}/s{}".format(self.adapterid, pdinfo.device_id)
                cmd = "{} {} show all J".format(self.cli, pdposition)
            else:
                pdposition = "/c{}/e{}/s{}".format(self.adapterid, pdinfo.controler_id, pdinfo.device_id)
                cmd = "{} {} show all J".format(self.cli, pdposition)
            output1, returncode = run_cmd(cmd)
            if returncode == 0:  # 如果磁盘状态bad,有可能无法查询到sn信息
                # 有点曲折
                pdinfo.sn = json.loads(output1).get("Controllers")[0].get("Response Data").get(
                    "Drive {} - Detailed Information".format(pdposition)).get(
                    "Drive {} Device attributes".format(pdposition)).get("SN")
                pdinfo.manufacturer = json.loads(output1).get("Controllers")[0].get("Response Data").get(
                    "Drive {} - Detailed Information".format(pdposition)).get(
                    "Drive {} Device attributes".format(pdposition)).get("Manufacturer Id")
                pdinfo.remark = pdposition  # 该扩展记录/cx/ex/sx的信息
            self.pdlist.append(pdinfo)


    def getVdlist(self) -> list:
        cmd = "{} /c{}/vall show all J".format(self.cli, self.adapterid)
        # 解析原命令信息
        output, returncode = run_cmd(cmd)
        if returncode != 0:
            raise OneRaidCommandGetVdlistError("获取raid组信息失败", self.__class__.__name__)
            self.format_vdinfo(output)
        return []

    def format_vdinfo(self,output:str):
        j = json.loads(output)
        for vd in j.get("Controllers")[0].get("Response Data").get("Virtual Drives"):
            vdinfo = Raid.Vdinfo()
            vdinfo.device_group = vd.get("DG/VD").split("/")[0:1][0]
            vdinfo.vd_id = vd.get("DG/VD").split("/")[1:2][0]
            vdinfo.state = vd.get("State")
            vdinfo.size = vd.get("Size")

            vdinfo.access_mode = vd.get("Access")
            vdinfo.consistent = vd.get("Consist")
            vdinfo.raid_detail = vd.get("Cache")
            vdinfo.scheduled = vd.get("sCC")

    def create_raidX_core(self, raidlevel: int, devices: str, options: str):

        if options == "":
            options = "AWB RA Cached"

        # devices 格式为 "32:2,32:4"
        cmd = "{} /c{} add vd r{} size=all drives={} {}".format(self.cli, self.adapterid, raidlevel, devices, options)
        output, returncode = run_cmd(cmd)
        if returncode == 0:
            print("设备[{}] 添加raid{} 成功".format(devices, raidlevel))
        else:
            raise OneRaidCommandGetVdlistError("创建raid组失败", self.__class__.__name__)

    def delete_raidX_core(self):
        pass

    def onLED_core(self, pdposition):
        cmd = "{} {} start locate".format(self.cli, pdposition)
        output, code = run_cmd(cmd)
        if code == 0:
            super().log_success("成功点亮磁盘{}".format(pdposition))

    def offLED_core(self, pdposition):
        cmd = "{} {} stop locate".format(self.cli, pdposition)
        run_cmd(cmd)

    #  点亮功能通过sn
    def onLED_by_sn(self, sn):
        for pd in self.pdlist:
            if pd.sn == sn:
                self.onLED_core(pd.remark)

    # 自动点亮未挂载磁盘
    def onLED_by_auto(self):
        # 查找没有挂载的磁盘
        cmd = "lsblk | grep sd | egrep -v '/|NAME|├─|└─' | grep -v ` lsblk | grep boot | awk 'NR==1{print $1}' | cut -c3-5 ` | awk '{print $1}'"
        output, returncode = run_cmd(cmd)
        unusedisk = []
        if returncode == 0:
            unusedisk = output.splitlines()

        # 如果没有未挂载的提示
        if len(unusedisk) == 0:
            print("没有未挂载磁盘")
            return

        cmd = "/usr/local/bin/disk_info --all"
        output, returncode = run_cmd(cmd)
        if returncode == 0:
            diskinfo = json.loads(output)
            for disk in unusedisk:
                sn = diskinfo.get("disk_info").get(str(disk)).get("disk_list")[0].get("serial_number")
                self.onLED_by_sn(sn)
        else:
            pass

    # 关闭所有LED灯
    def offLED_ALL(self):
        for pd in self.pdlist:
            self.offLED_core(pd.remark)


# 直接继承Storcli64
class Perccli64(Storcli64):
    pass


class Arcconf(Raid):
    def __init__(self, cli, adapterid) -> None:
        super().__init__()
        self.cli = cli
        self.adapterid = adapterid
        self.pdlist = []

    # arcc正则查询属性
    def arcc_re_search(self, part: str, sources: str) -> str:
        res = re.search(part + ".*: (.*)\n", sources)
        if res:
            return res.group(1)
        else:
            return ""

    def getApinfo(self):
        cmd = "{} GETCONFIG {} AD".format(self.cli, self.adapterid)
        # 解析原命令信息
        output, errorcode = run_cmd(cmd)
        if errorcode == 0:
            self.format_apinfo(output)

    def format_apinfo(self, output: str):

        apinfostr = output
        apinfo = Raid.Apaterinfo()
        apinfo.apater_name = self.arcc_re_search("Controller Model", apinfostr)
        apinfo.sn = self.arcc_re_search("Controller Serial Number", apinfostr)
        apinfo.bios_version = self.arcc_re_search("Driver", apinfostr)
        apinfo.fireware_version = self.arcc_re_search("Firmware", apinfostr)
        apinfo.bus_id = self.arcc_re_search("PCI Address", apinfostr).split(":")[1:2][0]
        apinfo.device_id = self.arcc_re_search("PCI Address", apinfostr).split(":")[2:3][0]
        apinfo.function_id = self.arcc_re_search("PCI Address", apinfostr).split(":")[3:4][0]
        self.apinfo = apinfo

    def getPdlist(self) -> list:
        cmd = "{} GETCONFIG {} PD".format(self.cli, self.adapterid)
        # 解析原命令信息
        output, errorcode = run_cmd(cmd)
        self.format_pdinfo(output)
        return []

    # 格式化命令输出信息，然后填充到pdlist
    def format_pdinfo(self, output: str):
        pdpattern = re.compile(r"Device #(.*?)Device Phy Information", re.S)
        matches = pdpattern.finditer(output)
        for match in matches:
            pdinfostr = match.group()
            pdinfo = Raid.Pdinfo()
            pdinfo.controler_id = self.arcc_re_search("Reported Channel", pdinfostr).split(",")[0:1][0]
            pdinfo.device_id = self.arcc_re_search("Reported Channel", pdinfostr).split(",")[1:2][0].split("(")[0:1][0]
            pdinfo.state = self.arcc_re_search("State", pdinfostr)
            pdinfo.size = self.arcc_re_search("Total Size", pdinfostr)
            pdinfo.sn = self.arcc_re_search("Serial number", pdinfostr)
            pdinfo.manufacturer = self.arcc_re_search("Vendor", pdinfostr)
            pdinfo.model = self.arcc_re_search("Model", pdinfostr)
            pdinfo.protocal = self.arcc_re_search("Transfer Speed", pdinfostr)
            pdinfo.type = self.arcc_re_search("Drive Configuration Type", pdinfostr)
            pdinfo.remark = self.arcc_re_search("Disk Name", pdinfostr)
            self.pdlist.append(pdinfo)


def download_soft():
    if os.path.exists("/tmp/raid") == False:
        os.mkdir("/tmp/raid", 0o744)

    def download_core(name, path, cmd):
        if os.path.exists(path) == False:
            output, returncode = run_cmd(cmd)
            if returncode == 0:
                print("[{}]软件安装成功,保存路径为:{}".format(name, path))

    # 需要下载的基础软件
    cmd = "lspci --version"
    # 解析原命令信息
    output, errorcode = run_cmd(cmd)
    if errorcode != 0:
        download_core(
            name='lspci',
            path="yum安装路径",
            cmd="yum install -y pciutils"
        )



    # 按需下载软件包
    for raid in RAID_ALL:
        if raid.__class__.__name__ == 'Perccli64':
            download_core(
                name='Perccli64',
                path=PATH_PERCCLI64,
                cmd="cd /tmp/raid && curl -skO {} && chmod 744 {}".format(DOWNLOAD_URL_PERCCLI64, PATH_PERCCLI64))

        elif raid.__class__.__name__ == 'Storcli64':
            download_core(
                name='Storcli64',
                path=PATH_STORCLI64,
                cmd="cd /tmp/raid && curl -skO {} && chmod 744 {}".format(DOWNLOAD_URL_STORCLI64, PATH_STORCLI64))

        elif raid.__class__.__name__ == 'Sas2iru':
            download_core(
                name='Sas2iru',
                path=PATH_SAS2IRU,
                cmd="cd /tmp/raid && curl -skO {} && chmod 744 {}".format(DOWNLOAD_URL_SAS2IRU, PATH_SAS2IRU))

        elif raid.__class__.__name__ == 'Sas3iru':
            download_core(
                name='Sas3iru',
                path=PATH_SAS3IRU,
                cmd="cd /tmp/raid && curl -skO {} && chmod 744 {}".format(DOWNLOAD_URL_SAS3IRU, PATH_SAS3IRU))

        elif raid.__class__.__name__ == 'Arcconf':
            download_core(
                name='Arcconf',
                path=PATH_ARCCONF,
                cmd="cd /tmp/raid && curl -skO {} && chmod 744 {}".format(DOWNLOAD_URL_ARCCONF, PATH_ARCCONF))


"""
sas3iru
Serial Attached SCSI controller: Broadcom / LSI SAS3008 PCI-Express Fusion-MPT SAS-3 (rev 02)
Serial Attached SCSI controller: LSI Logic / Symbios Logic SAS3008

storcli
RAID bus controller: Broadcom / LSI MegaRAID SAS-3 3008

arcconf
Serial Attached SCSI controller: Adaptec Series 8 12G SAS/PCIe 3
"""


def get_PCIE_raid():
    cmd = 'lspci | grep -i -E "scsi|raid"'
    output, returncode = run_cmd(cmd)
    if returncode == 0:
        sas3I = sas2I = perI = stroI = 0  # 各种控制器的index
        arffI = 1
        for line in output.splitlines():
            if ('Serial Attached SCSI controller: Broadcom / LSI SAS3' in line) or (
                    'Serial Attached SCSI controller: LSI Logic / Symbios Logic SAS3' in line):  # sas3iru
                sas3 = Sas3iru(PATH_SAS3IRU, sas3I)
                RAID_ALL.append(sas3)
                sas3I += 1
            elif 'Serial Attached SCSI controller: Broadcom / LSI SAS2' in line:  # sas2iru
                sas2 = Sas2iru(PATH_SAS2IRU, sas2I)
                RAID_ALL.append(sas2)
                sas2I += 1
            elif 'RAID bus controller: Broadcom / LSI MegaRAID' in line:
                cmd_isDELL = "dmidecode -s system-manufacturer"
                output1, returncode1 = run_cmd(cmd_isDELL)
                if output1.startswith('Dell'):
                    perOrStor = Perccli64(PATH_PERCCLI64, perI)  # perccli
                    perI += 1
                else:
                    perOrStor = Storcli64(PATH_STORCLI64, stroI)  # storcli
                    stroI += 1
                RAID_ALL.append(perOrStor)
            elif 'Serial Attached SCSI controller: Adaptec Series' in line:  # affconf
                arff = Arcconf(PATH_ARCCONF, arffI)
                RAID_ALL.append(arff)
                arffI += 1
            else:
                print("lspci找不到raid卡")
        download_soft()
    else:
        pass


def isNotNone(args):
    return args != None


if __name__ == '__main__':

    #  初始识别当前环境的
    get_PCIE_raid()
    print(RAID_ALL)
    parser = argparse.ArgumentParser(description='on_raid 用于各种raid操作，目前只支持sas3iru和sas2iru!!!!')

    parser.add_argument('-s',
                        dest="show",
                        action='store_true',
                        help='显示raid整列卡以及其信息')
    parser.add_argument('-a', '--adapter',
                        dest='adapter_id',
                        type=int,
                        help='指定控制器命令（adapter）的id')
    parser.add_argument('-c', '--create',
                        dest='create',
                        nargs='*',
                        metavar='raidlevel "eid:sid" (raidoptions)',
                        help='创建raid组')
    parser.add_argument('--raid',
                        dest='raid_soft',
                        choices=["sas3iru", "sas2iru", "precli", "strocli", "arcconf"],
                        help='指定控制软件,默认情况会自动识别当前的pcie识别,使用指定的控制软件')
    parser.add_argument('-l', '--locate',
                        dest='sns',
                        nargs='*',
                        help='通过sn点亮磁盘')
    parser.add_argument('-u', '--unlocate',
                        dest='unlocate',
                        action='store_true',
                        help='关闭所有磁盘LED')

    parser.add_argument('-m', '--mode',
                        dest='mode',
                        type=int,
                        help='自定义模式')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + __version__)

    args = parser.parse_args()

    adapter_id = 0

    # 自定义模式
    if isNotNone(args.mode):
        if args.mode == 1:  # 自动点亮未使用的磁盘
            for r in RAID_ALL:
                r.getPdlist()
                r.offLED_ALL()
                r.onLED_by_auto()

    if isNotNone(args.create):
        try:
            if not isNotNone(args.adapter_id):
                raise OneRaidParserCreateRaidError("创建raid需要指定控制命令（adapter）id")
            else:
                raidlevel, devices, options = args.create  # 如果options没填的话不行
                if args.create[0] == "raid0":
                    for r in RAID_ALL:
                        if r.adapterid == adapter_id:
                            r.create_raidX_core(0, devices, options)
                elif args.create[0] == "raid1":
                    for r in RAID_ALL:
                        if r.adapterid == adapter_id:
                            r.create_raidX_core(1, devices, options)
                elif args.create[0] == "raid10":
                    for r in RAID_ALL:
                        if r.adapterid == adapter_id:
                            r.create_raidX_core(1, devices, options)
                else:
                    pass
        finally:
            pass

    if isNotNone(args.show):
        if adapter_id:
            pass
        else:
            for r in RAID_ALL:
                r.getApinfo()
                r.getPdlist()
                r.getVdlist()
                r.pretty_display()

    if isNotNone(args.sns):
        if adapter_id:
            pass
        else:
            for r in RAID_ALL:
                r.getPdlist()

                # 先关闭所有磁盘LED
                r.offLED_ALL()
                # 点亮磁盘
                for sn in args.sns:
                    r.onLED_by_sn(sn)

    if args.unlocate:
        for r in RAID_ALL:
            r.getPdlist()
            # 先关闭所有磁盘LED
            r.offLED_ALL()
