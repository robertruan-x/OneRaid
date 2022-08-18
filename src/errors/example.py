# CN
ONERAID_SHOW_DEFAULT_CN = 'one_raid -s  自动识别当前机器的raid卡,展示每张raid卡的信息'
ONERAID_SHOW_SELECT_CN = 'one_raid -a 0 -s  指定展示控制器0的raid卡的信息'

ONERAID_CREATE_RAID0_CN = 'one_raid -a 0 -c raid0 "32:12" "AWB"    将控制器0的 32:12 这块磁盘制作成raid0，并且raid参数设置为AWB'
ONERAID_CREATE_RAID1_CN = 'one_raid -a 0 -c raid1 "32:11,32:12" "AWB"    将控制器0的 32:11,32:12 这两块磁盘制作成raid1，并且raid参数设置为AWB'
ONERAID_CREATE_RAID10_CN = 'one_raid -a 0 -c raid10 "32:11,32:12" "AWB"    将控制器0的 32:11,32:12 这两块磁盘制作成raid10，并且raid参数设置为AWB'

ONERAID_DELETE_SELECT_CN = ''
ONERAID_DELETE_ALL_CN = ''

PERCCLI64_CREATE_RAID0_CN = '/tmp/raid/perccli64 /c0 add vd r0 size=all drives=32:13 WB RA Cache  PERCCLI64将控制器0的 32:12 这块磁盘制作成raid0，并且raid参数设置为WB RA Cache'
PERCCLI64_DELETE_VD_CN = '/tmp/raid/perccli64 /c0/v0 delete 删除raid组0'
PERCCLI64_SHOW_PRECACHE_CN = '/tmp/raid/perccli64 /c0 show preservedcache   显示当前已经掉盘，但是保留缓存的磁盘'
PERCCLI64_SHOW_FOREIGN_CN = '/tmp/raid/perccli64 /c0/fall show  显示当前foreign状态的磁盘'
PERCCLI64_GET_VDLIST_CN = '/tmp/raid/perccli64 /c0/vall show    显示制作了raid组的磁盘'
PERCCLI64_CREATE_RAID_RECOMMEND_CN = 'perccli64 创建raid前需要先检查当前的磁盘是否存在foreign,以及是否有磁盘存在保留缓存(preservedcache)'
PERCCLI64_DELETE_VD_RECOMMEND_CN = 'perccli64 创建raid前需要先检查当前的磁盘是否存在foreign,以及是否有磁盘存在保留缓存(preservedcache)'


ONERAID_PARSER_ERROR_CN = """\
    命令参数输入错误, {detail_error}
    
    例子：
        {example}
    """

ONERAID_COMMAND_ERROR_CN = """\
    命令运行错误, {detail_error}

    建议：{recommend}

    或则你可以使用原生raid命令: 
        {raw_command}
    """

ONERAID_DOWNLOAD_ERROR_CN = """\
    下载错误, {detail_error}

    建议：你需要检查下当前的网络环境，和dns解析

    或则你尝试手动执行下载命令: 
        {raw_command}
    """
