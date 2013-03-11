
import sys
from gu.ands.handle.pids import AndsPidService
from gu.ands.handle.settings import CONFIG


def usage(msg):
    print msg
    print "Usage:", sys.argv[0], "cmd args"
    print ""
    print " cmd is on of: "
    print "    mint, addValue, listHandles, getHandle, modifyValueByIndex "
    print " params depends on cmd."
    sys.exit(1)


def parsecli():
    if not len(sys.argv) >= 2:
        usage("missing command")
    cmd = sys.argv[1]
    if cmd == "mint":
        if len(sys.argv) == 2:
            kwargs = {"type": "",
                      "value": ""}
        elif len(sys.argv) == 4:
            kwargs = {"type": sys.argv[2],
                      "value": sys.argv[3]}
        else:
            usage("mint needs type ('DESC', 'URL') and value or nothing as  parameters.")
    elif cmd == "addValue":
        if len(sys.argv) == 5:
            kwargs = {"handle": sys.argv[2],
                      "type": sys.argv[3],
                      "value": sys.argv[4]}
        else:
            usage("addValue needs handle, type ('DESC', 'URL') and value as parameters.")
    elif cmd == "listHandles":
        if len(sys.argv) == 2:
            kwargs = {"starthandle": ""}
        elif len(sys.argv) == 3:
            kwargs = {"starthandle": sys.argv[2]}
        else:
            usage("listHandles accepts only one optional parameter. (the last handle to list from)")
    elif cmd == "getHandle":
        if len(sys.argv) == 3:
            kwargs = {"handle": sys.argv[2]}
        else:
            usage("getHandle needs a handle as parameter")
    elif cmd == "modifyValueByIndex":
        if len(sys.argv) == 5:
            kwargs = {"handle": sys.argv[2],
                      "index": sys.argv[3],
                      "value": sys.argv[4]}
        else:
            usage("modifyValueByIndex needs handle, index and value as parameters.")
    else:
        usage("")
    return cmd, kwargs


def main():
    cmd, kwargs = parsecli()
    svc = AndsPidService(CONFIG["url"], CONFIG["appid"],
                         CONFIG["identifier"], CONFIG["authdomain"])
    if cmd == "mint":
        ret = svc.mint(**kwargs)
    elif cmd == "addValue":
        ret = svc.addValue(**kwargs)
    elif cmd == "listHandles":
        ret = svc.listHandles(**kwargs)
    elif cmd == "getHandle":
        ret = svc.getHandle(**kwargs)
    elif cmd == "modifyValueByIndex":
        ret = svc.modifyValueByIndex(**kwargs)
    else:
        usage()
    print str(ret)

if __name__ == "__main__":
    main()
