# Windows 与 Linux 打开文件的完整过程对比

## 概述

打开文件在两种系统中的核心问题相同：**将用户给定的文件路径解析为具体的数据在磁盘上的位置**。但两种系统在路径解析机制、目录结构、权限模型、缓存方式和最终的数据访问路径上差异显著。

| 对比维度 | Windows (NTFS) | Linux (ext4) |
|---|---|---|
| 文件系统类型 | NTFS | ext4 / xfs 等 |
| 目录结构 | 树型（驱动器号 + 路径） | 单一根树（/） |
| PCB 索引结构 | MFT（Master File Table） | inode 表 |
| 路径分隔符 | `\` | `/` |
| 路径解析方式 | 从 MFT 根开始逐层查 | 从 inode 根（2）开始逐层查 |
| 打开结果 | 返回句柄（HANDLE） | 返回文件描述符（fd） |

---

## 一、Linux 打开文件的完整过程（以 ext4 为例）

假设调用 `open("/home/user/a.txt", O_RDONLY)`。

### 阶段 1：用户态 → 内核态

```
用户程序
  │ 调用 open()（glibc 封装）
  │
  ├── glibc 将参数压栈，触发 `syscall` 指令（x86-64）
  │   └── CPU 切换到内核态（ring 0）
  │
  └── 进入内核的 sys_open() 系统调用处理
```

### 阶段 2：路径解析（namei / path_walk）

```
sys_open()
  │
  └── do_sys_open() → do_filp_open() → path_openat()
        │
        ├── 获取根目录 inode：当前命名空间根 inode（/ 的 inode 号为 2）
        │
        └── 逐分量查找（path_walk / link_path_walk）
              │
              ├── 分量 "home"：
              │   ├── 读根目录的数据块（ext4 通过 inode 2 找到目录数据块）
              │   ├── 在目录数据块中线性搜索 "home" 的目录项（ext4_dx_entry）
              │   └── 找到 home 的 inode 号
              │
              ├── 分量 "user"：
              │   ├── 读 home 目录的数据块（inode → 数据块）
              │   ├── 搜索 "user" 的目录项
              │   └── 找到 user 的 inode 号
              │
              └── 分量 "a.txt"：
                  ├── 读 user 目录的数据块
                  ├── 搜索 "a.txt" 的目录项
                  └── 找到 a.txt 的 inode 号
```

**每个目录分量的查找步骤**：

```
读取目录 inode
    ↓
从 inode 获得目录数据块位置（extent tree）
    ↓
读取目录数据块 → 遍历目录项（以 hash 索引加速 ext4）
    ↓
匹配到目标文件名的目录项 → 获取目标 inode 号
    ↓
将目标 inode 缓存到 dentry cache
```

### 阶段 3：inode 加载与权限检查

```
获得 a.txt 的 inode 号
    │
    ├── ext4_iget()：从磁盘 inode 表读取 inode 到内存
    │   └── 关键信息：文件模式、属主、大小、数据块指针（extent tree）、时间戳
    │
    ├── 权限检查：进程 uid/gid vs inode 的属主/权限位
    │   └── 失败 → 返回 EACCES
    │
    └── 检查其他标志（O_CREAT、O_TRUNC 等）
```

### 阶段 4：创建内核数据结构

```
├── 分配 struct file（文件对象）
│   ├── f_path = 已解析的路径
│   ├── f_inode = 指向 inode
│   ├── f_pos = 0（当前读写偏移）
│   ├── f_mode = O_RDONLY
│   └── f_op = ext4_file_operations（函数指针表）
│
├── 将 struct file 插入进程的 files_struct 表
│   └── 返回的表索引就是文件描述符（fd）
│
└── 将 dentry 和 inode 加入缓存（dcache / inode cache）
```

### 阶段 5：返回到用户态

```
sys_open 返回 fd（整数，如 3）
    │
    └── glibc 将 fd 返回给用户程序
```

---

## 二、Windows 打开文件的完整过程（以 NTFS 为例）

假设调用 `CreateFile("C:\\Users\\user\\a.txt", GENERIC_READ, ...)`。

### 阶段 1：用户态 → 内核态

```
应用程序
  │ 调用 CreateFile()（kernel32.dll）
  │
  ├── kernel32 调用 NtCreateFile()（ntdll.dll）
  │   └── 触发 syscall 进入内核态
  │
  └── 进入 ntoskrnl.exe 的 IoCreateFile()
```

### 阶段 2：路径解析（ObpLookupObjectName + ntfs 解析）

```
IoCreateFile()
  │
  ├── ObpLookupObjectName()：在对象管理器中解析路径
  │   ├── 先找到根目录对象 "\"
  │   │   └── 即 \GLOBAL?? 对象目录
  │   └── 解析 "C:" → 找到 C: 设备（\Device\HarddiskVolume1）
  │
  └── 剩余路径 "\Users\user\a.txt" 交给 ntfs.sys 驱动
        │
        └── NtfsParse() → 逐分量查找
              │
              ├── 读卷的 $Root 索引（MFT 中根目录的 $INDEX_ROOT）
              │
              ├── 查找 "Users"：
              │   ├── 读根目录的 B+ 树索引（$INDEX_ALLOCATION）
              │   ├── 在 B+ 树中搜索 "Users"
              │   └── 找到 Users 的 MFT 引用号
              │
              ├── 查找 "user"：
              │   └── 读 Users 目录的 B+ 树索引，找到 user 的 MFT 引用号
              │
              └── 查找 "a.txt"：
                  ├── 读 user 目录的 B+ 树索引
                  ├── 搜索 "a.txt"
                  └── 找到 a.txt 的 MFT 引用号
```

### 阶段 3：MFT 加载与安全检查

```
找到 a.txt 的 MFT 引用号
    │
    ├── 读 MFT 中对应的 MFT Entry（Master File Table Record）
    │   └── MFT Entry 中包含：
    │       ├── 标准属性（$STANDARD_INFORMATION）
    │       ├── 文件名属性（$FILE_NAME）
    │       ├── 安全描述符（$SECURITY_DESCRIPTOR）
    │       └── 数据属性（$DATA）：常驻 or 非常驻
    │
    ├── SeAccessCheck()：检查 DACL 是否允许当前用户访问
    │   └── 失败 → 返回 STATUS_ACCESS_DENIED
    │
    └── 检查 CreateOptions 标志
```

### 阶段 4：创建内核对象

```
├── 创建 FILE_OBJECT（文件对象）
│   ├── DeviceObject = 指向卷设备
│   ├── Vpb = 卷参数块
│   ├── SectionObjectPointer = 用于内存映射
│   ├── CurrentByteOffset = 0
│   └── Flags = 访问模式
│
├── 将 FILE_OBJECT 插入进程的句柄表
│   └── 返回的索引就是句柄值（HANDLE）
│
└── 缓存结果：MFT Entry 缓存在 ntfs 的缓存管理器中
```

### 阶段 5：返回到用户态

```
NtCreateFile 返回 HANDLE（如 0x000000E4）
    │
    └── kernel32 通过 HANDLE 返回给应用程序
```

---

## 三、核心差异对比

### 3.1 目录结构差异

| | Linux (ext4) | Windows (NTFS) |
|---|---|---|
| 根 | `/`，inode 2 | `\`，MFT Entry 5（根目录） |
| 目录项组织 | 线性 / hash 索引（ext4_dx_entry） | **B+ 树**索引（$INDEX_ROOT + $INDEX_ALLOCATION） |
| 文件名编码 | 字节流（通常 UTF-8） | UTF-16 LE（大小写不敏感） |
| 文件名大小写 | **敏感** | 不敏感（保留大小写） |
| 硬链接 | 支持（inode 级） | 支持（NTFS links） |
| 快捷方式 | 软链接（symlink） | .lnk 文件（文件级） |

### 3.2 元数据组织差异

| | Linux (ext4) | Windows (NTFS) |
|---|---|---|
| FCB 存储 | inode 数组（固定大小，格式化时分配） | MFT（Master File Table），动态扩展文件 |
| FCB 大小 | 固定 256 B（ext4） | 可变 1 KB（一个 MFT Record） |
| 小文件数据 | 可存在 inode 的 extent block 中 | **直接存 MFT Entry 的 $DATA 属性**（常驻文件） |
| 扩展属性 | xattr 系统 | $EA 属性 + $EA_INFORMATION |

### 3.3 权限模型差异

```
Linux：DAC（Discretionary Access Control）
  ├── owner / group / others × rwx
  └── ACL（扩展）+ LSM（如 SELinux）

Windows：DACL + SACL（安全审计）
  ├── 每个 MFT Entry 包含安全描述符
  └── 权限粒度更细（read/execute/write/delete/change permission...）
```

### 3.4 打开句柄 vs 文件描述符

| | fd (Linux) | HANDLE (Windows) |
|---|---|---|
| 本质 | 进程文件表中的整数索引 | 对象管理器句柄表中的索引 |
| 跨进程传递 | fork/exec 时按需继承 | DuplicateHandle() 显式复制 |
| 数值范围 | 小整数（0、1、2…） | 32 位整数，通常 4 的倍数 |
| 关闭 | close(fd) | CloseHandle(hFile) |
| 指向 | struct file | FILE_OBJECT |

---

## 四、打开文件后的完整 I/O 路径（对比）

### Linux 读文件：read(fd, buf, 1024)

```
read()
  │
  ├── sys_read() → vfs_read()
  │   ├── 通过 fd 找到 struct file
  │   │
  │   ├── 检查 file->f_op->read 是否存在
  │   │   └── ext4_file_read_iter()
  │   │
  │   ├── 通用块层（generic_block_io）
  │   │   └── 通过 inode 的 extent tree 求文件偏移 → 物理块号
  │   │
  │   ├── 页缓存（page cache）：
  │   │   ├── 检查 page cache 是否命中
  │   │   └── 未命中 → 缺页 → submit_bio() 提交 I/O
  │   │
  │   ├── I/O 调度层（cfq / deadline / noop）
  │   │
  │   └── 磁盘驱动 → 磁盘
  │
  └── 返回
      f_pos += 已读字节数
```

### Windows 读文件：ReadFile(hFile, buf, 1024, &bytesRead, NULL)

```
ReadFile()
  │
  ├── NtReadFile() → IoPageRead()
  │   ├── 通过 HANDLE 找到 FILE_OBJECT
  │   │
  │   ├── IRP 构建（I/O Request Packet）
  │   │   └── MajorFunction = IRP_MJ_READ
  │   │
  │   ├── 缓存管理器（Cache Manager）：
  │   │   ├── 文件映射到系统缓存区（VACB）
  │   │   └── 未命中 → MmAccessFault() → 缺页
  │   │
  │   ├── 卷管理驱动 → 磁盘驱动
  │   │
  │   └── 完成 IRP → 返回数据
  │
  └── 返回
      FilePointer += 已读字节数
```

### 对比：读文件路径

| 层级 | Linux | Windows |
|---|---|---|
| 系统调用 | sys_read → vfs_read | NtReadFile → IoPageRead |
| 偏移管理 | f_pos（struct file 中） | CurrentByteOffset（FILE_OBJECT 中） |
| 缓存 | Page Cache（页级，与 VM 统一） | 缓存管理器（VACB，独立于 VM） |
| 异步 IO | AIO / io_uring | Overlapped I/O（LPOVERLAPPED） |
| 驱动模型 | VFS → 具体 FS → 通用块层 → I/O 调度 | IRP 包 → 文件系统驱动 → 卷管理 → 磁盘驱动 |

---

## 典型例题

**例 1**：Linux 中，进程执行 `open("/usr/include/stdio.h", O_RDONLY)`，最少需要读几次磁盘？（假设所有目录和 inode 都不在缓存中，每个目录需读一次 inode 和一次数据块）

解：
逐分量解析：
- `/`：inode 2 已知（常驻），读根目录数据块搜 "usr" = 1 次
- `usr`：读 usr 的 inode（1 次）+ 读 usr 目录数据块搜 "include"（1 次）= 2 次
- `include`：读 include 的 inode（1 次）+ 读 include 目录数据块搜 "stdio.h"（1 次）= 2 次
- `stdio.h`：读 stdio.h 的 inode（1 次）

**最少磁盘 I/O = 1 + 2 + 2 + 1 = 6 次**（不含 inode 表本身的读取）。

**例 2**：对比 Windows 和 Linux 打开 "C:\Users\a\b.txt" 和 "/home/user/a/b.txt" 在目录查找时的数据结构差异。

在 Windows 中，NTFS 用 B+ 树索引目录（$INDEX_ROOT / $INDEX_ALLOCATION），大目录查找效率为 O(log n)；Linux ext4 用线性扩展 + 两级 hash 索引（htree），大目录平均查找 O(1) 但最差 O(n)。NTFS 的 B+ 树对目录项插入/删除更友好（平衡自动维护），ext4 的 htree 超过一定深度会退化为线性。

---

## 易错点

1. **Linux 中路径解析从 inode 2 开始**：root 目录的 inode 号固定为 2，不是 0 或 1
2. **Windows 中 "C:" 不是路径起点**：C: 本身是一个符号链接对象（\GLOBAL??\C:），指向 \Device\HarddiskVolume1
3. **文件描述符和句柄的正确关闭方式**：Linux 用 close(fd) ≠ Windows CloseHandle(hFile)，混用会导致资源泄漏
4. **dentry 和 inode 的缓存关系**：Linux 的 dentry cache 和 inode cache 是分开的。open 后 dentry 先缓存，inode 随后。再次打开同名文件时，dentry 命中可跳过路径解析
5. **常驻 vs 非常驻属性**（NTFS）：小文件（<~900 B）的数据直接存在 MFT Entry 中，无需数据块寻址，读文件省去一次读盘

---

## 关联知识

- 与「目录项、FCB、簇号与盘块大小的关系」直接衔接——本篇讲打开流程，上篇讲目录项/FCB 的结构
- 与「成组连接法」同属文件管理——成组连接管空闲分配，本篇管已分配文件的访问
- 与「Inode 结构」「MFT 结构」互补（如后续有专门笔记）

---

*归档于 2026-07-12*
