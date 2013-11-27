import web
import codecs
import pygit2
import time
from git import git
from config import *

### URLS
urls = (
  '/([^/]+)', 'IndexPage',
  '/([^/]+?)/(.+)', 'CommitPage'
)

### Templates
render = web.template.render('templates', base='base')

class IndexPage:
  form = web.form.Form(
    web.form.Textarea('content', web.form.notnull, class_='u-ipt js-textarea', description=''),
    web.form.Button('update', class_="u-btn u-btn-1 f-fr js-submit")
  );

  def GET(self, file_name):
    data = git.git_blob_data_from_head_commit(file_name)
    field_content = self.form.get('content')
    field_content.set_value(data)
    all_file_names = git.git_file_list()
    commits = git.git_file_history(file_name)
    return render.index(commits, self.form, file_name, all_file_names)

  def POST(self, file_name):
    form = self.form;
    if not form.validates():
      return self.GET()
    content = form.d.content;
    #file_object = codecs.open(base_path + file_name, 'w','utf-8')
    #file_object.write(content)
    #file_object.close()
    #git.git_do_commit_with_workdir_modify(file_name, 'change content to:' + content)
    git.git_do_commit_with_content(file_name, 'commit content without write workdir', content)
    raise web.seeother('/' + file_name);

class CommitPage:
  def GET(self, file_name, commit_oid):
    return git.git_blob_data_from_comimit_oid(commit_oid, file_name)

app = web.application(urls, globals())

if __name__ == '__main__':
  app.run()
