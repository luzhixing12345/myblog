
# bcc

编译参考 [bcc INSTALL](https://github.com/iovisor/bcc/blob/master/INSTALL.md)

```bash
git clone https://github.com/iovisor/bcc.git
mkdir bcc/build; cd bcc/build

# cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/bfs/bcc
cmake ..
make
sudo make install

# https://github.com/iovisor/bcc/pull/4716
# cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/bfs/bcc -DPYTHON_CMD=python3 -DPY_SKIP_DEB_LAYOUT=true
cmake -DPYTHON_CMD=python3 .. # build python3 binding
pushd src/python/
make
sudo make install
popd
```