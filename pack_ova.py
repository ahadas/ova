import os
import io
import tarfile
import sys
import time

BLOCKSIZE = 512
NUL = "\0"

tar = open(sys.argv[1], "w")

print 'writing ovf'
ovf = sys.argv[2]
info = tarfile.TarInfo(name="ovf")
info.size = len(ovf.encode('utf-8'))
info.mtime = time.time()
buf = info.tobuf()
tar.write(buf)
tar.write(ovf)
blocks, remainder = divmod(info.size, BLOCKSIZE)
if remainder > 0:
    tar.write(NUL * (BLOCKSIZE - remainder))
    blocks += 1

for arg in sys.argv[3:]:
    idx = arg.index(':')
    path = arg[:idx]
    size = int(arg[idx+1:])
    print 'writing disk %s (%d)' % (path, size)
    fd = os.open(path, os.O_RDWR)
    basename = os.path.basename(path)
    info = tarfile.TarInfo(name=basename)
    info.size = size
    info.mtime = time.time()
    buf = info.tobuf()
    tar.write(buf)
    file = io.FileIO(fd, "r+")
    buf = bytearray(4096)
    while 1:
        r = file.readinto(buf)
        if r == 0:
            break
        tar.write(buf)
    blocks, remainder = divmod(info.size, BLOCKSIZE)
    if remainder > 0:
        tar.write(NUL * (BLOCKSIZE - remainder))


# writing two null blocks at the end of the file
empty = NUL * 512
tar.write(empty)
tar.write(empty)


tar.close()

