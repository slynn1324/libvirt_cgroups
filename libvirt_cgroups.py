import pathlib
import glob
import os
import re

def getNewLinks():
    rval = {}
    dirs = glob.glob('/sys/fs/cgroup/machine.slice/machine-qemu*')
    for d in dirs:
        path = pathlib.PurePath(d)
        name = path.name
        name = re.sub('\\\\x2d', '-', name)
        name = re.sub('machine-qemu[-][0-9]+[-]', '', name)
        name = re.sub('[.]scope$', '', name)
        rval[name] = path.as_posix()
    return rval

new_links = getNewLinks()


# create or update links
for vm in new_links:
    print(vm)

    link_src = new_links[vm]
    link_dst = '/libvirt_cgroups/' + vm

    if ( os.path.islink(link_dst) ):
        print("  link exists " + link_src)

        target = pathlib.Path(link_dst).resolve().as_posix();
        print("   -> " + target)

        if ( target == link_src ):
            print("  target matches, no update")
        else:
            print("  target differs, update")
            os.remove(link_dst)
            os.symlink(link_src, link_dst)
    else:
        print("link does not exist for " + vm)
        os.symlink(link_src, link_dst)



# delete old links...
cgroup_links = glob.glob("/libvirt_cgroups/*")
for l in cgroup_links:
    name = pathlib.PurePath(l).name
    if name not in new_links:
        print("cgroup no longer exists, removing link: " + l)
        os.remove(l)

