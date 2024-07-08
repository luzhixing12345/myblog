
# cli

```bash
ls /boot | grep 6.6 | xargs -I {} cp /boot/{} ~/workspace/
```

xargs -I 创建一个匹配组