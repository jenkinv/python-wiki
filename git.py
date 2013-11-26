import pygit2
import time
from config import *

class Git:
  repo = pygit2.Repository(git_dir)
  def git_do_commit(self, file_name, message):
    index = self.repo.index
    index.add(file_name)
    index.write()
    oid = index.write_tree()
    author = pygit2.Signature('zjw', 'jenkinv@163.com', int(time.time()), 480);
    self.repo.create_commit('HEAD', author, author, message, oid, [self.repo.head.target]);

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
    for commit in self.repo.walk(self.repo.head.target, pygit2.GIT_SORT_NONE):
      if file_name in commit.tree:
        tree_entry = commit.tree[file_name]
      else:
        continue
      commits.append(commit)
    return commits

  def git_file_list(self):
    commit = self.repo.revparse_single('HEAD')
    tree = commit.tree
    file_names = []
    for tree_entry in tree:
      file_names.append(tree_entry.name)
    return file_names
git = Git()