import os
import io
import tarfile
import sys

print 'starting'

BLOCKSIZE = 512
NUL = "\0"

#tar = tarfile.open("arik.tar", "w")
tar = open("arik.tar", "w")
offset = 0
file2offset = {}

print 'writing ovf'
#ovf = StringIO.StringIO(sys.argv[1])

ovf = sys.argv[1]
info = tarfile.TarInfo(name="ovf")
info.size=len(ovf)
buf = info.tobuf()
tar.write(buf)
offset += len(buf)
tar.write(ovf)
blocks, remainder = divmod(info.size, BLOCKSIZE)
if remainder > 0:
    tar.write(NUL * (BLOCKSIZE - remainder))
    blocks += 1
offset += blocks * BLOCKSIZE


for arg in sys.argv[2:]:
    info = tarfile.TarInfo(name=os.path.basename(arg))
    info.size=1073741824
    buf = info.tobuf()
    tar.write(buf)
    offset += len(buf)
    # save the offset
    file2offset[arg] = offset
    tar.seek(offset + info.size)
    blocks, remainder = divmod(info.size, BLOCKSIZE)
    if remainder > 0:
        tar.write(NUL * (BLOCKSIZE - remainder))
        blocks += 1
    offset += BLOCKSIZE * blocks


# writing two null blocks at the end of the file
empty = NUL * 512
tar.write(empty)
tar.write(empty)


for file in file2offset:
    offset = file2offset[file]
    tar.seek(offset)
    fd = os.open("3a09f002-044d-478d-8733-58f4333941ee", os.O_RDWR)
    file = io.FileIO(fd, "r+")
    buf = bytearray(4096)
    buf2 = "\0"*4096
    mview = memoryview(buf)
    while 1:
        r = file.readinto(buf)
        if r == 0:
            break
        tar.write(buf)

tar.close()

