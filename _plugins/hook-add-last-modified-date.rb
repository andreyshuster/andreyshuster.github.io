Jekyll:Hooks.register :posts :pre_render do |post|
  mod_time = File.mtime(post.path)
  post.data['last-modified-date'] = mod_time
end
