"""
改变从网站上上传的 图片 和 附件 的默认存储位置
"""

from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


# 默认的系统存储 FileStronge
class FDFSStorage(Storage):
    '''fast dfs文件存储类'''
    def __init__(self):
        '''初始化'''
        self.client_conf = settings.FDFS_CLIENT_CONF
        self.base_url = settings.FDFS_URL

    # 打开文件时使用
    def _open(self, name, mode='rb'):
        pass

    # 保存文件时使用
    def _save(self, name, content):
        """
        :param name: 你选择上传文件的名字
        :param content: 包含你上传文件内容的File对象
        :return:
        """
        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_conf)

        # 上传文件到fast dfs系统中
        res = client.upload_by_buffer(content.read())

        # print('res----------------------------->>>>>>>', res)
        # 返回的数据格式
        # {
        #     'Uploaded size': '9.69KB',
        #     'Storage IP': b'192.168.12.189',
        #     'Group name': b'group1',
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Remote file_id': b'group1/M00/00/00/wKgMvVvHKzeAFiJkAAAmv27pX4k7691647'
        # }

        # 可能会返回二进制（bytes）
        if res.get('Status') != 'Upload successed.':
            #上传失败
            raise Exception('上传文件到FastDFS失败')

        # 获取返回的文件ID(一定要记得修改文件格式为‘utf8’)
        # 不同系统文件上传格式不一样。
        # 可能会返回二进制文件
        try:
            filename = res.get('Remote file_id').decode()
        except:
            filename = res.get('Remote file_id')

        # print('----------filename:', filename)
        return filename

    # Django判断文件名是否可用
    def exists(self, name):
        return False

    # 返回访问文件的url路径
    def url(self, name):
        return self.base_url+name