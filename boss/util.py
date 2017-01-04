from fabric.colors import red, green


def info(msg):
    print '\n' + green(msg)


def halt(msg):
    raise SystemExit(red(msg))
