
from .example import *

class OneRaidError(Exception):
    def __init__(self, *args: object,message="") -> None:
        self._message = message
    
    
    @property
    def message(self):
        return self._message
    
    
    def message(self,val):
        self._message = val   
    
    
    def __str__(self) -> str:
        return self.message


class OneRaidParserError(OneRaidError):
    """执行oneraid命令解析错误"""
    pass

class OneRaidParserShowError(OneRaidParserError):

    def message(self):
        return ONERAID_PARSER_ERROR_CN.format(
            detail_errror=self._message,
            example='\n'.join(ONERAID_SHOW_DEFAULT_CN,ONERAID_SHOW_SELECT_CN))
    

class OneRaidParserCreateRaidError(OneRaidParserError):
    def message(self):
        return ONERAID_PARSER_ERROR_CN.format(
            detail_errror=self._message,
            example='\n'.join(ONERAID_CREATE_RAID0_CN,ONERAID_CREATE_RAID1_CN))
    

class OneRaidParserDeleteRaidError(OneRaidParserError):
    def message(self):
        return ONERAID_PARSER_ERROR_CN.format(
            detail_errror=self._message,
            example='\n'.join(ONERAID_DELETE_SELECT_CN,ONERAID_DELETE_ALL_CN))
 










class OneRaidCommandError(OneRaidError):
    """命令运行时错误"""
    pass


class OneRaidDownloadError(OneRaidError):
    """下载命令时错误"""
    pass
    