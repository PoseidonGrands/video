def enum_type_check(obj, type, msg):
    """检查传入的类型是否存在于指定枚举类型中"""
    try:
        obj[type]
    except:
        return {'code': -1, 'msg': msg}
    return {'code': 1, 'msg': 'success'}


def validate_data(*args, **kwagrs):
    """验证是否存在错误"""
    error = ''
    print(args)
    if not all([]):
        error = 'missing field...'
    return error