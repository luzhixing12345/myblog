
# uv

## 安装

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
pip install uv
```

下载 https://github.com/astral-sh/uv/releases

## 换源

~/.config/uv/uv.toml

```toml
[[index]]
url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
default = true
```

## 使用

```bash
uv python install 3.10
```

```bash
source .venv/bin/activate
```