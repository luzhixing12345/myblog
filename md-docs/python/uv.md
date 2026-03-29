
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
uv python install 3.13
```

```bash
uv venv --python 3.13
```

```bash
source .venv/bin/activate
uv pip install pip
```

[pytorch locally](https://pytorch.org/get-started/locally/)

```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu129
```