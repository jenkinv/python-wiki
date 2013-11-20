import web
import pygit2
import time
urls = (
  '/(.*)', 'hello'
)
base_path = 'webpy/'
file_name = 'test.txt'
file_path = base_path + file_name
git_dir = base_path + '.git'

app = web.application(urls, globals())

class hello:
  def GET(self, name):
    if not name:
      name = 'World'
    file_object = open(file_path, 'w')
    file_object.write(name)
    file_object.close()
    self.git_commit('change content to:' + name)
    return 'Hello,' + name + '!'
  def git_commit(self, message):
    repo = pygit2.Repository(git_dir);
    index = repo.index
    index.add(file_name)
    index.write()
    oid = index.write_tree()
    author = pygit2.Signature('zjw', 'jenkinv@163.com', int(time.time()), 480);
    repo.create_commit('HEAD', author, author, message, oid, [repo.head.target]);
if __name__ == '__main__':
  app.run()
