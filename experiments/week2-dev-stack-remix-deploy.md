# Day 9: Dev Stack 实践 — Remix 部署 Counter 合约

**日期**: 2026-05-26

---

## 实践目标

用 Remix 部署一个极简计数器合约，验证"写→编译→部署→交互"的完整链路。

---

## 操作步骤

### 1. 编写合约

在 Remix IDE 创建 `Counter.sol`：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Counter {
    uint256 public count;

    event CountChanged(uint256 newCount);

    function increment() public {
        count += 1;
        emit CountChanged(count);
    }

    function getCount() public view returns (uint256) {
        return count;
    }
}
```

### 2. 编译

- 选择 Solidity 编译器版本 `0.8.x`
- 点击 **Compile Counter.sol**
- 生成 bytecode 和 ABI

### 3. 部署

- 环境选择 **Remix VM (Cancun)**
- 点击 **Deploy**
- 合约地址：`0xd9145CCE52D386f254917e481eB44e9943F39138`
- 交易哈希：`0x1a10b5f878060a2a3962f561b355b057e367659684de4077f8631e9a48b8790c`

### 4. 交互

- 展开 **Deployed Contracts**
- 点击蓝色按钮 `getCount()` → 返回 `0`
- 点击橙色按钮 `increment()` → 弹出交易日志
- 再次点击 `getCount()` → 返回 `1`
- 在 Terminal 日志中查看 `CountChanged` event

---

## 关键产出

| 项目 | 值 |
|------|------|
| 合约地址 | `0xd9145CCE52D386f254917e481eB44e9943F39138` |
| 部署网络 | Remix VM (Cancun) |
| 部署账户 | `0x5B38Da6a701c568545dCfcB03FcB875f56beddC4` |
| 交易哈希 | `0x1a10b5f878060a2a3962f561b355b057e367659684de4077f8631e9a48b8790c` |
| ABI | 已复制到 `abi.json` |

---

## 未完成部分

Hardhat 本地工程搭建因 Node.js v25.4.0 版本过高，依赖反复冲突（TypeScript 缺失、ESM 模块冲突、hardhat-toolbox 版本冲突），最终放弃。

**后续计划**：使用 nvm 降级到 Node.js LTS（v18/v20）后重试 Hardhat 实践。

---

## 收获

- Remix 适合快速原型，但不适合工程化项目
- 正式项目应迁入 Hardhat/Foundry + Git
- 合约地址、ABI、部署网络必须进版本控制
- 私钥、RPC URL 必须放在 `.env` 或密钥管理里

---

*AI x Web3 School Day 9 实践完成 — 由 Hermes AI（模型：阿里百炼免费模型）在 2026-05-26 生成*
