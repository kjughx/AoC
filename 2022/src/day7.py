from dataclasses import dataclass

class File:
    def __init__(self, size, name):
        self.name = name,
        self.size = size

    def __repr__(self):
        return f"File(name={self.name}, size={self.size})"

    def calcSize(self):
        pass

    def isDir(self):
        return False

class Dir:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.contents = []
        self.size = 0

    def __repr__(self):
        if self.parent is not None:
            return f'Dir(parent={self.parent.name}, name={self.name}, contents={self.contents}, size={self.size})'
        else:
            return f'Dir(parent=None, name={self.name}, contents={self.contents}, size={self.size})'
    
    def isDir(self):
        return True

    def refresh(self, filesystem):
        for content in self.contents:
            if content.isDir():
                content = filesystem.files[content.name]

    def calcSize(self):
        self.size = 0
        for content in self.contents:
            if content.isDir():
                if filesystem.files[content.name].size == 0:
                    filesystem.files[content.name].calcSize()
                self.size += filesystem.files[content.name].size
            else:
                self.size += content.size

class Filesystem:
    def __init__(self):
        self.files = {}
        self.current = '/'
        self.files['/'] = Dir(None, '/')
        self.root = self.current

    def godown(self, name):
        if not name in self.files.keys():
            self.files[name] = Dir(self.current, name)
        self.current = self.files[name]

    def goup(self):
        if self.current.parent is None:
            self.current = self.files['/']
        else:
            self.current = self.current.parent

    def addContent(self, contents):
        self.current.contents.extend(contents)

    def ls(self):
        return self.current.contents

with open(0) as file:
    cmds = []
    for line in file.readlines():
        cmds.append(line.strip('\n'))

    n = 0
    filesystem = Filesystem()
    while n < len(cmds):
        line = cmds[n]
        cmd = line.split(' ')

        if cmd[0] == '$' and cmd[1] == "cd":
            path = cmd[2]
            if path == "..":
                filesystem.goup()
            else:
                filesystem.godown(path)

        elif cmd[1] == "ls":
            contents = []
            parent = filesystem.files[filesystem.current.name]

            while n < len(cmds) - 1:
                if cmds[n+1][0] == '$':
                    break
                cmd = cmds[n+1]
                entry = cmd.split(' ')
                if entry[0] == "dir":
                    if parent == '/':
                        contents.append(Dir(None, entry[1]))
                    else:
                        contents.append(Dir(parent, entry[1]))
                else:
                    contents.append(File(int(entry[0]), entry[1]))
                n += 1
            filesystem.addContent(contents)
        n += 1

    sum = 0
    for file in filesystem.files:
        filesystem.files[file].calcSize()
    for file in filesystem.files:
        filesystem.files[file].refresh(filesystem)
    for file in filesystem.files:
        if filesystem.files[file].size < 100000:
            sum += filesystem.files[file].size
    print(sum)

