import os
import io
import shutil
import tempfile
import tarfile
import sys
import StringIO

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


#info = tarfile.TarInfo(name="disk2")
#info.size=100000
#buf = info.tobuf()
#tar.write(buf)
#offset += len(buf)
## save the offset
#tar.seek(offset + info.size)
#blocks, remainder = divmod(info.size, BLOCKSIZE)
#if remainder > 0:
#    tar.write(NUL * (BLOCKSIZE - remainder))
#    blocks += 1
#offset += BLOCKSIZE * blocks


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
#    file.seek(counter)
        tar.write(buf)

   

#fd = os.open("3a09f002-044d-478d-8733-58f4333941ee", os.O_RDWR | os.O_DIRECT)
#fd = os.open("3a09f002-044d-478d-8733-58f4333941ee", os.O_RDWR)
#file = io.FileIO(fd, "r+")
#file = io.FileIO(fd, "r+", closefd=True)

print 'creating temporary file'
fd2 = os.open("sss", os.O_WRONLY | os.O_CREAT)
file2 = io.FileIO(fd2, "w+", closefd=True)


print 'copying file'
buf = bytearray(4096)
mview = memoryview(buf)
counter=0
#while 1:
#    r = file.readinto(mview)
#    print r
#    if r == 0:
#        break
#    counter = counter + r
#    file.seek(counter)
#    file2.write(mview)

#r = file.readinto(mview)
#print r
#counter = counter + r
#tar.write(mview)

tar.close()

