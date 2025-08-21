"""
记载本软件内置的所有错误类型
"""

class EDAWBaseException(Exception):
    def __init__(self, message):
        super(EDAWBaseException, self).__init__(message)


class WaveGenerateError(EDAWBaseException, TypeError):

    def __init__(self, message):
        super(WaveGenerateError, self).__init__(message)