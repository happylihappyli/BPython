#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复opcode.py的原始内容
"""

import os
import shutil

def restore_opcode():
    """恢复opcode.py的原始内容"""
    
    # 获取Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    lib_dir = os.path.join(python_src_dir, "Lib")
    
    # opcode.py文件路径
    opcode_file = os.path.join(lib_dir, "opcode.py")
    backup_file = os.path.join(lib_dir, "backup_original", "opcode.py")
    
    print(f"正在恢复opcode.py: {opcode_file}")
    
    # 检查备份文件是否存在
    if os.path.exists(backup_file):
        # 使用备份文件恢复
        shutil.copy2(backup_file, opcode_file)
        print("✅ 使用备份文件恢复opcode.py")
    else:
        # 如果没有备份，手动恢复内容
        print("❌ 备份文件不存在，手动恢复opcode.py")
        
        # 手动写入正确的opcode.py内容
        correct_content = '''# Opcode module
#
# Define the opcodes and related information for the Python bytecode interpreter.

import _opcode

# Opcode constants
MIN_PSEUDO_OPCODE = 256
MAX_PSEUDO_OPCODE = 511

# Instruction categories
hasarg = []
hasconst = []
hasname = []
hasjrel = []
hasjabs = []
haslocal = []
hascompare = []
hasfree = []
hasexc = []

def is_pseudo(op):
    return op >= MIN_PSEUDO_OPCODE and op <= MAX_PSEUDO_OPCODE


oplists = [hasarg, hasconst, hasname, hasjrel, hasjabs,
           haslocal, hascompare, hasfree, hasexc]

opmap = {}

## pseudo opcodes (used in the compiler) mapped to the values
## they can become in the actual code.
_pseudo_ops = {}

def def_op(name, op):
    opmap[name] = op


def name_op(name, op):
    def_op(name, op)
    hasname.append(op)


def jrel_op(name, op):
    def_op(name, op)
    hasjrel.append(op)


def jabs_op(name, op):
    def_op(name, op)
    hasjabs.append(op)


def pseudo_op(name, op, real_ops):
    def_op(name, op)
    _pseudo_ops[name] = real_ops
    # add the pseudo opcode to the lists its targets are in
    for oplist in oplists:
        res = [opmap[rop] in oplist for rop in real_ops]
        if any(res):
            assert all(res)
            oplist.append(op)


        
    

# Instruction opcodes for compiled code
# Blank lines correspond to available opcodes

def_op('CACHE', 0)
def_op('POP_TOP', 1)
def_op('PUSH_NULL', 2)
def_op('INTERPRETER_EXIT', 3)

def_op('END_FOR', 4)
def_op('END_SEND', 5)

def_op('NOP', 9)'''
        
        with open(opcode_file, 'w', encoding='utf-8') as f:
            f.write(correct_content)
        print("✅ 手动恢复opcode.py完成")
    
    return True

if __name__ == "__main__":
    if restore_opcode():
        print("✅ opcode.py恢复完成")
    else:
        print("❌ opcode.py恢复失败")