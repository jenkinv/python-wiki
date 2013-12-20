import web
import codecs
import pygit2
import time
import markdown
from git import git
from config import *
from datetime import datetime,tzinfo,timedelta

### URLS
urls = (
  '/([^/]+)', 'IndexPage',
  '/([^/]+?)/(.+)', 'CommitPage'
)

class LocalTimezone(tzinfo):
  def utcoffset(self, dt):
    return timedelta(hours=8)
  def dst(self, dt):
    return timedelta(0)
  def tzname(self, dt):
    return '+08:00'

### Templates
t_globals = dict(
  datestr=web.datestr,
  datetime=datetime,
  LocalTimezone=LocalTimezone,
)
render = web.template.render('templates', base='base', globals=t_globals)


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
    utf8_codecs = codecs.lookup('ascii');
    content = content.encode('utf-8')
    git.git_do_commit_with_content(file_name, 'commit content without write workdir', content)
    raise web.seeother('/' + file_name);

class CommitPage:
  def GET(self, file_name, commit_oid):
    data = git.git_blob_data_from_comimit_oid(commit_oid, file_name)
    html_data = markdown.markdown(data.decode('utf-8'))
    render2 = web.template.render('templates', base='single_base', globals=t_globals)
    return render2.single_page(data, html_data)

app = web.application(urls, globals())

if __name__ == '__main__':
  app.run()
