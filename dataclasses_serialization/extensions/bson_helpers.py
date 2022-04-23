try:
    import bson

    try:
        # Assume py-bson version of bson installed
        bson_loads = bson.loads
        bson_dumps = bson.dumps

    except AttributeError:
        # Fallback to pymongo version of bson
        bson_loads = lambda bson_str: bson.BSON(bson_str).decode()
        bson_dumps = bson.BSON.encode

except ImportError:
    raise ImportError("py-bson or pymongo required for BSON serialization")
