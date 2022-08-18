from .example import *


# 通过raid类型，转换变量
def getVarOfRaid(name, raid: str):
    res = ""
    if raid != "":
        try:
            res = globals()[raid.upper() + name]
            # exec('res = {}'.format(raid.upper() + name))
        finally:
            pass
    return res


class OneRaidError(Exception):
    def __init__(self, message) -> None:
        self._message = message

    def message(self):
        return self._message

    def __str__(self) -> str:
        return self.message()


class OneRaidParserError(OneRaidError):
    """执行oneraid命令解析错误"""
    pass


class OneRaidParserShowError(OneRaidParserError):

    def message(self):
        return ONERAID_PARSER_ERROR_CN.format(
            detail_error=self._message,
            example='\n\t'.join([ONERAID_SHOW_DEFAULT_CN, ONERAID_SHOW_SELECT_CN]))


class OneRaidParserCreateRaidError(OneRaidParserError):
    def message(self):
        return ONERAID_PARSER_ERROR_CN.format(
            detail_error=self._message,
            example='\n\t'.join([ONERAID_CREATE_RAID0_CN, ONERAID_CREATE_RAID1_CN]))


class OneRaidParserDeleteRaidError(OneRaidParserError):
    def message(self):
        return ONERAID_PARSER_ERROR_CN.format(
            detail_error=self._message,
            example='\n\t'.join([ONERAID_DELETE_SELECT_CN, ONERAID_DELETE_ALL_CN]))


class OneRaidCommandError(OneRaidError):
    """命令运行时错误"""

    def __init__(self, message, raid) -> None:
        self._message = message
        self._raid = raid


class OneRaidCommandCreateRaidError(OneRaidCommandError):
    def message(self):
        _CREATE_RAID0_CN = getVarOfRaid("_CREATE_RAID0_CN", self._raid)
        _CREATE_RAID_RECOMMEND_CN = getVarOfRaid("_CREATE_RAID_RECOMMEND_CN", self._raid)
        _SHOW_FOREIGN_CN = getVarOfRaid("_SHOW_FOREIGN_CN", self._raid)
        _SHOW_PRECACHE_CN = getVarOfRaid("_SHOW_PRECACHE_CN", self._raid)

        return ONERAID_COMMAND_ERROR_CN.format(
            detail_error=self._message,
            recommend=_CREATE_RAID_RECOMMEND_CN,
            raw_command='\n\t'.join([_CREATE_RAID0_CN, _SHOW_FOREIGN_CN, _SHOW_PRECACHE_CN]))


class OneRaidCommandDeleteVdError(OneRaidCommandError):
    def message(self):
        _DELETE_VD_CN = getVarOfRaid(" _DELETE_VD_CN", self._raid)

        return ONERAID_COMMAND_ERROR_CN.format(
            detail_error=self._message,
            recommend="",
            raw_command='\n\t'.join([_DELETE_VD_CN]))


class OneRaidCommandGetVdlistError(OneRaidCommandError):
    def message(self):
        _GET_VDLIST_CN = getVarOfRaid("_GET_VDLIST_CN", self._raid)

        return ONERAID_COMMAND_ERROR_CN.format(
            detail_error=self._message,
            recommend="",
            raw_command='\n\t'.join([_GET_VDLIST_CN]))


class OneRaidDownloadError(OneRaidError):
    """下载命令时错误"""
    pass
