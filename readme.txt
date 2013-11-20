Denpendencies:
1.libgit2:
  git clone git://github.com/libgit2/libgit2.git
  cd libgit2
  git checkout v0.19.0//pygit2 0.19.x need this version
  mkdir build & cd build
  cmake ..
  cmake --build .
  sudo cmake --build . --target install

2.pygit2(need pythonXX-dev)
  git clone git://github.com/libgit2/pygit2.git
  cd pygit2
  python setup.py install
  python setup.py test

3.webpy(download to your project)
  git clone git://github.com/webpy/webpy.git
  ln -s webpy/web .
  
Run:
  python demo.py
