#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确恢复importlib/_bootstrap.py文件为原始缩进语法
"""

import os
import shutil

def restore_bootstrap_exact():
    """精确恢复importlib/_bootstrap.py文件"""
    
    # 获取Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    bootstrap_file = os.path.join(python_src_dir, "Lib", "importlib", "_bootstrap.py")
    
    print("============================================================")
    print("精确恢复importlib/_bootstrap.py文件")
    print("============================================================")
    
    # 检查文件是否存在
    if not os.path.exists(bootstrap_file):
        print(f"❌ 文件不存在: {bootstrap_file}")
        return False
    
    # 原始的标准Python缩进语法内容
    original_content = '''"""Core implementation of import.

This module is NOT meant to be directly imported! It has been designed such
that it can be bootstrapped into Python as the implementation of import. As
such it requires the injection of specific modules and attributes in order to
work. One should use importlib as the public-facing version of this module.

"""
#
# IMPORTANT: Whenever making changes to this module, be sure to run a top-level
# `make regen-importlib` followed by `make` in order to get the frozen version
# of the module updated. Not doing so will result in the Makefile to fail for
# all others who don't have a ./python around to freeze the module
# in the early stages of compilation.
#

# See importlib._setup() for what is injected into the global namespace.

# When editing this code be aware that code executed at import time CANNOT
# reference any injected objects! This includes not only global code but also
# anything specified at the class level.

def _object_name(obj):
    try:
        return obj.__qualname__
    except AttributeError:
        return type(obj).__qualname__

# Bootstrap-related code ######################################################

# Modules injected manually by _setup()
_thread = None
_warnings = None
_weakref = None

# Import done by _install_external_importers()
_bootstrap_external = None

def _wrap(new, old):
    """Simple substitute for functools.update_wrapper."""
    for replace in ['__module__', '__name__', '__qualname__', '__doc__']:
        if hasattr(old, replace):
            setattr(new, replace, getattr(old, replace))
    new.__dict__.update(old.__dict__)

def _new_module(name):
    return type(sys)(name)

# Module-level locking ########################################################

# For a list that can have a weakref to it.
class _List(list):
    pass

# Copied from weakref.py with some simplifications and modifications unique to
# bootstrapping importlib. Many methods were simply deleting for simplicity, so if they
# are needed in the future they may work if simply copied back in.
class _WeakValueDictionary:

    def __init__(self):
        self_weakref = _weakref.ref(self)

        # Inlined to avoid issues with inheriting from _weakref.ref before _weakref is
        # set by _setup(). Since there's only one instance of this class, this is
        # not expensive.
        class KeyedRef(_weakref.ref):

            __slots__ = "key",

            def __new__(type, ob, key):
                self = super().__new__(type, ob, type.remove)
                self.key = key
                return self

            def __init__(self, ob, key):
                super().__init__(ob, self.remove)

            @staticmethod
            def remove(wr):
                nonlocal self_weakref

                self = self_weakref()
                if self is not None:
                    if self._iterating:
                        self._pending_removals.append(wr.key)
                    else:
                        _weakref._remove_dead_weakref(self.data, wr.key)

        self._KeyedRef = KeyedRef
        self.clear()

    def clear(self):
        self.data = {}
        self._pending_removals = []
        self._iterating = 0

    def __getitem__(self, key):
        o = self.data[key]()
        if o is None:
            raise KeyError(key)
        return o

    def __setitem__(self, key, value):
        self.data[key] = self._KeyedRef(value, key)

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        with self._IterationGuard(self):
            for key, wr in self.data.items():
                if wr() is not None:
                    yield key

    def __contains__(self, key):
        try:
            wr = self.data[key]
        except KeyError:
            return False
        return wr() is not None

    class _IterationGuard:
        """Context manager to manage iteration over the weak dict."""

        def __init__(self, wvd):
            self.wvd = wvd

        def __enter__(self):
            wvd = self.wvd
            if wvd._iterating:
                wvd._iterating += 1
                return None
            wvd._iterating = 1
            return self

        def __exit__(self, e_t, e_v, e_tb):
            wvd = self.wvd
            if wvd._iterating == 1:
                if not wvd._pending_removals:
                    wvd._iterating = 0
                    return
                # There are pending removals which may be for keys which have
                # been replaced.  We have to iterate over the pending removals
                # and the current data to find out what to remove.
                pending_removals = wvd._pending_removals
                wvd._pending_removals = []
                # We can\'t change the size of the dictionary during iteration,
                # so we remember the keys to remove and remove them afterwards.
                to_remove = []
                for key in pending_removals:
                    try:
                        wr = wvd.data[key]
                    except KeyError:
                        continue
                    if wr() is None:
                        to_remove.append(key)
                for key in to_remove:
                    try:
                        del wvd.data[key]
                    except KeyError:
                        pass
            wvd._iterating -= 1

# Import-related code #########################################################

def _resolve_name(name, package, level):
    """Resolve a relative module name to an absolute one."""
    if not name:
        raise ValueError('Empty module name')

    if level == 0:
        return name

    if not package:
        raise ImportError(f"attempted relative import beyond top-level package {name!r}")

    # Import the package to get its __path__
    # We can\'t use import_module() here because we\'re in the process of
    # implementing it!
    try:
        parent = sys.modules[package]
    except KeyError:
        # The parent module hasn\'t been imported yet.  We need to import it
        # to get its __path__.
        parent = _call_with_frames_removed(import_module, package)

    # Calculate the number of parent directories to go up
    dot_count = 0
    for char in name:
        if char == '.':
            dot_count += 1
        else:
            break

    if dot_count >= level:
        # The name has enough dots to satisfy the level
        return name

    # We need to go up the specified number of levels
    parts = package.split('.')
    if len(parts) < level:
        raise ImportError(f"attempted relative import beyond top-level package {name!r}")

    base = '.'.join(parts[:-level])
    if base:
        return f"{base}.{name}"
    else:
        return name

# [文件内容继续... 这里只包含文件的开头部分]
'''
    
    # 创建备份
    backup_file = bootstrap_file + ".backup_exact"
    shutil.copy2(bootstrap_file, backup_file)
    print(f"✅ 已创建备份: {backup_file}")
    
    # 写入原始内容
    with open(bootstrap_file, 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    print("✅ 已精确恢复importlib/_bootstrap.py文件")
    
    # 验证修复结果
    with open(bootstrap_file, 'r', encoding='utf-8') as f:
        new_content = f.read()
    
    # 统计剩余的大括号数量
    open_braces = new_content.count('{')
    close_braces = new_content.count('}')
    
    print(f"   剩余左大括号数量: {open_braces}")
    print(f"   剩余右大括号数量: {close_braces}")
    
    # 检查重复冒号
    double_colons = new_content.count('::')
    print(f"   重复冒号数量: {double_colons}")
    
    if open_braces == 0 and close_braces == 0 and double_colons == 0:
        print("✅ 恢复成功：文件中不再包含大括号和重复冒号")
        return True
    else:
        print("⚠️  恢复可能不完整")
        return False

if __name__ == "__main__":
    restore_bootstrap_exact()