import pygit2
import time
from config import *

class Git:
  try:
    repo = pygit2.Repository(base_path)
  except Exception,data:
    print 'First Time, Init Repository NOW'
    repo = pygit2.init_repository(base_path, bare=True)
  def git_do_commit_with_workdir_modify(self, file_name, message):
    index = self.repo.index
    index.add(file_name)
    index.write()
    tree_oid = index.write_tree()
    self.git_do_commit_with_tree_oid(tree_oid, message)

  def git_do_commit_with_tree_oid(self, tree_oid, message):
    author = pygit2.Signature('zjw', 'jenkinv@163.com', int(time.time()), 480);
    self.repo.create_commit('HEAD', author, author, message, tree_oid, [self.repo.head.target]);

  def git_do_commit_with_content(self, file_name, message, content):
    blob_oid = self.repo.create_blob(content)
    head_commit_tree = self.repo.revparse_single('HEAD').tree;
    tree_builder = self.repo.TreeBuilder(head_commit_tree)
    tree_builder.insert(file_name, blob_oid, pygit2.GIT_FILEMODE_BLOB)
    tree_oid = tree_builder.write()
    self.git_do_commit_with_tree_oid(tree_oid, message)

  def git_blob_data_from_head_commit(self, file_name):
    commit = self.repo.revparse_single('HEAD');
    return self.git_blob_data_from_commit(commit, file_name)

  def git_blob_data_from_comimit_oid(self, commit_oid, file_name):
    commit = self.repo[commit_oid]
    return self.git_blob_data_from_commit(commit, file_name)

  def git_blob_data_from_commit(self, commit, file_name):
    if file_name in commit.tree :
      tree_entry = commit.tree[file_name]
    else:
      return ''
    blob = self.repo[tree_entry.oid]
    return blob.data;

  def git_file_history(self, file_name):
    commits = []
    last_oid = None
    for commit in self.repo.walk(self.repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL | pygit2.GIT_SORT_REVERSE):
      if file_name in commit.tree:
        file_oid = commit.tree[file_name].oid
        has_changed = (last_oid != file_oid)
        if not has_changed:
          continue
        else:
          last_oid = file_oid
      else:
        continue
      commits.insert(0,commit)
    return commits

  def git_file_list(self):
    commit = self.repo.revparse_single('HEAD')
    tree = commit.tree
    file_names = []
    for tree_entry in tree:
      file_names.append(tree_entry.name)
    return file_names
git = Git()