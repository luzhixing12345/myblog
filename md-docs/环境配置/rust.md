
# rust

在Linux上安装Rust一般会很简单. 但是在国内,有时候,安装过程会很慢甚至不稳定. 因此,我可能会需要配置toolchain和rustup更新服务器的镜像. 

```bash
# 用于更新 toolchain
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
# 用于更新 rustup
export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup
```

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

安装过程选第一个

```bash
Current installation options:


   default host triple: x86_64-unknown-linux-gnu
     default toolchain: stable (default)
               profile: default
  modify PATH variable: yes

1) Proceed with standard installation (default - just press enter)
2) Customize installation
3) Cancel installation
>
```

笔者用的是 bash, rust 安装之后默认会将 ". "$HOME/.cargo/env" 加入到结尾, source 一下或者重开一个 bash 就可以正常用 rust 相关的工具链了

在国内我们还有可能需要配置 [crates.io](http://crates.io) 的镜像.我们可以通过修改配置文件 ~/.cargo/config(如果不存在则需要手动创建)来配置镜像, 使用清华源镜像 [tuna mirrors](https://mirrors.tuna.tsinghua.edu.cn/help/crates.io-index.git/)

```toml
[source.crates-io]
replace-with = 'mirror'

[source.mirror]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"
```

初次 install 时需要很长一段时间下载索引

## 常用工具

### 代码行数统计

[tokei](https://github.com/XAMPPRocky/tokei)

```bash
cargo install tokei
```

```bash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Language            Files        Lines         Code     Comments       Blanks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 BASH                    4           49           30           10            9
 JSON                    1         1332         1332            0            0
 Shell                   1           49           38            1           10
 TOML                    2           77           64            4            9
───────────────────────────────────────────────────────────────────────────────
 Markdown                5         1355            0         1074          281
 |- JSON                 1           41           41            0            0
 |- Rust                 2           53           42            6            5
 |- Shell                1           22           18            0            4
 (Total)                           1471          101         1080          290
───────────────────────────────────────────────────────────────────────────────
 Rust                   19         3416         2840          116          460
 |- Markdown            12          351            5          295           51
 (Total)                           3767         2845          411          511
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Total                  32         6745         4410         1506          829
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

建议加一个 alias tokei="tokei -s files" 按文件数量统计

## 参考

- [Linux上安装rust](https://zhuanlan.zhihu.com/p/308452799)