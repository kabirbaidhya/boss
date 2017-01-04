from fabric.colors import red


def halt(msg):
    raise SystemExit(red(msg))
