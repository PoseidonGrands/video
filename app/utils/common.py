def enum_type_check(obj, type, msg):
    try:
        obj[type]
    except:
        return {'code': -1, 'msg': msg}
    return {'code': 1, 'msg': 'success'}
